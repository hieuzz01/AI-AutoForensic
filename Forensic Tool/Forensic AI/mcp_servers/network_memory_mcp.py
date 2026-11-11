"""
Network & Memory Forensics MCP Server
Exposes Volatility 3, MemProcFS, TShark, and AD1 capabilities to V-AutoFor via FastMCP.
Sends live telemetry of all tool calls and target files to ForBrain.
"""

import os
import subprocess
import json
import time
import functools
import urllib.request
from typing import List, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("network-memory-tools")

VOL_BIN = r"E:\Hunting-Forensics\Forensic Tool\Forensic AI\AIFT\.venv\Scripts\vol.exe"
TSHARK_BIN = r"C:\Program Files\Wireshark\tshark.exe"
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
    # 1. Try POST to ForBrain API
    try:
        req = urllib.request.Request(
            TELEMETRY_URL,
            data=json.dumps(event_data).encode("utf-8"),
            headers={"Content-Type": "application/json"}
        )
        urllib.request.urlopen(req, timeout=0.6)
        return
    except Exception:
        pass

    # 2. Fallback direct file append
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
        return "\n".join(result) if result else "Command executed successfully with no output."
    except subprocess.TimeoutExpired:
        return f"Error: Command timed out after {timeout} seconds."
    except Exception as e:
        return f"Error executing command: {str(e)}"

# -------------------------------------------------------------
# MEMORY FORENSICS (VOLATILITY 3 & MEMPROCFS)
# -------------------------------------------------------------

@mcp.tool()
def volatility_pslist(memory_file: str) -> str:
    """Lists running processes from a memory dump (.dmp, .raw, .vmem) using Volatility 3 windows.pslist."""
    t0 = time.time()
    if not os.path.exists(memory_file):
        res = f"Error: Memory file '{memory_file}' does not exist."
        _report_telemetry("volatility_pslist", memory_file, {}, "ERROR", res, time.time() - t0)
        return res
    cmd = [VOL_BIN, "-f", memory_file, "windows.pslist"]
    res = _execute(cmd, timeout=300)
    status = "ERROR" if res.startswith("Error") else "SUCCESS"
    _report_telemetry("volatility_pslist", memory_file, {"plugin": "windows.pslist"}, status, res, time.time() - t0)
    return res

@mcp.tool()
def volatility_pstree(memory_file: str) -> str:
    """Displays parent-child process tree hierarchy to identify anomalous parentage or injected processes."""
    t0 = time.time()
    if not os.path.exists(memory_file):
        res = f"Error: Memory file '{memory_file}' does not exist."
        _report_telemetry("volatility_pstree", memory_file, {}, "ERROR", res, time.time() - t0)
        return res
    cmd = [VOL_BIN, "-f", memory_file, "windows.pstree"]
    res = _execute(cmd, timeout=300)
    status = "ERROR" if res.startswith("Error") else "SUCCESS"
    _report_telemetry("volatility_pstree", memory_file, {"plugin": "windows.pstree"}, status, res, time.time() - t0)
    return res

@mcp.tool()
def volatility_malfind(memory_file: str, pid: Optional[int] = None) -> str:
    """Scans memory for hidden, injected, or unlinked executable code and hollowed processes."""
    t0 = time.time()
    if not os.path.exists(memory_file):
        res = f"Error: Memory file '{memory_file}' does not exist."
        _report_telemetry("volatility_malfind", memory_file, {"pid": pid}, "ERROR", res, time.time() - t0)
        return res
    cmd = [VOL_BIN, "-f", memory_file, "windows.malfind"]
    if pid is not None:
        cmd.extend(["--pid", str(pid)])
    res = _execute(cmd, timeout=300)
    status = "ERROR" if res.startswith("Error") else "SUCCESS"
    _report_telemetry("volatility_malfind", memory_file, {"pid": pid}, status, res, time.time() - t0)
    return res

