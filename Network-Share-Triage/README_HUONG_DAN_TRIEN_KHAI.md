# HUONG DAN TRIEN KHAI AGENTLESS NETWORK SHARE TRIAGE CHO V-AUTOFOR

## 1. NGUYEN LY HOAT DONG (ZERO-FOOTPRINT TRIAGE)
- Khong cai bat ky phan mem hay agent nao tren may nan nhan.
- May chu V-AutoFor chia se 2 thu muc qua mang LAN:
  1. `\\<IP_V_AUTOFOR>\ForensicTools` (Read-Only): Chua cac file portable binaries (WinPmem, RawCap, CyLR, Sysinternals).
  2. `\\<IP_V_AUTOFOR>\Evidence` (Writeable): Thu muc chua chung cu ForBrain/V-AutoFor.
- May nan nhan chay file thuc thi truc tiep tu o mang vao RAM theo thu tu RFC 3227:
  [1] Dump RAM (winpmem) -> stream ve server
  [2] Capture PCAP (RawCap/Pktmon) -> stream ve server
  [3] Live State (tcpvcon, pslist, autoruns) -> luu LiveState/
  [4] Full Artifacts (CyLR: MFT, Registry, EventLogs, Prefetch) -> nen zip
  [5] Tinh hash SHA-256 tao bien ban Chain of Custody

## 2. CACH THIET LAP TREN MAY CHU V-AUTOFOR (1-CLICK)
Chay file voi quyen Administrator:
👉 `E:\Hunting-Forensics\Network-Share-Triage\setup_network_share.cmd`

## 3. CACH KICH HOAT THU THAP TREN MAY NAN NHAN
- Cach A (Thong qua WinRM / PowerShell Remoting tu xa):
  Invoke-Command -ComputerName <Target_IP> -ScriptBlock { & '\\<IP_V_AUTOFOR>\ForensicTools\Scripts\Run_Full_Triage_Remote.bat' '\\<IP_V_AUTOFOR>' }

- Cach B (Chay truc tiep tai may nan nhan):
  Mo CMD voi quyen Administrator va go:
  `\\<IP_V_AUTOFOR>\ForensicTools\Scripts\Run_Full_Triage_Remote.bat \\<IP_V_AUTOFOR>`

## 4. CO CAN CONFIG GIA TREN V-AUTOFOR KHONG?
- KHONG can config them ve duong dan luu tru: Toan bo goi chung cu duoc day thang ve `E:\Hunting-Forensics\Evidence\<HOSTNAME>_<DATE>\`.
- ForBrain (Port 5000) va V-AutoFor Studio (Port 8787) tu dong quet thay file evidence moi va Agent 01/02 se tiep nhan de verify integrity ngay lap tuc!
