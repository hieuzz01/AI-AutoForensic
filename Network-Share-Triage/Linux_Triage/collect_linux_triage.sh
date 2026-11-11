#!/bin/sh
# ==============================================================================
# V-AutoFor Agentless Linux Live Triage Collector (RFC 3227 Compliant)
#
# TWO-PHASE, STATE-DRIVEN DESIGN (no arguments):
#   Call 1 (START):  Collects volatile state, live logs, user config, then
#                    launches a 5-minute (300s) live PCAP capture in the
#                    background (detached, survives session close) and
#                    exits immediately. No SUCCESS line -> MCP tool call
#                    stays far below the 300s per-call safety cap.
#   Call 2 (FINISH): Waits for tcpdump to finish, moves the pcap into the
#                    work tree, archives everything, computes SHA-256 Chain
#                    of Custody, emits SUCCESS:<tar>:<coc> so the MCP tool
#                    pulls the evidence package back to V-AutoFor.
#
# State file (between calls): /tmp/.vautofor_capture.state
# ==============================================================================

CAPTURE_SECONDS=60    # 1 minute live PCAP capture (per operator request; default design was 300s)
STATE_FILE="/tmp/.vautofor_capture.state"

# Privilege escalation: when invoked as a non-root SSH user with SUDO_PASSWORD
# set (common on Kali/Ubuntu where root SSH login is blocked but the user is a
# sudoer), re-execute the ENTIRE script as root via 'sudo -S' (password on
# stdin). Grants tcpdump CAP_NET_RAW (needed for '-i any') and access to
# root-only artifacts (/etc/shadow, /root history, full ss process names).
if [ "$(id -u 2>/dev/null || echo 1000)" != "0" ] && [ -n "$SUDO_PASSWORD" ] && command -v sudo >/dev/null 2>&1; then
    printf '%s\n' "$SUDO_PASSWORD" | sudo -S sh "$0" 2>&1
    exit $?
fi

if [ -f "$STATE_FILE" ]; then
    # ======================================================================
    # PHASE B: FINISH  (second MCP call, ~5 minutes after capture start)
    # ======================================================================
    . "$STATE_FILE"

    # Wait for tcpdump to finish (up to 120s)
    i=0
    while [ $i -lt 120 ]; do
        if [ -n "$TCP_PID" ] && kill -0 "$TCP_PID" 2>/dev/null; then
            sleep 5
            i=$((i + 5))
        else
            break
        fi
    done
    # Still running? Force stop (pcap up to this point is still valid)
    if [ -n "$TCP_PID" ] && kill -0 "$TCP_PID" 2>/dev/null; then
        kill -9 "$TCP_PID" 2>/dev/null
    fi

    # Move pcap into the work tree if it was produced
    if [ -n "$PCAP_PATH" ] && [ -f "$PCAP_PATH" ]; then
        mv "$PCAP_PATH" "${WORK_DIR}/Network/live_traffic_${CAPTURE_SECONDS}s.pcap" 2>/dev/null
        echo "PCAP_OK $(stat -c %s "${WORK_DIR}/Network/live_traffic_${CAPTURE_SECONDS}s.pcap" 2>/dev/null || echo unknown) bytes"
    else
        echo "WARNING: PCAP NOT FOUND at ${PCAP_PATH} (PCAP_TOOL=${PCAP_TOOL:-unknown})"
    fi

    # 8. Archive and compute SHA-256 Chain of Custody
    tar -czf "${ARCHIVE_PATH}" -C /tmp "${EVIDENCE_NAME}" 2>/dev/null

    echo "=== V-AUTOFOR LINUX CHAIN OF CUSTODY ===" > "${COC_PATH}"
    echo "Hostname: ${HOSTNAME}" >> "${COC_PATH}"
    echo "Acquisition Timestamp: $(date 2>/dev/null)" >> "${COC_PATH}"
    echo "Capture window: ${CAPTURE_SECONDS}s live PCAP (started at phase A)" >> "${COC_PATH}"
    echo "Evidence Archive: ${ARCHIVE_PATH}" >> "${COC_PATH}"
    echo "Size (Bytes): $(wc -c < "${ARCHIVE_PATH}" 2>/dev/null)" >> "${COC_PATH}"
    echo "SHA-256 Hash:" >> "${COC_PATH}"
    sha256sum "${ARCHIVE_PATH}" >> "${COC_PATH}" 2>/dev/null || shasum -a 256 "${ARCHIVE_PATH}" >> "${COC_PATH}" 2>/dev/null

    # Clean up raw directory + state to save disk space on victim
    rm -rf "${WORK_DIR}" 2>/dev/null
    rm -f "${STATE_FILE}" 2>/dev/null

    echo "SUCCESS:${ARCHIVE_PATH}:${COC_PATH}"
