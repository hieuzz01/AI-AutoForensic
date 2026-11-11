"""
V-AutoFor Universal Cross-Platform Remote Triage MCP Server
Supports zero-footprint Agentless Acquisition for both Windows and Linux targets.
Auto-detects OS:
  - Linux: Executes collect_linux_triage.sh over SSH (Port 22) and PULLS files back via SFTP/SCP.
           (Requires only Port 22 open on the target machine!).
  - Windows: Executes Run_Full_Triage_Remote.bat via WinRM/SMB (Port 5985/445).
"""

import os
import subprocess
import json
import time
import socket
from typing import Optional, Dict, Any, List
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("vautofor-remote-triage")

BASE_DIR = r"E:\Hunting-Forensics\Network-Share-Triage"
LINUX_DIR = os.path.join(BASE_DIR, "Linux_Triage")
SCRIPTS_DIR = os.path.join(BASE_DIR, "Scripts")
EVIDENCE_DIR = r"E:\Hunting-Forensics\Evidence"
TELEMETRY_URL = "http://127.0.0.1:5000/api/telemetry/event"
TELEMETRY_FILE = r"E:\Hunting-Forensics\Forensic Tool\ForBrain\telemetry_events.json"

def _report_telemetry(tool_name: str, target: str, params: dict, status: str, output: str, duration: float):
    event_data = {
        "id": f"evt_{int(time.time() * 1000)}",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "caller": "Agent 02 (Acquisition)",
        "tool": tool_name,
        "target": target,
        "params": params,
        "status": status,
        "duration": round(duration, 3),
        "output_preview": output[:3000]
    }
    try:
        import urllib.request
        req = urllib.request.Request(
            TELEMETRY_URL,
            data=json.dumps(event_data).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=0.6)
        return
    except Exception:
        pass

    try:
        events = []
        if os.path.exists(TELEMETRY_FILE):
            with open(TELEMETRY_FILE, "r", encoding="utf-8") as f:
                events = json.load(f)
        events.insert(0, event_data)
        with open(TELEMETRY_FILE, "w", encoding="utf-8") as f:
            json.dump(events[:100], f, indent=2, ensure_ascii=False)
    except Exception:
        pass

def _get_local_ip() -> str:
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"

def _check_port_open(host: str, port: int, timeout: float = 1.5) -> bool:
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(timeout)
        result = sock.connect_ex((host, port))
        sock.close()
        return result == 0
    except Exception:
        return False

@mcp.tool()
def detect_target_os_and_ports(target_ip: str) -> str:
    """
    Scans the target IP to determine its Operating System (Windows vs Linux)
    and verifies active management ports (Port 22 SSH for Linux, Port 5985 WinRM / 445 SMB for Windows).
    """
    t_start = time.time()
    ssh_open = _check_port_open(target_ip, 22)
    winrm_open = _check_port_open(target_ip, 5985)
    winrm_ssl_open = _check_port_open(target_ip, 5986)
    smb_open = _check_port_open(target_ip, 445)
    rdp_open = _check_port_open(target_ip, 3389)

    detected_os = "Unknown"
    confidence = "Low"
    recommended_mode = ""

    if ssh_open and not (winrm_open or smb_open or rdp_open):
        detected_os = "Linux / Unix"
        confidence = "High"
        recommended_mode = "ssh_pull (Only Port 22 required on destination)"
    elif (winrm_open or smb_open or rdp_open) and not ssh_open:
        detected_os = "Windows"
        confidence = "High"
        recommended_mode = "winrm_smb (Port 5985 or 445 on destination)"
    elif ssh_open and (winrm_open or smb_open):
        detected_os = "Dual/Multi-Port (Likely Windows with OpenSSH or Linux with Samba)"
        confidence = "Medium"
        recommended_mode = "ssh_pull if Linux, winrm_smb if Windows"

    res = {
        "target_ip": target_ip,
        "detected_os": detected_os,
        "confidence": confidence,
        "recommended_acquisition": recommended_mode,
        "ports_status": {
            "22/SSH (Linux)": "OPEN" if ssh_open else "CLOSED",
            "5985/WinRM-HTTP (Windows)": "OPEN" if winrm_open else "CLOSED",
            "5986/WinRM-HTTPS (Windows)": "OPEN" if winrm_ssl_open else "CLOSED",
            "445/SMB (Windows)": "OPEN" if smb_open else "CLOSED",
            "3389/RDP (Windows)": "OPEN" if rdp_open else "CLOSED"
        }
    }
    duration = time.time() - t_start
    output = json.dumps(res, indent=2)
    _report_telemetry("detect_target_os_and_ports", target_ip, {}, "SUCCESS", output, duration)
    return output