@mcp.tool()
def volatility_netscan(memory_file: str) -> str:
    """Scans memory for active and terminated network connections (TCP/UDP, listening sockets) at capture time."""
    t0 = time.time()
    if not os.path.exists(memory_file):
        res = f"Error: Memory file '{memory_file}' does not exist."
        _report_telemetry("volatility_netscan", memory_file, {}, "ERROR", res, time.time() - t0)
        return res
    cmd = [VOL_BIN, "-f", memory_file, "windows.netscan"]
    res = _execute(cmd, timeout=300)
    status = "ERROR" if res.startswith("Error") else "SUCCESS"
    _report_telemetry("volatility_netscan", memory_file, {"plugin": "windows.netscan"}, status, res, time.time() - t0)
    return res

@mcp.tool()
def volatility_cmdline(memory_file: str, pid: Optional[int] = None) -> str:
    """Displays command line arguments for running processes in the memory image."""
    t0 = time.time()
    if not os.path.exists(memory_file):
        res = f"Error: Memory file '{memory_file}' does not exist."
        _report_telemetry("volatility_cmdline", memory_file, {"pid": pid}, "ERROR", res, time.time() - t0)
        return res
    cmd = [VOL_BIN, "-f", memory_file, "windows.cmdline"]
    if pid is not None:
        cmd.extend(["--pid", str(pid)])
    res = _execute(cmd, timeout=300)
    status = "ERROR" if res.startswith("Error") else "SUCCESS"
    _report_telemetry("volatility_cmdline", memory_file, {"pid": pid}, status, res, time.time() - t0)
    return res

@mcp.tool()
def volatility_run(memory_file: str, plugin: str, extra_args: str = "") -> str:
    """Runs any arbitrary Volatility 3 plugin (e.g. windows.filescan, windows.dumpfiles, linux.bash)."""
    t0 = time.time()
    if not os.path.exists(memory_file):
        res = f"Error: Memory file '{memory_file}' does not exist."
        _report_telemetry("volatility_run", memory_file, {"plugin": plugin}, "ERROR", res, time.time() - t0)
        return res
    cmd = [VOL_BIN, "-f", memory_file, plugin]
    if extra_args:
        cmd.extend(extra_args.split())
    res = _execute(cmd, timeout=300)
    status = "ERROR" if res.startswith("Error") else "SUCCESS"
    _report_telemetry("volatility_run", memory_file, {"plugin": plugin, "extra_args": extra_args}, status, res, time.time() - t0)
    return res

# -------------------------------------------------------------
# NETWORK FORENSICS (TSHARK / WIRESHARK)
# -------------------------------------------------------------

@mcp.tool()
def tshark_conversations(pcap_file: str, conv_type: str = "ip") -> str:
    """Summarizes network conversations in a PCAP file (conv_type: 'ip', 'tcp', 'udp', 'eth')."""
    t0 = time.time()
    if not os.path.exists(pcap_file):
        res = f"Error: PCAP file '{pcap_file}' does not exist."
        _report_telemetry("tshark_conversations", pcap_file, {"conv_type": conv_type}, "ERROR", res, time.time() - t0)
        return res
    if not os.path.exists(TSHARK_BIN):
        res = f"Error: TShark not found at '{TSHARK_BIN}'."
        _report_telemetry("tshark_conversations", pcap_file, {}, "ERROR", res, time.time() - t0)
        return res
    cmd = [TSHARK_BIN, "-r", pcap_file, "-q", "-z", f"conv,{conv_type}"]
    res = _execute(cmd, timeout=180)
    status = "ERROR" if res.startswith("Error") else "SUCCESS"
    _report_telemetry("tshark_conversations", pcap_file, {"conv_type": conv_type}, status, res, time.time() - t0)
    return res