else
    # ======================================================================
    # PHASE A: START  (first MCP call)
    # ======================================================================
    HOSTNAME=$(hostname 2>/dev/null || uname -n)
    TIMESTAMP=$(date +%Y%m%d_%H%M%S 2>/dev/null || date +%s)
    EVIDENCE_NAME="Linux_Triage_${HOSTNAME}_${TIMESTAMP}"
    WORK_DIR="/tmp/${EVIDENCE_NAME}"
    ARCHIVE_PATH="/tmp/${EVIDENCE_NAME}.tar.gz"
    COC_PATH="/tmp/Chain_of_Custody_${HOSTNAME}_${TIMESTAMP}.txt"
    PCAP_PATH="${WORK_DIR}/Network/live_traffic_${CAPTURE_SECONDS}s.pcap"

    mkdir -p "${WORK_DIR}/LiveState"
    mkdir -p "${WORK_DIR}/Logs"
    mkdir -p "${WORK_DIR}/Config_Users"
    mkdir -p "${WORK_DIR}/Network"

    # 1. System & Network Info
    uname -a > "${WORK_DIR}/LiveState/uname.txt" 2>&1
    uptime > "${WORK_DIR}/LiveState/uptime.txt" 2>&1
    ip addr > "${WORK_DIR}/LiveState/ip_addr.txt" 2>&1 || ifconfig -a > "${WORK_DIR}/LiveState/ip_addr.txt" 2>&1
    ip route > "${WORK_DIR}/LiveState/routes.txt" 2>&1 || route -n > "${WORK_DIR}/LiveState/routes.txt" 2>&1
    arp -an > "${WORK_DIR}/LiveState/arp_cache.txt" 2>&1 || ip neigh > "${WORK_DIR}/LiveState/arp_cache.txt" 2>&1

    # 2. Live Connections & Open Ports (RFC 3227 Volatile State)
    ss -antup > "${WORK_DIR}/LiveState/active_connections_ss.txt" 2>&1 || netstat -tlpn > "${WORK_DIR}/LiveState/active_connections_ss.txt" 2>&1
    lsof -n -P > "${WORK_DIR}/LiveState/lsof_open_files.txt" 2>&1

    # 3. Process Tree & Memory Artifacts
    ps auxf > "${WORK_DIR}/LiveState/process_tree.txt" 2>&1 || ps -ef > "${WORK_DIR}/LiveState/process_tree.txt" 2>&1
    lsmod > "${WORK_DIR}/LiveState/kernel_modules.txt" 2>&1

    # 4. Persistence (Crontabs, Systemd services)
    crontab -l > "${WORK_DIR}/LiveState/root_crontab.txt" 2>&1
    cp -r /etc/cron* "${WORK_DIR}/LiveState/" 2>/dev/null
    systemctl list-unit-files --state=enabled > "${WORK_DIR}/LiveState/enabled_services.txt" 2>&1

    # 5. Live PCAP Packet Capture (5 minutes, detached so this call returns fast)
    # Locate tcpdump explicitly: non-login/non-interactive SSH shells have a
    # minimal PATH that excludes /usr/sbin on Debian/Ubuntu/Kali, where
    # tcpdump lives. Probe common locations instead of trusting `command -v`.
    TCPDUMP_BIN=$(command -v tcpdump 2>/dev/null || true)
    if [ -z "$TCPDUMP_BIN" ]; then
        for _cand in /usr/sbin/tcpdump /sbin/tcpdump /usr/bin/tcpdump /bin/tcpdump; do
            if [ -x "$_cand" ]; then TCPDUMP_BIN="$_cand"; break; fi
        done
    fi
    TCP_PID=""
    TCPDUMP_BIN_USED=""
    if [ -n "$TCPDUMP_BIN" ]; then
        if command -v setsid >/dev/null 2>&1; then
            setsid nohup timeout ${CAPTURE_SECONDS} "$TCPDUMP_BIN" -i any -w "${PCAP_PATH}" >/dev/null 2>&1 &
        else
            nohup timeout ${CAPTURE_SECONDS} "$TCPDUMP_BIN" -i any -w "${PCAP_PATH}" >/dev/null 2>&1 &
        fi
        TCP_PID=$!
        TCPDUMP_BIN_USED="$TCPDUMP_BIN"
    else
        TCPDUMP_BIN_USED="MISSING"
    fi

    # 6. User Accounts, SSH Keys, Shell Histories
    cp -f /etc/passwd "${WORK_DIR}/Config_Users/" 2>/dev/null
    cp -f /etc/shadow "${WORK_DIR}/Config_Users/" 2>/dev/null
    cp -f /etc/group "${WORK_DIR}/Config_Users/" 2>/dev/null
    cp -f /etc/sudoers "${WORK_DIR}/Config_Users/" 2>/dev/null
    cp -f /etc/hosts "${WORK_DIR}/Config_Users/" 2>/dev/null

    # Shell histories for root & users
    mkdir -p "${WORK_DIR}/Config_Users/histories"
    cp -f /root/.*history "${WORK_DIR}/Config_Users/histories/root_history" 2>/dev/null
    cp -r /root/.ssh "${WORK_DIR}/Config_Users/root_ssh" 2>/dev/null

    for user_home in /home/*; do
        if [ -d "$user_home" ]; then
            u_name=$(basename "$user_home")
            cp -f "$user_home"/.*history "${WORK_DIR}/Config_Users/histories/${u_name}_history" 2>/dev/null
            cp -r "$user_home"/.ssh "${WORK_DIR}/Config_Users/${u_name}_ssh" 2>/dev/null
        fi
    done

    # 7. System & Auth Logs (auth.log, secure, syslog, messages, wtmp, btmp)
    cp -f /var/log/auth.log* "${WORK_DIR}/Logs/" 2>/dev/null
    cp -f /var/log/secure* "${WORK_DIR}/Logs/" 2>/dev/null
    cp -f /var/log/syslog* "${WORK_DIR}/Logs/" 2>/dev/null
    cp -f /var/log/messages* "${WORK_DIR}/Logs/" 2>/dev/null
    cp -f /var/log/wtmp* "${WORK_DIR}/Logs/" 2>/dev/null
    cp -f /var/log/btmp* "${WORK_DIR}/Logs/" 2>/dev/null
    cp -f /var/run/utmp "${WORK_DIR}/Logs/" 2>/dev/null

    # Login history summaries
    last -Faiwx > "${WORK_DIR}/Logs/last_logins.txt" 2>&1
    lastb -Faiwx > "${WORK_DIR}/Logs/failed_logins_lastb.txt" 2>&1
    who -a > "${WORK_DIR}/Logs/who_active.txt" 2>&1

    # Persist state for Phase B (second call)
    cat > "${STATE_FILE}" <<EOF
HOSTNAME=${HOSTNAME}
WORK_DIR=${WORK_DIR}
EVIDENCE_NAME=${EVIDENCE_NAME}
ARCHIVE_PATH=${ARCHIVE_PATH}
COC_PATH=${COC_PATH}
PCAP_PATH=${PCAP_PATH}
TCP_PID=${TCP_PID}
PCAP_TOOL=${TCPDUMP_BIN_USED}
EOF
    chmod 644 "${STATE_FILE}" 2>/dev/null

    echo "PHASE_START_COMPLETE pcap=${PCAP_PATH} pid=${TCP_PID} tool=${TCPDUMP_BIN_USED} duration=${CAPTURE_SECONDS}s"
fi