@mcp.tool()
def pull_linux_evidence(
    target_ip: str,
    target_user: str = "root",
    target_password: str = "",
    sudo_password: str = "",
    ssh_key_path: str = "",
    target_port: int = 22,
    timeout_seconds: int = 300
) -> str:
    """
    AGENTLESS LINUX ACQUISITION (PULL METHOD):
    Connects to target Linux host over SSH (Port 22 only!), executes collect_linux_triage.sh,
    and PULLS the resulting evidence package (.tar.gz) and Chain of Custody hash back to V-AutoFor.
    No ports need to be opened on the V-AutoFor host! Only Port 22 on the target machine!

    sudo_password: optional. When set and the SSH user is non-root, the collector
    re-executes itself as root via 'sudo -S' (password on stdin). Needed on
    Debian/Ubuntu/Kali targets where root SSH login is blocked but the SSH user
    is a sudoer; grants tcpdump CAP_NET_RAW and root-only artifacts.
    """
    t_start = time.time()
    try:
        import paramiko
    except ImportError:
        return json.dumps({"status": "ERROR", "message": "paramiko library missing"}, indent=2)

    script_path = os.path.join(LINUX_DIR, "collect_linux_triage.sh")
    if not os.path.exists(script_path):
        return json.dumps({"status": "ERROR", "message": f"Script not found at {script_path}"}, indent=2)

    with open(script_path, "r", encoding="utf-8") as f:
        script_content = f.read().replace("\r\n", "\n")

    dest_folder = os.path.join(EVIDENCE_DIR, f"{target_ip}_Linux_{time.strftime('%Y%m%d_%H%M%S')}")
    os.makedirs(dest_folder, exist_ok=True)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        connect_kwargs = {
            "hostname": target_ip,
            "port": target_port,
            "username": target_user,
            "timeout": 15
        }
        if ssh_key_path and os.path.exists(ssh_key_path):
            connect_kwargs["key_filename"] = ssh_key_path
        elif target_password:
            connect_kwargs["password"] = target_password

        client.connect(**connect_kwargs)

        # 1. Upload collector script to /tmp/
        sftp = client.open_sftp()
        remote_script = "/tmp/collect_linux_triage.sh"
        with sftp.file(remote_script, "w") as rf:
            rf.write(script_content)
        sftp.chmod(remote_script, 0o755)

        # 2. Execute script remotely (SUDO_PASSWORD exported so the script can
        #    re-exec as root via 'sudo -S' when the SSH user is a non-root sudoer).
        exec_cmd = f"sh {remote_script}"
        exec_env = {}
        if sudo_password:
            exec_cmd = f"SUDO_PASSWORD={sudo_password} {exec_cmd}"
        stdin, stdout, stderr = client.exec_command(exec_cmd, timeout=timeout_seconds)
        output_lines = stdout.read().decode("utf-8", errors="ignore")
        err_lines = stderr.read().decode("utf-8", errors="ignore")

        # Parse output for tar.gz and coc path
        tar_remote_path = ""
        coc_remote_path = ""
        for line in output_lines.splitlines():
            if line.startswith("SUCCESS:"):
                parts = line.strip().split(":")
                if len(parts) >= 3:
                    tar_remote_path = parts[1]
                    coc_remote_path = parts[2]

        pulled_files = []
        coc_content = ""

        # 3. Pull evidence back via SFTP
        if tar_remote_path:
            local_tar = os.path.join(dest_folder, os.path.basename(tar_remote_path))
            sftp.get(tar_remote_path, local_tar)
            pulled_files.append(os.path.basename(tar_remote_path))
            try:
                sftp.remove(tar_remote_path)
            except Exception:
                pass

        if coc_remote_path:
            local_coc = os.path.join(dest_folder, os.path.basename(coc_remote_path))
            sftp.get(coc_remote_path, local_coc)
            pulled_files.append(os.path.basename(coc_remote_path))
            if os.path.exists(local_coc):
                with open(local_coc, "r", encoding="utf-8", errors="ignore") as cf:
                    coc_content = cf.read()
            try:
                sftp.remove(coc_remote_path)
            except Exception:
                pass

        try:
            sftp.remove(remote_script)
        except Exception:
            pass

        sftp.close()
        client.close()

        status_str = "SUCCESS" if pulled_files else "FAILED"
        result = {
            "status": status_str,
            "target_ip": target_ip,
            "os_type": "Linux",
            "protocol": "SSH / SFTP (Port 22)",
            "evidence_directory": dest_folder,
            "pulled_files": pulled_files,
            "chain_of_custody": coc_content.strip(),
            "remote_stdout_snippet": output_lines[-1000:],
            "remote_stderr_snippet": err_lines[-500:] if err_lines else ""
        }
        duration = time.time() - t_start
        out_json = json.dumps(result, indent=2)
        _report_telemetry("pull_linux_evidence", target_ip, {"user": target_user}, status_str, out_json, duration)
        return out_json

    except Exception as e:
        client.close()
        err_res = {
            "status": "ERROR",
            "target_ip": target_ip,
            "error_message": str(e)
        }
        duration = time.time() - t_start
        out_json = json.dumps(err_res, indent=2)
        _report_telemetry("pull_linux_evidence", target_ip, {"user": target_user}, "ERROR", out_json, duration)
        return out_json