@mcp.tool()
def tshark_dns_queries(pcap_file: str, max_records: int = 150) -> str:
    """Extracts all DNS queries, domain lookups, and IP responses to discover C2 domains, beaconing, or DGA."""
    t0 = time.time()
    if not os.path.exists(pcap_file):
        res = f"Error: PCAP file '{pcap_file}' does not exist."
        _report_telemetry("tshark_dns_queries", pcap_file, {}, "ERROR", res, time.time() - t0)
        return res
    if not os.path.exists(TSHARK_BIN):
        res = f"Error: TShark not found at '{TSHARK_BIN}'."
        _report_telemetry("tshark_dns_queries", pcap_file, {}, "ERROR", res, time.time() - t0)
        return res
    cmd = [
        TSHARK_BIN, "-r", pcap_file,
        "-Y", "dns.flags.response == 0",
        "-T", "fields",
        "-e", "frame.time",
        "-e", "ip.src",
        "-e", "dns.qry.name",
        "-e", "dns.qry.type",
        "-E", "header=y",
        "-E", "separator=,",
        "-c", str(max_records)
    ]
    res = _execute(cmd, timeout=120)
    status = "ERROR" if res.startswith("Error") else "SUCCESS"
    _report_telemetry("tshark_dns_queries", pcap_file, {"max_records": max_records}, status, res, time.time() - t0)
    return res

@mcp.tool()
def tshark_http_requests(pcap_file: str, max_records: int = 150) -> str:
    """Extracts HTTP web requests (Host, Method, URI, User-Agent) from a PCAP capture."""
    t0 = time.time()
    if not os.path.exists(pcap_file):
        res = f"Error: PCAP file '{pcap_file}' does not exist."
        _report_telemetry("tshark_http_requests", pcap_file, {}, "ERROR", res, time.time() - t0)
        return res
    if not os.path.exists(TSHARK_BIN):
        res = f"Error: TShark not found at '{TSHARK_BIN}'."
        _report_telemetry("tshark_http_requests", pcap_file, {}, "ERROR", res, time.time() - t0)
        return res
    cmd = [
        TSHARK_BIN, "-r", pcap_file,
        "-Y", "http.request",
        "-T", "fields",
        "-e", "frame.time",
        "-e", "ip.src",
        "-e", "http.request.method",
        "-e", "http.host",
        "-e", "http.request.uri",
        "-e", "http.user_agent",
        "-E", "header=y",
        "-E", "separator=,",
        "-c", str(max_records)
    ]
    res = _execute(cmd, timeout=120)
    status = "ERROR" if res.startswith("Error") else "SUCCESS"
    _report_telemetry("tshark_http_requests", pcap_file, {"max_records": max_records}, status, res, time.time() - t0)
    return res

@mcp.tool()
def tshark_tls_sni(pcap_file: str, max_records: int = 150) -> str:
    """Extracts SSL/TLS Server Name Indications (SNI) to discover encrypted HTTPS domains contacted by malware."""
    t0 = time.time()
    if not os.path.exists(pcap_file):
        res = f"Error: PCAP file '{pcap_file}' does not exist."
        _report_telemetry("tshark_tls_sni", pcap_file, {}, "ERROR", res, time.time() - t0)
        return res
    if not os.path.exists(TSHARK_BIN):
        res = f"Error: TShark not found at '{TSHARK_BIN}'."
        _report_telemetry("tshark_tls_sni", pcap_file, {}, "ERROR", res, time.time() - t0)
        return res
    cmd = [
        TSHARK_BIN, "-r", pcap_file,
        "-Y", "tls.handshake.extensions_server_name",
        "-T", "fields",
        "-e", "frame.time",
        "-e", "ip.src",
        "-e", "ip.dst",
        "-e", "tls.handshake.extensions_server_name",
        "-E", "header=y",
        "-E", "separator=,",
        "-c", str(max_records)
    ]
    res = _execute(cmd, timeout=120)
    status = "ERROR" if res.startswith("Error") else "SUCCESS"
    _report_telemetry("tshark_tls_sni", pcap_file, {"max_records": max_records}, status, res, time.time() - t0)
    return res

