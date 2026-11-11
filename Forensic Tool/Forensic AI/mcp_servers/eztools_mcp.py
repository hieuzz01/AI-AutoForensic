"""
Eric Zimmerman & Deep Forensic Artifacts MCP Server
Provides SANS FOR508 forensic artifact parsers (Amcache, Prefetch, Shimcache, MFT, EVTX,
Shellbags, LNK, Jumplists, SRUM), PE Static Analysis (pefile), and Linux Log Analysis.
All tool executions send live telemetry events to ForBrain.
"""

import os
import subprocess
import json
import time
import hashlib
from typing import List, Optional, Dict, Any
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("eztools")

BASE_DIR = r"E:\Hunting-Forensics\Forensic Tool\Get-ZimmermanTools"
TELEMETRY_URL = "http://127.0.0.1:5000/api/telemetry/event"
TELEMETRY_FILE = r"E:\Hunting-Forensics\Forensic Tool\ForBrain\telemetry_events.json"

def _report_telemetry(tool_name: str, target: str, params: dict, status: str, output: str, duration: float):
    event_data = {
        "id": f"evt_{int(time.time() * 1000)}",
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "caller": "V-AutoFor AI",
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

def _resolve_tool(tool_name: str) -> str:
    if not tool_name.lower().endswith(".exe"):
        tool_name += ".exe"
    # Search in root of Get-ZimmermanTools or subfolders
    direct = os.path.join(BASE_DIR, tool_name)
    if os.path.exists(direct):
        return direct
    for root, dirs, files in os.walk(BASE_DIR):
        for f in files:
            if f.lower() == tool_name.lower():
                return os.path.join(root, f)
    raise FileNotFoundError(f"Zimmerman tool '{tool_name}' not found under {BASE_DIR}")

def _execute(cmd: List[str], timeout: int = 300) -> str:
    try:
        proc = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            creationflags=subprocess.CREATE_NO_WINDOW if os.name == 'nt' else 0
        )
        out = proc.stdout.strip()
        err = proc.stderr.strip()
        result = []
        if out:
            result.append(out)
        if err and proc.returncode != 0:
            result.append(f"[STDERR]\n{err}")
        return "\n".join(result) if result else "Tool executed with return code 0."
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout} seconds."
    except Exception as e:
        return f"Error executing tool: {str(e)}"

# -------------------------------------------------------------
# EVIDENCE INTEGRITY & COMPANION METADATA
# -------------------------------------------------------------

@mcp.tool()
def verify_evidence_integrity(evidence_file: str, companion_txt_file: Optional[str] = None) -> str:
    """Computes MD5, SHA-1, and SHA-256 for an evidence file (.ad1, .E01, .raw, .pcap, .dmp)
    and verifies it against companion acquisition metadata (e.g. FirstHack.ad1.txt).
    """
    t0 = time.time()
    if not os.path.exists(evidence_file):
        res = f"Error: Evidence file '{evidence_file}' does not exist."
        _report_telemetry("verify_evidence_integrity", evidence_file, {}, "ERROR", res, time.time() - t0)
        return res

    h_md5 = hashlib.md5()
    h_sha1 = hashlib.sha1()
    h_sha256 = hashlib.sha256()
    size = 0

    with open(evidence_file, "rb") as f:
        while chunk := f.read(4 * 1024 * 1024):
            h_md5.update(chunk)
            h_sha1.update(chunk)
            h_sha256.update(chunk)
            size += len(chunk)

    md5_hex = h_md5.hexdigest()
    sha1_hex = h_sha1.hexdigest()
    sha256_hex = h_sha256.hexdigest()

    lines = [
        f"=== EVIDENCE INTEGRITY VERIFICATION (ISO/IEC 27037) ===",
        f"Target File: {evidence_file}",
        f"Size: {size:,} bytes ({size / (1024*1024):.2f} MB)",
        f"MD5:    {md5_hex}",
        f"SHA-1:  {sha1_hex}",
        f"SHA-256:{sha256_hex}",
    ]

    # Check companion txt file if provided or auto-detect
    txt_candidate = companion_txt_file or f"{evidence_file}.txt"
    if os.path.exists(txt_candidate):
        lines.append(f"\nCompanion Metadata Found: {txt_candidate}")
        with open(txt_candidate, "r", encoding="utf-8", errors="ignore") as f:
            txt_content = f.read()
        
        md5_match = "MATCH (VERIFIED)" if md5_hex.lower() in txt_content.lower() else "NO MATCH / NOT FOUND"
        sha1_match = "MATCH (VERIFIED)" if sha1_hex.lower() in txt_content.lower() else "NO MATCH / NOT FOUND"
        
        lines.append(f"- MD5 vs Metadata: {md5_match}")
        lines.append(f"- SHA-1 vs Metadata: {sha1_match}")
        lines.append("\n--- METADATA SNIPPET ---")
        lines.append(txt_content[:1500])

    res = "\n".join(lines)
    _report_telemetry("verify_evidence_integrity", evidence_file, {"companion": companion_txt_file}, "SUCCESS", res, time.time() - t0)
    return res