def wait_for_linux_capture(
    target_ip: str,
    target_user: str = "root",
    target_password: str = "",
    ssh_key_path: str = "",
    target_port: int = 22,
    poll_seconds: int = 280
) -> str:
    """
    PHASE B of agentless Linux acquisition (two-phase capture):
    Waits for the background tcpdump started by pull_linux_evidence to finish,
    then archives, hashes (SHA-256 CoC), and PULLS the evidence package back
    via SFTP. Use pull_linux_evidence first (PHASE A: volatile state + start
    capture), then call this tool once or twice. Returns SUCCESS when the
    package is pulled.
    """
    t_start = time.time()
    try:
        import paramiko
    except ImportError:
        return json.dumps({"status": "ERROR", "message": "paramiko library missing"}, indent=2)

    dest_folder = os.path.join(EVIDENCE_DIR, f"{target_ip}_Linux_{time.strftime('%Y%m%d_%H%M%S')}")
    os.makedirs(dest_folder, exist_ok=True)

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        connect_kwargs = {
            "hostname": target_ip,
            "port": target_port,
            "username": target_user,
            "timeout": 15
        }
        if ssh_key_path and os.path.exists(ssh_key_path):
            connect_kwargs["key_filename"] = ssh_key_path
        elif target_password:
            connect_kwargs["password"] = target_password

        client.connect(**connect_kwargs)

        sftp = client.open_sftp()

        # Read state file produced by PHASE A
        state_path = "/tmp/.vautofor_capture.state"
        try:
            with sftp.open(state_path, "r") as sf:
                state_content = sf.read().decode("utf-8", errors="ignore")
        except IOError:
            sftp.close()
            client.close()
            return json.dumps({
                "status": "ERROR",
                "target_ip": target_ip,
                "error_message": "No capture state found on target. Run pull_linux_evidence (PHASE A) first."
            }, indent=2)

        if "ARCHIVE_PATH=" not in state_content:
            sftp.close()
            client.close()
            return json.dumps({
                "status": "ERROR",
                "target_ip": target_ip,
                "error_message": f"Malformed capture state on target: {state_content[:200]}"
            }, indent=2)

        # Poll loop (each SSH command well under the 300s MCP call cap)
        stdout_tail = ""
        deadline = time.time() + max(1, min(poll_seconds, 285))
        while True:
            cmd = 'sh /tmp/collect_linux_triage.sh 2>&1 | tail -n 10'
            stdin, stdout, stderr = client.exec_command(cmd, timeout=295)
            stdout_tail = stdout.read().decode("utf-8", errors="ignore")
            success_line = ""
            for line in stdout_tail.splitlines():
                if line.startswith("SUCCESS:"):
                    success_line = line.strip()
            if success_line:
                break
            if time.time() >= deadline:
                break
            time.sleep(15)

        tar_remote_path = ""
        coc_remote_path = ""
        for line in stdout_tail.splitlines():
            if line.startswith("SUCCESS:"):
                parts = line.strip().split(":")
                if len(parts) >= 3:
                    tar_remote_path = parts[1]
                    coc_remote_path = parts[2]
                    break

        pulled_files = []
        coc_content = ""

        if tar_remote_path:
            local_tar = os.path.join(dest_folder, os.path.basename(tar_remote_path))
            sftp.get(tar_remote_path, local_tar)
            pulled_files.append(os.path.basename(tar_remote_path))
            try:
                sftp.remove(tar_remote_path)
            except Exception:
                pass

        if coc_remote_path:
            local_coc = os.path.join(dest_folder, os.path.basename(coc_remote_path))
            sftp.get(coc_remote_path, local_coc)
            pulled_files.append(os.path.basename(coc_remote_path))
            if os.path.exists(local_coc):
                with open(local_coc, "r", encoding="utf-8", errors="ignore") as cf:
                    coc_content = cf.read()
            try:
                sftp.remove(coc_remote_path)
            except Exception:
                pass

        sftp.close()
        client.close()

        status_str = "SUCCESS" if pulled_files else "PENDING"
        result = {
            "status": status_str,
            "target_ip": target_ip,
            "os_type": "Linux",
            "protocol": "SSH / SFTP (Port 22)",
            "evidence_directory": dest_folder,
            "pulled_files": pulled_files,
            "chain_of_custody": coc_content.strip(),
            "remote_stdout_snippet": stdout_tail[-1000:]
        }
        if status_str == "PENDING":
            result["message"] = "Capture not finished in this poll window. Call wait_for_linux_capture again."
        duration = time.time() - t_start
        out_json = json.dumps(result, indent=2)
        _report_telemetry("wait_for_linux_capture", target_ip, {"user": target_user}, status_str, out_json, duration)
        return out_json

    except Exception as e:
        client.close()
        err_res = {
            "status": "ERROR",
            "target_ip": target_ip,
            "error_message": str(e)
        }
        duration = time.time() - t_start
        out_json = json.dumps(err_res, indent=2)
        _report_telemetry("wait_for_linux_capture", target_ip, {"user": target_user}, "ERROR", out_json, duration)
        return out_json

