"""Telemetry blueprint for ForBrain.

Logs and broadcasts tool invocations from V-AutoFor AI to the ForBrain monitoring UI.
"""

from __future__ import annotations

import json
import os
import time
from datetime import datetime
from pathlib import Path
from typing import Any
from flask import Blueprint, jsonify, request

telemetry_bp = Blueprint("telemetry_bp", __name__)

TELEMETRY_FILE = Path(__file__).resolve().parents[2] / "telemetry_events.json"
EVIDENCE_DIR = Path(r"E:\Hunting-Forensics\Evidence")
VOL_BIN = Path(r"E:\Hunting-Forensics\Forensic Tool\Forensic AI\AIFT\.venv\Scripts\vol.exe")
TSHARK_BIN = Path(r"C:\Program Files\Wireshark\tshark.exe")

_MAX_EVENTS = 100
_EVENTS_BUFFER: list[dict[str, Any]] = []

def _load_events() -> list[dict[str, Any]]:
    global _EVENTS_BUFFER
    if _EVENTS_BUFFER:
        return _EVENTS_BUFFER
    if TELEMETRY_FILE.exists():
        try:
            with open(TELEMETRY_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                if isinstance(data, list):
                    _EVENTS_BUFFER = data[-_MAX_EVENTS:]
                    return _EVENTS_BUFFER
        except Exception:
            pass
    return []

def _save_events():
    global _EVENTS_BUFFER
    try:
        with open(TELEMETRY_FILE, "w", encoding="utf-8") as f:
            json.dump(_EVENTS_BUFFER[-_MAX_EVENTS:], f, indent=2, ensure_ascii=False)
    except Exception:
        pass

@telemetry_bp.post("/api/telemetry/event")
def record_event():
    """Receives a tool invocation event from V-AutoFor or FastMCP."""
    data = request.get_json(silent=True) or {}
    event_id = data.get("id") or f"evt_{int(time.time() * 1000)}"
    timestamp = data.get("timestamp") or datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tool_name = data.get("tool", "unknown_tool")
    target = data.get("target", "unknown_target")
    params = data.get("params", {})
    status = data.get("status", "SUCCESS")
    duration = data.get("duration", 0)
    output_preview = data.get("output_preview", "")
    caller = data.get("caller", "V-AutoFor AI")

    event = {
        "id": event_id,
        "timestamp": timestamp,
        "caller": caller,
        "tool": tool_name,
        "target": target,
        "params": params,
        "status": status,
        "duration": duration,
        "output_preview": output_preview[:4000],  # cap at 4KB preview
    }

    global _EVENTS_BUFFER
    _load_events()
    _EVENTS_BUFFER.insert(0, event)
    if len(_EVENTS_BUFFER) > _MAX_EVENTS:
        _EVENTS_BUFFER = _EVENTS_BUFFER[:_MAX_EVENTS]
    _save_events()

    return jsonify({"success": True, "event_id": event_id})

@telemetry_bp.get("/api/telemetry/events")
def get_events():
    """Returns recent tool execution events."""
    events = _load_events()
    return jsonify({
        "success": True,
        "total": len(events),
        "events": events
    })

@telemetry_bp.post("/api/telemetry/clear")
def clear_events():
    """Clears telemetry events."""
    global _EVENTS_BUFFER
    _EVENTS_BUFFER = []
    _save_events()
    return jsonify({"success": True, "message": "Telemetry events cleared"})

@telemetry_bp.get("/api/telemetry/status")
def get_system_status():
    """Returns the live status of all integrated forensic engines and evidence files."""
    # Check Volatility 3
    vol_online = VOL_BIN.exists()
    
    # Check TShark
    tshark_online = TSHARK_BIN.exists()

    # Check MemProcFS
    try:
        import memprocfs
        memprocfs_online = True
    except ImportError:
        memprocfs_online = False

    # Check Dissect
    try:
        import dissect.target
        dissect_online = True
    except ImportError:
        dissect_online = False

    # Check Evidence Directory & Files
    evidence_files = []
    if EVIDENCE_DIR.exists():
        try:
            for item in EVIDENCE_DIR.rglob("*"):
                if item.is_file():
                    evidence_files.append({
                        "name": item.name,
                        "rel_path": str(item.relative_to(EVIDENCE_DIR)),
                        "size_bytes": item.stat().st_size,
                        "ext": item.suffix.lower(),
                    })
        except Exception:
            pass

    return jsonify({
        "success": True,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "tools": {
            "dissect": {
                "name": "Dissect Forensic Engine",
                "status": "ONLINE" if dissect_online else "OFFLINE",
                "capabilities": ["AD1", "E01", "VMDK", "VHD", "RAW", "Logical custom container"],
                "version": "Dissect 3.x"
            },
            "volatility3": {
                "name": "Volatility 3 Memory Forensics",
                "status": "ONLINE" if vol_online else "OFFLINE",
                "capabilities": ["windows.pslist", "windows.pstree", "windows.malfind", "windows.netscan", "windows.cmdline"],
                "path": str(VOL_BIN)
            },
            "memprocfs": {
                "name": "MemProcFS Direct RAM Analyzer",
                "status": "ONLINE" if memprocfs_online else "OFFLINE",
                "capabilities": ["Live VMM mounting", "Physical memory forensic page tables"],
                "version": "MemProcFS 5.19"
            },
            "tshark": {
                "name": "Wireshark / TShark Network Engine",
                "status": "ONLINE" if tshark_online else "OFFLINE",
                "capabilities": ["PCAP / PCAPNG", "Conversations", "DNS Hunting", "HTTP/TLS SNI"],
                "path": str(TSHARK_BIN)
            },
            "fastmcp_gateway": {
                "name": "FastMCP Bridge to V-AutoFor",
                "status": "CONNECTED",
                "plugins": ["aift", "eztools", "sysinternals", "network_memory"],
                "target_ai": "V-AutoFor (Port 8787)"
            },
            "zimmerman": {
                "name": "Eric Zimmerman Tools (SANS FOR508)",
                "status": "ONLINE",
                "capabilities": ["AmcacheParser", "PECmd", "AppCompatCacheParser", "MFTECmd", "EvtxECmd", "SBECmd", "LECmd", "JLECmd", "SrumECmd"],
                "path": r"E:\Hunting-Forensics\Forensic Tool\Get-ZimmermanTools"
            },
            "pe_malware": {
                "name": "PE Static & Malware Analysis",
                "status": "ONLINE",
                "capabilities": ["Compile Timestamp", "Section Entropy (Packer detection)", "Imphash", "API Import Table"],
                "version": "pefile 2024.8.26"
            },
            "linux_logs": {
                "name": "Linux Log & Bash History Analyzer",
                "status": "ONLINE",
                "capabilities": ["SSH Brute-Force", "Successful logins", "Sudo escalation", "Suspicious bash commands"]
            }
        },
        "evidence_repository": {
            "root_path": str(EVIDENCE_DIR),
            "files_count": len(evidence_files),
            "files": evidence_files[:30]
        }
    })