# -------------------------------------------------------------
# SANS FOR508 ZIMMERMAN TOOLS
# -------------------------------------------------------------

@mcp.tool()
def parse_prefetch(prefetch_path: str, output_csv_dir: str, extra_args: str = "") -> str:
    """Parses Windows Prefetch (.pf) files using PECmd.exe to discover Evidence of Execution."""
    t0 = time.time()
    try:
        tool_path = _resolve_tool("PECmd.exe")
        os.makedirs(output_csv_dir, exist_ok=True)
        cmd = [tool_path, "-d" if os.path.isdir(prefetch_path) else "-f", prefetch_path, "--csv", output_csv_dir, "-q"]
        if extra_args:
            cmd.extend(extra_args.split())
        res = _execute(cmd)
        status = "ERROR" if res.startswith("Error") else "SUCCESS"
        _report_telemetry("parse_prefetch", prefetch_path, {"output_csv": output_csv_dir}, status, res, time.time() - t0)
        return res
    except Exception as e:
        res = f"Error running PECmd: {str(e)}"
        _report_telemetry("parse_prefetch", prefetch_path, {}, "ERROR", res, time.time() - t0)
        return res

@mcp.tool()
def parse_amcache(amcache_path: str, output_csv_dir: str, extra_args: str = "") -> str:
    """Parses Amcache.hve using AmcacheParser.exe to uncover unexecuted or executed program SHA-1 hashes and first run times."""
    t0 = time.time()
    try:
        tool_path = _resolve_tool("AmcacheParser.exe")
        os.makedirs(output_csv_dir, exist_ok=True)
        cmd = [tool_path, "-f", amcache_path, "--csv", output_csv_dir]
        if extra_args:
            cmd.extend(extra_args.split())
        res = _execute(cmd)
        status = "ERROR" if res.startswith("Error") else "SUCCESS"
        _report_telemetry("parse_amcache", amcache_path, {"output_csv": output_csv_dir}, status, res, time.time() - t0)
        return res
    except Exception as e:
        res = f"Error running AmcacheParser: {str(e)}"
        _report_telemetry("parse_amcache", amcache_path, {}, "ERROR", res, time.time() - t0)
        return res

@mcp.tool()
def parse_shimcache(system_hive_path: str, output_csv_dir: str, extra_args: str = "") -> str:
    """Parses AppCompatCache (Shimcache) from a SYSTEM registry hive using AppCompatCacheParser.exe."""
    t0 = time.time()
    try:
        tool_path = _resolve_tool("AppCompatCacheParser.exe")
        os.makedirs(output_csv_dir, exist_ok=True)
        cmd = [tool_path, "-f", system_hive_path, "--csv", output_csv_dir]
        if extra_args:
            cmd.extend(extra_args.split())
        res = _execute(cmd)
        status = "ERROR" if res.startswith("Error") else "SUCCESS"
        _report_telemetry("parse_shimcache", system_hive_path, {"output_csv": output_csv_dir}, status, res, time.time() - t0)
        return res
    except Exception as e:
        res = f"Error running AppCompatCacheParser: {str(e)}"
        _report_telemetry("parse_shimcache", system_hive_path, {}, "ERROR", res, time.time() - t0)
        return res