@mcp.tool()
def trigger_universal_remote_triage(
    target_ip: str,
    target_user: str = "",
    target_password: str = "",
    ssh_key_path: str = "",
    force_os: str = "auto"
) -> str:
    """
    UNIVERSAL AGENTLESS ACQUISITION (Windows & Linux):
    Automatically detects whether the target host is Linux or Windows:
      - If Linux: Executes triage and PULLS files back via SSH/SFTP (Only Port 22 required!).
      - If Windows: Dispatches Windows Triage via WinRM/SMB.
    
    force_os: 'auto' (detect automatically), 'linux', or 'windows'.
    """
    os_target = force_os.lower()
    if os_target == "auto":
        ssh_open = _check_port_open(target_ip, 22)
        winrm_open = _check_port_open(target_ip, 5985)
        smb_open = _check_port_open(target_ip, 445)
        if ssh_open and not (winrm_open or smb_open):
            os_target = "linux"
        else:
            os_target = "windows"

    if os_target == "linux":
        user = target_user if target_user else "root"
        return pull_linux_evidence(
            target_ip=target_ip,
            target_user=user,
            target_password=target_password,
            ssh_key_path=ssh_key_path
        )
    else:
        return trigger_remote_triage(
            target_ip=target_ip,
            target_user=target_user,
            target_password=target_password,
            acquisition_mode="full"
        )

