"""
Sysinternals Tools MCP Server
Exposes Sysinternals CLI utilities via Model Context Protocol (FastMCP).
Automatically injects -accepteula to prevent interactive GUI prompts.
Sends telemetry events to ForBrain.
"""

import os
import subprocess
import json
import time
from typing import List, Optional
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("sysinternals-tools")

BASE_DIR = r"E:\Hunting-Forensics\Forensic Tool\SysinternalsSuite"
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
    tool_path = os.path.join(BASE_DIR, tool_name)
    if not os.path.exists(tool_path):
        tool_64 = tool_name.replace(".exe", "64.exe")
        p64 = os.path.join(BASE_DIR, tool_64)
        if os.path.exists(p64):
            return p64
        raise FileNotFoundError(f"Sysinternals tool '{tool_name}' not found at {tool_path}")
    return tool_path

def _execute(cmd: List[str], timeout: int = 180) -> str:
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
        return f"Error executing command: {str(e)}"

@mcp.tool()
def list_sysinternals_tools() -> str:
    """Lists all available Sysinternals command line and GUI executables in the suite."""
    if not os.path.exists(BASE_DIR):
        return f"Directory {BASE_DIR} does not exist."
    tools = []
    for f in sorted(os.listdir(BASE_DIR)):
        if f.lower().endswith(".exe"):
            tools.append(f)
    return "Available Sysinternals Tools:\n" + "\n".join(tools)

@mcp.tool()
def run_sysinternals_tool(tool_name: str, arguments: List[str], timeout_seconds: int = 180) -> str:
    """Runs any Sysinternals CLI tool with the specified arguments, automatically injecting -accepteula."""
    t0 = time.time()
    try:
        tool_path = _resolve_tool(tool_name)
        cmd = [tool_path, "-accepteula"] + [a for a in arguments if a.lower() != "-accepteula"]
        res = _execute(cmd, timeout=timeout_seconds)
        status = "ERROR" if res.startswith("Error") else "SUCCESS"
        _report_telemetry(f"sysinternals_{tool_name}", " ".join(arguments), {}, status, res, time.time() - t0)
        return res
    except Exception as e:
        res = f"Error: {str(e)}"
        _report_telemetry(f"sysinternals_{tool_name}", " ".join(arguments), {}, "ERROR", res, time.time() - t0)
        return res

@mcp.tool()
def autoruns_triage(output_csv: Optional[str] = None, filter_all: bool = True, extra_args: str = "") -> str:
    """Runs autorunsc.exe to inspect all autostart persistence locations (registry, tasks, services)."""
    t0 = time.time()
    tool_path = _resolve_tool("autorunsc64.exe")
    cmd = [tool_path, "-accepteula"]
    if filter_all:
        cmd.extend(["-a", "*"])
    if output_csv:
        cmd.extend(["-c", "-s"])
    if extra_args:
        cmd.extend(extra_args.split())
    res = _execute(cmd)
    if output_csv and "STDOUT" in res:
        try:
            with open(output_csv, "w", encoding="utf-8") as f:
                f.write(res)
        except Exception:
            pass
    status = "ERROR" if res.startswith("Error") else "SUCCESS"
    _report_telemetry("autoruns_triage", "System Persistence", {"output_csv": output_csv}, status, res, time.time() - t0)
    return res

@mcp.tool()
def sigcheck_file(file_or_dir_path: str, check_hashes: bool = True, check_virustotal: bool = False, extra_args: str = "") -> str:
    """Verifies file digital signatures, publisher, PE headers and hashes using sigcheck64.exe."""
    t0 = time.time()
    tool_path = _resolve_tool("sigcheck64.exe")
    cmd = [tool_path, "-accepteula"]
    if check_hashes:
        cmd.append("-h")
    if check_virustotal:
        cmd.append("-v")
    if extra_args:
        cmd.extend(extra_args.split())
    cmd.append(file_or_dir_path)
    res = _execute(cmd)
    status = "ERROR" if res.startswith("Error") else "SUCCESS"
    _report_telemetry("sigcheck_file", file_or_dir_path, {"hashes": check_hashes}, status, res, time.time() - t0)
    return res

@mcp.tool()
def extract_strings(file_path: str, min_length: int = 4, unicode_only: bool = False, extra_args: str = "") -> str:
    """Extracts printable ASCII and Unicode strings from binary files using strings64.exe."""
    t0 = time.time()
    tool_path = _resolve_tool("strings64.exe")
    cmd = [tool_path, "-accepteula", "-n", str(min_length)]
    if unicode_only:
        cmd.append("-u")
    if extra_args:
        cmd.extend(extra_args.split())
    cmd.append(file_path)
    res = _execute(cmd)
    status = "ERROR" if res.startswith("Error") else "SUCCESS"
    _report_telemetry("extract_strings", file_path, {"min_length": min_length}, status, res, time.time() - t0)
    return res

@mcp.tool()
def list_handles(target_name_or_pid: Optional[str] = None, extra_args: str = "") -> str:
    """Lists open file/registry handles across processes using handle64.exe."""
    t0 = time.time()
    tool_path = _resolve_tool("handle64.exe")
    cmd = [tool_path, "-accepteula"]
    if extra_args:
        cmd.extend(extra_args.split())
    if target_name_or_pid:
        cmd.append(target_name_or_pid)
    res = _execute(cmd)
    status = "ERROR" if res.startswith("Error") else "SUCCESS"
    _report_telemetry("list_handles", target_name_or_pid or "ALL", {}, status, res, time.time() - t0)
    return res

@mcp.tool()
def list_network_connections(extra_args: str = "") -> str:
    """Lists active network sockets, protocols, and endpoints using tcpvcon.exe."""
    t0 = time.time()
    tool_path = _resolve_tool("tcpvcon.exe")
    cmd = [tool_path, "-accepteula", "-a", "-c"]
    if extra_args:
        cmd.extend(extra_args.split())
    res = _execute(cmd)
    status = "ERROR" if res.startswith("Error") else "SUCCESS"
    _report_telemetry("list_network_connections", "Local Sockets", {}, status, res, time.time() - t0)
    return res

if __name__ == "__main__":
    mcp.run()