@mcp.tool()
def parse_mft(mft_file: str, output_csv_dir: str, extra_args: str = "") -> str:
    """Parses an NTFS Master File Table ($MFT) using MFTECmd.exe to detect Timestomping and file creation/deletion."""
    t0 = time.time()
    try:
        tool_path = _resolve_tool("MFTECmd.exe")
        os.makedirs(output_csv_dir, exist_ok=True)
        cmd = [tool_path, "-f", mft_file, "--csv", output_csv_dir]
        if extra_args:
            cmd.extend(extra_args.split())
        res = _execute(cmd)
        status = "ERROR" if res.startswith("Error") else "SUCCESS"
        _report_telemetry("parse_mft", mft_file, {"output_csv": output_csv_dir}, status, res, time.time() - t0)
        return res
    except Exception as e:
        res = f"Error running MFTECmd: {str(e)}"
        _report_telemetry("parse_mft", mft_file, {}, "ERROR", res, time.time() - t0)
        return res

@mcp.tool()
def parse_evtx(evtx_path: str, output_csv_dir: str, extra_args: str = "") -> str:
    """Parses Windows Event Logs (.evtx) using EvtxECmd.exe and exports to structured CSV."""
    t0 = time.time()
    try:
        tool_path = _resolve_tool("EvtxECmd.exe")
        os.makedirs(output_csv_dir, exist_ok=True)
        cmd = [tool_path, "-d" if os.path.isdir(evtx_path) else "-f", evtx_path, "--csv", output_csv_dir]
        if extra_args:
            cmd.extend(extra_args.split())
        res = _execute(cmd)
        status = "ERROR" if res.startswith("Error") else "SUCCESS"
        _report_telemetry("parse_evtx", evtx_path, {"output_csv": output_csv_dir}, status, res, time.time() - t0)
        return res
    except Exception as e:
        res = f"Error running EvtxECmd: {str(e)}"
        _report_telemetry("parse_evtx", evtx_path, {}, "ERROR", res, time.time() - t0)
        return res

@mcp.tool()
def parse_shellbags(hive_path: str, output_csv_dir: str) -> str:
    """Parses Windows Explorer Shellbags from UsrClass.dat or NTUSER.DAT using SBECmd.exe to discover user folder traversal."""
    t0 = time.time()
    try:
        tool_path = _resolve_tool("SBECmd.exe")
        os.makedirs(output_csv_dir, exist_ok=True)
        cmd = [tool_path, "-d" if os.path.isdir(hive_path) else "-f", hive_path, "--csv", output_csv_dir]
        res = _execute(cmd)
        status = "ERROR" if res.startswith("Error") else "SUCCESS"
        _report_telemetry("parse_shellbags", hive_path, {"output_csv": output_csv_dir}, status, res, time.time() - t0)
        return res
    except Exception as e:
        res = f"Error running SBECmd: {str(e)}"
        _report_telemetry("parse_shellbags", hive_path, {}, "ERROR", res, time.time() - t0)
        return res

@mcp.tool()
def parse_lnk(lnk_path: str, output_csv_dir: str) -> str:
    """Parses Windows Shortcut (.lnk) files using LECmd.exe to identify target paths, volumes, and MAC addresses."""
    t0 = time.time()
    try:
        tool_path = _resolve_tool("LECmd.exe")
        os.makedirs(output_csv_dir, exist_ok=True)
        cmd = [tool_path, "-d" if os.path.isdir(lnk_path) else "-f", lnk_path, "--csv", output_csv_dir]
        res = _execute(cmd)
        status = "ERROR" if res.startswith("Error") else "SUCCESS"
        _report_telemetry("parse_lnk", lnk_path, {"output_csv": output_csv_dir}, status, res, time.time() - t0)
        return res
    except Exception as e:
        res = f"Error running LECmd: {str(e)}"
        _report_telemetry("parse_lnk", lnk_path, {}, "ERROR", res, time.time() - t0)
        return res

@mcp.tool()
def parse_jumplists(jumplist_path: str, output_csv_dir: str) -> str:
    """Parses AutomaticDestinations-ms / CustomDestinations-ms using JLECmd.exe."""
    t0 = time.time()
    try:
        tool_path = _resolve_tool("JLECmd.exe")
        os.makedirs(output_csv_dir, exist_ok=True)
        cmd = [tool_path, "-d" if os.path.isdir(jumplist_path) else "-f", jumplist_path, "--csv", output_csv_dir]
        res = _execute(cmd)
        status = "ERROR" if res.startswith("Error") else "SUCCESS"
        _report_telemetry("parse_jumplists", jumplist_path, {"output_csv": output_csv_dir}, status, res, time.time() - t0)
        return res
    except Exception as e:
        res = f"Error running JLECmd: {str(e)}"
        _report_telemetry("parse_jumplists", jumplist_path, {}, "ERROR", res, time.time() - t0)
        return res