@mcp.tool()
def check_network_share_status() -> str:
    """
    Checks the status of the local SMB shares (ForensicTools and Evidence) on the V-AutoFor host.
    Verifies that portable binaries exist for both Windows and Linux.
    """
    t_start = time.time()
    local_ip = _get_local_ip()
    share_proc = subprocess.run("net share", capture_output=True, text=True, shell=True)
    has_tools_share = "ForensicTools" in share_proc.stdout
    has_evidence_share = "Evidence" in share_proc.stdout

    tools_inventory = {
        "Windows_RAM_WinPmem": os.path.exists(os.path.join(BASE_DIR, "1_RAM", "winpmem_mini_x64.exe")),
        "Windows_Network_RawCap": os.path.exists(os.path.join(BASE_DIR, "2_Network", "RawCap.exe")),
        "Windows_LiveState_Sysinternals": os.path.exists(os.path.join(BASE_DIR, "3_LiveState", "autorunsc64.exe")),
        "Windows_Artifacts_CyLR": os.path.exists(os.path.join(BASE_DIR, "4_Artifacts", "CyLR.exe")),
        "Linux_Triage_Script": os.path.exists(os.path.join(LINUX_DIR, "collect_linux_triage.sh")),
        "Linux_Artifacts_CyLR": os.path.exists(os.path.join(LINUX_DIR, "CyLR")),
        "Linux_Artifacts_UAC": os.path.exists(os.path.join(LINUX_DIR, "uac-3.4.0.tar.gz"))
    }

    status = {
        "vautofor_host_ip": local_ip,
        "shares": {
            "ForensicTools": {"active": has_tools_share, "unc_path": f"\\\\{local_ip}\\ForensicTools"},
            "Evidence": {"active": has_evidence_share, "unc_path": f"\\\\{local_ip}\\Evidence"}
        },
        "tools_inventory": tools_inventory,
        "readiness": "READY"
    }
    duration = time.time() - t_start
    output = json.dumps(status, indent=2)
    _report_telemetry("check_network_share_status", local_ip, {}, "SUCCESS", output, duration)
    return output

@mcp.tool()
def trigger_remote_triage(
    target_ip: str,
    target_user: str = "",
    target_password: str = "",
    acquisition_mode: str = "full",
    timeout_seconds: int = 600
) -> str:
    """
    Agent 02 Remote Acquisition for WINDOWS targets.
    """
    t_start = time.time()
    local_ip = _get_local_ip()
    before_folders = set(os.listdir(EVIDENCE_DIR)) if os.path.exists(EVIDENCE_DIR) else set()
    remote_bat = f"\\\\{local_ip}\\ForensicTools\\Scripts\\Run_Full_Triage_Remote.bat \\\\{local_ip}"
    
    if target_user and target_password:
        cred_block = f"""
$secPass = ConvertTo-SecureString '{target_password}' -AsPlainText -Force
$cred = New-Object System.Management.Automation.PSCredential ('{target_user}', $secPass)
Invoke-Command -ComputerName '{target_ip}' -Credential $cred -ScriptBlock {{ & '{remote_bat}' }}
"""
    else:
        cred_block = f"""
Invoke-Command -ComputerName '{target_ip}' -ScriptBlock {{ & '{remote_bat}' }}
"""

    ps_cmd = ["powershell", "-NoProfile", "-NonInteractive", "-Command", cred_block]
    try:
        proc = subprocess.run(ps_cmd, capture_output=True, text=True, timeout=timeout_seconds)
        stdout = proc.stdout
        stderr = proc.stderr
        exit_code = proc.returncode
    except subprocess.TimeoutExpired:
        stdout = ""
        stderr = f"Remote acquisition timed out after {timeout_seconds} seconds."
        exit_code = -1

    time.sleep(2)
    after_folders = set(os.listdir(EVIDENCE_DIR)) if os.path.exists(EVIDENCE_DIR) else set()
    new_dirs = list(after_folders - before_folders)
    evidence_path = ""
    collected_files = []
    coc_content = ""

    if new_dirs:
        evidence_path = os.path.join(EVIDENCE_DIR, new_dirs[0])
        if os.path.isdir(evidence_path):
            collected_files = os.listdir(evidence_path)
            coc_file = os.path.join(evidence_path, "Chain_of_Custody.txt")
            if os.path.exists(coc_file):
                with open(coc_file, "r", encoding="utf-8", errors="ignore") as f:
                    coc_content = f.read()

    status_str = "SUCCESS" if (new_dirs and collected_files) else "WARNING"
    result = {
        "status": status_str,
        "target_ip": target_ip,
        "os_type": "Windows",
        "acquisition_mode": acquisition_mode,
        "exit_code": exit_code,
        "evidence_folder": evidence_path,
        "collected_files": collected_files,
        "chain_of_custody": coc_content[:1000] if coc_content else "Pending verification"
    }
    duration = time.time() - t_start
    output = json.dumps(result, indent=2)
    _report_telemetry("trigger_remote_triage", target_ip, {"mode": acquisition_mode}, status_str, output, duration)
    return output

if __name__ == "__main__":
    mcp.run()