@mcp.tool()
def tshark_filter(pcap_file: str, display_filter: str, fields: str = "", max_records: int = 150) -> str:
    """Applies an arbitrary Wireshark display filter to a PCAP file and prints matching packet data."""
    t0 = time.time()
    if not os.path.exists(pcap_file):
        res = f"Error: PCAP file '{pcap_file}' does not exist."
        _report_telemetry("tshark_filter", pcap_file, {"filter": display_filter}, "ERROR", res, time.time() - t0)
        return res
    if not os.path.exists(TSHARK_BIN):
        res = f"Error: TShark not found at '{TSHARK_BIN}'."
        _report_telemetry("tshark_filter", pcap_file, {}, "ERROR", res, time.time() - t0)
        return res
    cmd = [TSHARK_BIN, "-r", pcap_file, "-Y", display_filter, "-c", str(max_records)]
    if fields:
        cmd.extend(["-T", "fields"])
        for f in fields.split(","):
            cmd.extend(["-e", f.strip()])
        cmd.extend(["-E", "header=y", "-E", "separator=,"])
    res = _execute(cmd, timeout=180)
    status = "ERROR" if res.startswith("Error") else "SUCCESS"
    _report_telemetry("tshark_filter", pcap_file, {"filter": display_filter, "fields": fields}, status, res, time.time() - t0)
    return res

# -------------------------------------------------------------
# AD1 LOGICAL IMAGE EXTRACTION (ACCESSDATA FTK IMAGER)
# -------------------------------------------------------------

@mcp.tool()
def ad1_list(ad1_file: str, path: str = "/") -> str:
    """Lists directory contents inside an AccessData FTK Imager Logical Image (.ad1)."""
    t0 = time.time()
    import dissect.target
    from pathlib import Path
    p = Path(ad1_file)
    if not p.exists():
        res = f"Error: File '{ad1_file}' does not exist."
        _report_telemetry("ad1_list", ad1_file, {"path": path}, "ERROR", res, time.time() - t0)
        return res
    try:
        target = dissect.target.Target.open(p)
        fs = target.filesystems[0]
        entries = fs.listdir(path)
        res = f"Contents of '{path}' in {ad1_file}:\n" + "\n".join(f"- {e}" for e in entries)
        _report_telemetry("ad1_list", ad1_file, {"path": path}, "SUCCESS", res, time.time() - t0)
        return res
    except Exception as e:
        res = f"Error reading AD1: {str(e)}"
        _report_telemetry("ad1_list", ad1_file, {"path": path}, "ERROR", res, time.time() - t0)
        return res

@mcp.tool()
def ad1_extract(ad1_file: str, output_dir: str) -> str:
    """Extracts all files and directories from an AccessData FTK Imager (.ad1) image to a target directory on disk."""
    t0 = time.time()
    import dissect.target
    from pathlib import Path
    p = Path(ad1_file)
    if not p.exists():
        res = f"Error: File '{ad1_file}' does not exist."
        _report_telemetry("ad1_extract", ad1_file, {"output_dir": output_dir}, "ERROR", res, time.time() - t0)
        return res
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    try:
        target = dissect.target.Target.open(p)
        fs = target.filesystems[0]
        count = 0
        for root, dirs, files in fs.walk('/'):
            for f in files:
                full_p = root.rstrip('/') + '/' + f
                rel = full_p.split('/[root]/')[-1] if '/[root]/' in full_p else f
                dest = out / rel.replace('/', '\\')
                dest.parent.mkdir(parents=True, exist_ok=True)
                try:
                    with fs.open(full_p) as src, open(dest, 'wb') as dst:
                        dst.write(src.read())
                    count += 1
                except Exception:
                    pass
        res = f"Successfully extracted {count} files from AD1 to '{output_dir}'!"
        _report_telemetry("ad1_extract", ad1_file, {"output_dir": output_dir, "extracted_count": count}, "SUCCESS", res, time.time() - t0)
        return res
    except Exception as e:
        res = f"Error extracting AD1: {str(e)}"
        _report_telemetry("ad1_extract", ad1_file, {"output_dir": output_dir}, "ERROR", res, time.time() - t0)
        return res

if __name__ == "__main__":
    mcp.run()