@mcp.tool()
def parse_srum(srudb_path: str, software_hive: Optional[str], output_csv_dir: str) -> str:
    """Parses System Resource Usage Monitor (SRUDB.dat) using SrumECmd.exe for 30-day process execution and network usage."""
    t0 = time.time()
    try:
        tool_path = _resolve_tool("SrumECmd.exe")
        os.makedirs(output_csv_dir, exist_ok=True)
        cmd = [tool_path, "-f", srudb_path, "--csv", output_csv_dir]
        if software_hive and os.path.exists(software_hive):
            cmd.extend(["-r", software_hive])
        res = _execute(cmd)
        status = "ERROR" if res.startswith("Error") else "SUCCESS"
        _report_telemetry("parse_srum", srudb_path, {"output_csv": output_csv_dir}, status, res, time.time() - t0)
        return res
    except Exception as e:
        res = f"Error running SrumECmd: {str(e)}"
        _report_telemetry("parse_srum", srudb_path, {}, "ERROR", res, time.time() - t0)
        return res

# -------------------------------------------------------------
# PE FILE & STATIC MALWARE ANALYSIS (pefile)
# -------------------------------------------------------------

@mcp.tool()
def pe_analyze(pe_path: str) -> str:
    """Performs deep static analysis on a Portable Executable (.exe, .dll, .sys) using pefile.
    Calculates compile timestamps, section entropy (UPX/packer detection), imphash, and suspicious API imports.
    """
    t0 = time.time()
    if not os.path.exists(pe_path):
        res = f"Error: PE file '{pe_path}' does not exist."
        _report_telemetry("pe_analyze", pe_path, {}, "ERROR", res, time.time() - t0)
        return res

    try:
        import pefile
        pe = pefile.PE(pe_path)
        out = []
        out.append(f"=== PE STATIC FORENSIC ANALYSIS: {os.path.basename(pe_path)} ===")
        out.append(f"Full Path: {pe_path}")
        out.append(f"Machine Type: {hex(pe.FILE_HEADER.Machine)}")
        out.append(f"Compile Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.gmtime(pe.FILE_HEADER.TimeDateStamp))}")
        out.append(f"Number of Sections: {pe.FILE_HEADER.NumberOfSections}")
        
        # Imphash
        if hasattr(pe, "get_imphash"):
            out.append(f"Import Hash (imphash): {pe.get_imphash()}")

        # Sections & Entropy
        out.append("\n--- SECTION ANALYSIS & ENTROPY ---")
        suspicious_entropy = False
        for s in pe.sections:
            name = s.Name.decode('utf-8', 'ignore').strip('\x00')
            entropy = s.get_entropy()
            is_high = " [HIGH ENTROPY - PACKED/ENCRYPTED!]" if entropy > 7.1 else ""
            if entropy > 7.1:
                suspicious_entropy = True
            out.append(f"- Section '{name}': Size={s.SizeOfRawData:,} bytes, Entropy={entropy:.2f}{is_high}")

        # Suspicious APIs
        SUSPICIOUS_APIS = {
            "VirtualAlloc", "VirtualAllocEx", "VirtualProtect", "WriteProcessMemory",
            "CreateRemoteThread", "QueueUserAPC", "SetWindowsHookEx", "IsDebuggerPresent",
            "CheckRemoteDebuggerPresent", "InternetOpenUrl", "HttpSendRequest", "URLDownloadToFile",
            "WinExec", "ShellExecute", "CryptEncrypt", "CryptDecrypt"
        }
        found_apis = []
        if hasattr(pe, "DIRECTORY_ENTRY_IMPORT"):
            out.append("\n--- SUSPICIOUS API IMPORTS ---")
            for entry in pe.DIRECTORY_ENTRY_IMPORT:
                dll_name = entry.dll.decode('utf-8', 'ignore')
                for imp in entry.imports:
                    if imp.name:
                        func_name = imp.name.decode('utf-8', 'ignore')
                        if func_name in SUSPICIOUS_APIS:
                            found_apis.append(f"{dll_name}!{func_name}")

        if found_apis:
            out.append("Detected Sensitive/Malicious APIs:")
            for a in found_apis:
                out.append(f"  * {a}")
        else:
            out.append("No common injection/C2 APIs directly in static import table.")

        res = "\n".join(out)
        _report_telemetry("pe_analyze", pe_path, {"entropy_alert": suspicious_entropy, "api_count": len(found_apis)}, "SUCCESS", res, time.time() - t0)
        return res
    except Exception as e:
        res = f"Error parsing PE with pefile: {str(e)}"
        _report_telemetry("pe_analyze", pe_path, {}, "ERROR", res, time.time() - t0)
        return res

# -------------------------------------------------------------
# LINUX LOG & COMMAND HISTORY FORENSIC ANALYZER
# -------------------------------------------------------------

@mcp.tool()
def analyze_linux_logs(target_path: str, log_type: str = "auto") -> str:
    """Analyzes Linux forensic logs (auth.log, syslog, .bash_history, crontab).
    Automatically detects SSH Brute-Force, successful logins, sudo privilege escalations,
    reconnaissance, download tools (curl/wget), reverse shells, and anti-forensics commands.
    """
    t0 = time.time()
    if not os.path.exists(target_path):
        res = f"Error: Target path '{target_path}' does not exist."
        _report_telemetry("analyze_linux_logs", target_path, {}, "ERROR", res, time.time() - t0)
        return res

    out = []
    out.append(f"=== LINUX LOG FORENSIC TRIAGE: {os.path.basename(target_path)} ===")

    # Determine files to inspect
    files_to_check = []
    if os.path.isdir(target_path):
        for root, dirs, files in os.walk(target_path):
            for f in files:
                files_to_check.append(os.path.join(root, f))
    else:
        files_to_check.append(target_path)

    ssh_fails: Dict[str, int] = {}
    ssh_success: List[str] = []
    sudo_events: List[str] = []
    suspicious_bash: List[str] = []

    BASH_PATTERNS = [
        "wget", "curl", "nc ", "netcat", "python -c", "perl -e", "bash -i", "/dev/tcp",
        "chmod +x", "chattr", "useradd", "usermod", "visudo", "history -c", "shred",
        "rm -rf /var/log", "/etc/crontab", "crontab -e", "base64", "socat"
    ]

    for fpath in files_to_check:
        fname = os.path.basename(fpath).lower()
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.readlines()
        except Exception:
            continue

        if "auth.log" in fname or "secure" in fname:
            out.append(f"\n[Artifact: {fname} ({len(content)} lines)]")
            for line in content:
                line_str = line.strip()
                if "Failed password for" in line_str:
                    parts = line_str.split("from")
                    if len(parts) > 1:
                        ip = parts[1].split()[0]
                        ssh_fails[ip] = ssh_fails.get(ip, 0) + 1
                elif "Accepted password for" in line_str or "Accepted publickey for" in line_str:
                    ssh_success.append(line_str)
                elif "sudo:" in line_str and "COMMAND=" in line_str:
                    sudo_events.append(line_str)

        elif "bash_history" in fname:
            out.append(f"\n[Artifact: {fname} ({len(content)} commands)]")
            for line in content:
                cmd = line.strip()
                if any(p in cmd.lower() for p in BASH_PATTERNS):
                    suspicious_bash.append(cmd)

    # Summarize Findings
    if ssh_fails:
        out.append("\n--- SSH BRUTE-FORCE DETECTED ---")
        for ip, count in sorted(ssh_fails.items(), key=lambda x: x[1], reverse=True)[:10]:
            out.append(f"- IP {ip}: {count} failed logon attempts")

    if ssh_success:
        out.append("\n--- SUCCESSFUL LOGONS (INITIAL ACCESS) ---")
        for s in ssh_success[:10]:
            out.append(f"* {s}")

    if sudo_events:
        out.append("\n--- SUDO PRIVILEGE ESCALATION ---")
        for ev in sudo_events[:10]:
            out.append(f"* {ev}")

    if suspicious_bash:
        out.append("\n--- SUSPICIOUS COMMANDS IN BASH HISTORY ---")
        for b in suspicious_bash[:20]:
            out.append(f"  > {b}")

    if not ssh_fails and not ssh_success and not suspicious_bash:
        out.append("No immediate obvious brute-force or malicious keywords found in examined logs.")

    res = "\n".join(out)
    _report_telemetry("analyze_linux_logs", target_path, {"ssh_fails": len(ssh_fails), "suspicious_cmds": len(suspicious_bash)}, "SUCCESS", res, time.time() - t0)
    return res

if __name__ == "__main__":
    mcp.run()
