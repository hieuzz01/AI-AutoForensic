---
name: collect-evidence
description: SOP thu thập (collection & acquisition) evidence từ xa các máy nạn nhân qua Network-Share-Triage — check máy mục tiêu, kiểm tra kết nối và điều kiện thu thập, pull log/file evidence về V-AutoFor. Chỉ được chạm vào scripts + tools trong E:\Hunting-Forensics\Network-Share-Triage; tải tool mới phải hỏi user; quyền thiếu thì dừng, không tự ý tác động máy victim.
---

# V-AutoFor Evidence Collection SOP (Agentless Acquisition từ các máy khác)

Skill này điều hành **phases thu thập evidence** (collection) từ các máy khác (Linux/Windows)
về `E:\Hunting-Forensics\Evidence\`. **Phân tích evidence KHÔNG nằm trong skill này** —
sau khi evidence về và verify, chuyển sang skill `v-autofor-investigation`.

---

## 0. VÙNG TÁC ĐỘNG — RÀNG BUỘC BẮT BUỘC (QUAN TRỌNG NHẤT)

> [!CAUTION]
> **QUY TẮC SỐ 1 — CHỈ ĐƯỢC ĐỘNG TỚI FOLDER THU THẬP:**
> Mọi thay đổi (sửa/troubleshoot script, nâng cấp tool) **CHỈ** được thực hiện trong
> `E:\Hunting-Forensics\Network-Share-Triage\` (scripts `Scripts\`, `Linux_Triage\`,
> `1_RAM\`, `2_Network\`, `3_LiveState\`, `4_Artifacts\`, `setup_network_share.cmd`).
> **TUYỆT ĐỐI KHÔNG** sửa bất kỳ thứ nào khác: code ForBrain, MCP servers, config
> Reasonix, các folder khác của workspace, và **chưa nói gì tới các máy khác**.
> (Ngoại lệ duy nhất đã được user duyệt trong 2026-11-11: thêm param `sudo_password`
> vào `remote_triage_mcp.py` — các lần sửa MCP server sau vẫn PHẢI hỏi user trước.)

> [!CAUTION]
> **QUY TẮC SỐ 2 — MÁY VICTIM CHỈ BỊ "THU THẬP", KHÔNG BỊ "TÁC ĐỘNG":**
> - Không cài đặt, không thêm/xóa gói (apt/pip/choco...), không đổi cấu hình,
>   không đổi service, không sửa file hệ thống, không tạo tài khoản, không tắt
>   firewall, không đổi timezone, không khởi động lại, không chạy tool phân tích.
> - Trừu tượng duy nhất được phép chạy trên victim: **script triage của
>   `Network-Share-Triage`** (thiết kế zero-footprint: script tự xóa bản thân
>   và state file sau khi pull xong).
> - Quyền cần trên victim (SSH user, sudo password, SMB/WinRM credential)
>   **LUÔN HỎI USER** trước khi dùng hoặc trước khi chạy bước thiếu quyền.
>   **Không đủ quyền ➔ dừng lại, báo user cần cấp quyền gì, KHÔNG tự tìm cách
>   bypass (không thử brute-force, không tìm key, không escalate ngoài sudo password
>   do user cấp).**

> [!CAUTION]
> **QUY TẮC SỐ 3 — TẢI TOOL MỚI PHẢI HỎI USER:**
> Mọi tool/binary mới cần đưa vào `Network-Share-Triage` (tcpdump bản khác,
> WinPmem bản khác, CyLR bản mới, thêm tool gì đó...) — **bắt buộc hỏi user**
> (tên tool, phiên bản, nguồn, tại sao cần, đặt ở subfolder nào) và **chỉ tải khi
> user đồng ý**. Không tự ý tải, không tự ý thay phiên bản tool đang có.
> Tool có sẵn (check trước khi hỏi tải): WinPmem Mini, RawCap, Sysinternals
> (autorunsc/handle/pslist/tcpvcon/sigcheck 32+64), CyLR (Windows + Linux),
> UAC 3.4.0 (Linux), `collect_linux_triage.sh`.

> [!NOTE]
> **QUY TẮC SỐ 4 — CHỈ THU THẬP (COLLECTION ONLY):**
> Skill này kết thúc khi evidence đã về `Evidence\` + integrity verified.
> Phân tích (tshark, volatility, parse logs...) thuộc `v-autofor-investigation`.

---

## 1. BẢN ĐỒ CÁC KÊNH THU THẬP

| Target | Kênh | Port cần | Credential | Script chạy trên victim | Evidence về bằng |
|---|---|---|---|---|---|
| **Linux** | SSH + SFTP **pull** (V-AutoFor chủ động connect) | 22 (1 chiều vào victim) | user + password (hoặc key); `sudo_password` nếu user không phải root | `Linux_Triage\collect_linux_triage.sh` (2 pha, leo quyền `sudo -S` tự động) | SFTP pull `.tar.gz` + CoC về `Evidence\<IP>_Linux_<ts>\` |
| **Windows** | WinRM + SMB share (victim **push**) | 445 (SMB) và/hoặc 5985 (WinRM) | credential domain/user có quyền | `Scripts\Run_Full_Triage_Remote.bat` | Victim ghi thẳng `\\<IP_V>\Evidence\<HOST>_<DATE>\` qua share |
| **Windows (fallback)** | Chạy bat tại máy + copy tay | — | user có quyền local | bat như trên ghi USB/local | Copy vào `Evidence\` thủ công |

MCP tools (server `remote_triage`, đã đăng ký trong `config.toml`):
- `detect_target_os_and_ports` — quét port 22/445/5985/5986/3389, đoán OS
- `pull_linux_evidence` — chạy PHASE A (START); khi chạy lần 2 với state file tồn tại ➔ PHASE B (FINISH + pull)
- `wait_for_linux_capture` — PHASE B chuyên dụng (polling, mỗi call ≤295s) — **chỉ hiệu lực sau khi process MCP server được khởi động lại** (chết process python `remote_triage_mcp.py` rồi gọi lại tool để Reasonix spawn mới)
- `trigger_universal_remote_triage` — auto-detect OS rồi dispatch
- `trigger_remote_triage` — Windows qua WinRM
- `check_network_share_status` — check share `ForensicTools`/`Evidence` + inventory tools

## 2. QUY TRÌNH STEP-BY-STEP

### STEP 1 — Xác định máy mục tiêu ("check máy gì?")
1. **HỎI/CONFIRM user:** IP + hostname của victim, OS dự kiến, credential theo kênh
   (Linux: user + password + có sudo không, password sudo; Windows: user + password).
   Không có credential ➔ dừng ở đây, báo user cần cung cấp gì.
2. Ghi nhận trong chat: target IP, hostname, OS, kênh định dùng, người duyệt.
3. Check máy chủ V-AutoFor có adapter cùng segment với victim không:
   `Get-NetIPAddress -AddressFamily IPv4` — victim `192.168.x.x` thì máy mình phải có
   interface `192.168.x.0/24` (VD: lab hiện tại dùng VMware VMnet8 `192.168.91.1`).
   Không cùng segment ➔ hỏi user cách nối (bridge VM, cable, route+firewall) —
   **không tự thêm route/firewall rule**.

### STEP 2 — Check kết nối
1. `Test-Connection <IP> -Count 4` — ping thông?
2. Gọi MCP `detect_target_os_and_ports(target_ip)` — OS + trạng thái port.
3. Chẩn đoán theo kết quả:
   - Ping DEAD ➔ sai IP / victim down / khác segment (quay STEP 1.3).
   - Ping sống nhưng port đóng ➔ firewall victim chặn kênh đó ➔ hỏi user kênh khác.
   - Linux: cần **22 OPEN**. Windows: cần **445 hoặc 5985 OPEN**.

### STEP 3 — Check điều kiện thu thập (theo OS)
**Linux:**
- SSH auth: user + password (test khi chạy PHASE A — lỗi "Authentication failed"
  thường do `PermitRootLogin prohibit-password`: **đừng login thẳng root**, dùng
  user thường + `sudo_password`).
- Quyền: tcpdump cần CAP_NET_RAW. User thường không có ➔ bắt buộc có
  `sudo_password` (script tự leo quyền). Không có ➔ **dừng, hỏi user** (chỉ thu
  được log của user, không có pcap + shadow).
- Check tool trên victim (khi có issue): `command -v tcpdump || ls -la /usr/sbin/tcpdump /usr/bin/tcpdump`
  (script đã tự probe các path này). tcpdump không tồn tại ➔ **hỏi user có được
  cài/không** (Quy tắc 3) — không tự cài.
- Disk /tmp của victim đủ chỗ (tar.gz có thể vài trăm MB).

**Windows:**
- Gọi `check_network_share_status` — share `ForensicTools` + `Evidence` ACTIVE,
  inventory tools đủ (WinPmem, RawCap, Sysinternals, CyLR).
  Share chưa có ➔ hỏi user chạy `setup_network_share.cmd` (Admin) trên máy chủ.
- Firewall máy chủ cho phép SMB-In (445) từ victim.
- **KNOWN BUG (chưa sửa, user chưa duyệt):** `trigger_remote_triage` gọi bat
  **không forward tham số IP** ➔ bat dùng fallback `\\10.1.20.80`
  (`Run_Full_Triage_Remote.bat` dòng 14). Nếu IP thật của V-AutoFor khác
  `10.1.20.80` ➔ **DÙNG CÁCH B** trong README (chạy bat trên victim với đúng
  IP tham số, hoặc WinRM Invoke-Command truyền IP) thay vì tool `trigger_remote_triage`.

### STEP 4 — Cấu hình script theo yêu cầu (chỉ trong `Network-Share-Triage`)
Được phép sửa `collect_linux_triage.sh` / `Run_Full_Triage_Remote.bat` để:
- Đổi thời lượng capture: hằng số `CAPTURE_SECONDS` (đầu script, hiện tại = 60 —
  mặc định thiết kế 300s; đổi theo yêu cầu user, nhớ ghi chú "per operator request").
- Thêm/bớt artifact thu thập (log, config, history) — thêm block copy, giữ cấu trúc
  RFC 3227 (volatile trước, PCAP, logs, CoC).
- **HẠN CHẾ KỸ THUẬT CỐT LÕI (không được phá khi sửa):** mỗi lần gọi MCP có trần
  300s (`mcp_call_timeout_seconds`). Thiết kế **2 pha** của `collect_linux_triage.sh`:
  - PHASE A (call 1): thu volatile state + bật tcpdump **detached**
    (`setsid nohup timeout N tcpdump ... &`) + ghi state file
    `/tmp/.vautofor_capture.state` + thoát nhanh.
  - PHASE B (call 2, cùng script): nhận state file (`. state_file`), chờ tcpdump,
    mv pcap vào work dir, `tar.gz`, `sha256sum` CoC, emit `SUCCESS:<tar>:<coc>`.
  - Khi sửa script: **giữ nguyên** contract `SUCCESS:` line, tên state file,
    cơ chế leo quyền `sudo -S` đầu script, cleanup tự xóa trên victim.
  - Sửa xong luôn kiểm tra logic shell (đọc lại; nếu có bash/gits trên lab mới thì
    `sh -n` được — trên host Windows thì đọc tay kỹ thứ tự câu lệnh).
- **KHÔNG** sửa bất kỳ file nào ngoài `Network-Share-Triage` vì lỗi của script
  (VD: lỗi ở MCP server ➔ báo user, KHÔNG tự sửa MCP).

### STEP 5 — Chạy thu thập
**Linux (2 pha):**
1. `pull_linux_evidence(target_ip, target_user, target_password, sudo_password=...)`
   ➔ PHASE A. Kiểm tra stdout có `PHASE_START_COMPLETE ... tool=/usr/bin/tcpdump`
   (hoặc path khác). Nếu `PCAP_TOOL=MISSING` ➔ tcpdump không có ➔ Quy tắc 3.
2. Sleep đủ `CAPTURE_SECONDS` + 15s đệm.
3. Gọi `pull_linux_evidence` lần 2 (hoặc `wait_for_linux_capture` nếu đã reload
   MCP) ➔ PHASE B. Kiểm tra stdout có `PCAP_OK <size> bytes` + `SUCCESS:`.
   Nếu `WARNING: PCAP NOT FOUND` ➔ vào bảng Troubleshoot (phần 5).
4. Kết quả: `Evidence\<IP>_Linux_<ts>\<EVIDENCE>.tar.gz` +
   `Chain_of_Custody_<host>.txt`.

**Windows:** chạy theo README `Network-Share-Triage\README_HUONG_DAN_TRIEN_KHAI.md`
(Cách A WinRM / Cách B chạy trực tiếp) — lưu ý KNOWN BUG ở STEP 3.

### STEP 6 — Xác minh evidence sau pull (trên máy V-AutoFor)
1. Đọc `Chain_of_Custody_*.txt` — lấy SHA-256 gốc.
2. Tính lại SHA-256 file tar.gz/pcap (khai báo rõ trong chat nếu dùng shell hash
   vì `verify_evidence_integrity` vắng mặt trong catalog — theo SOP
   `v-autofor-investigation` §2.1; nếu tool có trong catalog thì gọi MCP).
3. Khớp ➔ **Integrity Verified**. Lệch ➔ cảnh báo user (hỏng trong quá trình
   truyền tải), thu thập lại nếu cần.
4. Bung tar.gz ra `$TMPDIR` (scratch, KHÔNG bung vào Evidence\) để kiểm tra cấu
   trúc: có `Network/*.pcap` đúng size, `LiveState/`, `Logs/`, `Config_Users/`.
5. Báo cáo user: vị trí evidence, hash, thời gian acquire (ghi rõ timezone —
   VM Linux thường lệch múi so với host, xem CoC để đối chiếu), artifacts
   thiếu (nếu có) và lý do.

## 3. QUYỀN CẦN — BẢNG HỎI USER

| Thu thập được | Quyền tối thiểu trên victim |
|---|---|
| Log + process + PCAP **đầy đủ** (Linux) | user sudo được (cấp `sudo_password`) — chạy tcpdump như root |
| Log + process (không PCAP, không shadow) | SSH user thường, không cần sudo |
| Windows: RAM + PCAP + artifacts (CyLR) | credential chạy bat với Admin (WinPmem/RawCap cần Admin), user cho đọc share `ForensicTools` + ghi share `Evidence` |
| Windows: chỉ live state | user thường + SMB ghi `Evidence` |

Thiếu quyền ➔ **dừng, liệt kê đúng quyền còn thiếu, chờ user. Không bypass.**

## 4. BẢNG TROUBLESHOOT SCRIPT (các lỗi đã gặp thật, 2026-11-11)

| Triệu chứng | Nguyên nhân | Sửa trong script (trong `Network-Share-Triage` thôi) |
|---|---|---|
| `Network/` trống, không có `.pcap`, `WARNING: PCAP NOT FOUND (PCAP_TOOL=/usr/bin/tcpdump)` | TCPDUMP BỊ CHẾT IM LẶNG: user thường không có CAP_NET_RAW (`-i any` cần raw socket); stderr bị `>/dev/null` nuốt | Script đã có khối leo quyền `sudo -S` đầu file — gọi tool với `sudo_password=<pw>`. Nếu user không sudo được ➔ báo user, bỏ pcap (đổi `CAPTURE` block thành `:`) — **hỏi user trước** |
| `PCAP_TOOL=MISSING` | PATH shell SSH không-login không có `/usr/sbin` (Kali/Debian) | Script đã probe `/usr/sbin/tcpdump /sbin/tcpdump /usr/bin/tcpdump /bin/tcpdump` — nếu vẫn MISSING: tcpdump chưa cài ➔ **hỏi user** (Quy tắc 3) |
| MCP call timeout 300s giữa chừng | Capture dài hơn trần call | Giữ thiết kế 2 pha (STEP 4) — **không** chạy capture blocking dài trong 1 call |
| State file `>>` bị truncate mất | append vào state file **trước** khối `cat > STATE_FILE` cuối Phase A | Mọi biến cần mang sang Phase B phải nằm trong heredoc `cat >` cuối Phase A (VD: `PCAP_TOOL=${TCPDUMP_BIN_USED}`) |
| Pcap nằm trong `/tmp` rời rạc, Phase B không thấy | Ghi pcap ngoài work dir khi chạy root (work dir thuộc user) | `PCAP_PATH="${WORK_DIR}/Network/live_traffic_${CAPTURE_SECONDS}s.pcap"` — luôn ghi thẳng vào work dir (khi đã sudo re-exec, work dir thuộc root) |
| SSH `Authentication failed` với user root | `PermitRootLogin prohibit-password` (Kali/Ubuntu mặc định) | **Không** cố root SSH — dùng user thường + `sudo_password` |
| Windows bat chạy nhưng evidence đổ về folder sai / không có | KNOWN BUG: `trigger_remote_triage` không forward IP ➔ bat dùng fallback `10.1.20.80` | Dùng README Cách B (truyền đúng IP khi chạy bat). Sửa bat/MCP ➔ **hỏi user** (ngoài phạm vi folder được phép) |
| Timestamp file evidence lệch múi với host | Victim VM chạy timezone khác (VD: Kali EST, host UTC+7) | Không sửa clock victim. Ghi rõ timezone của victim trong báo cáo + đối chiếu qua CoC |
| `sudo` treo chờ TTY (`requiretty`) | /etc/sudoers có `requiretty` | **Không tự sửa sudoers trên victim** — hỏi user |
| Gói tar.gz thiếu artifacts (VD: không có `/etc/shadow`) | Chạy non-root | Bump lên root bằng `sudo_password` (hỏi user) |

## 5. CHECKLIST TRƯỚC KHI GHI "HOÀN TẤT" VỚI USER

- [ ] Evidence nằm trong `E:\Hunting-Forensics\Evidence\<target>_<OS>_<ts>\`
- [ ] SHA-256 đối chiếu CoC — khớp
- [ ] PCAP (nếu yêu cầu) tồn tại, size > 0, ghi rõ cửa sổ thời gian bắt đầu/kết thúc + timezone
- [ ] Script trên victim đã tự cleanup (state file, tar tạm, script) — zero-footprint
- [ ] Không có gì ngoài `Network-Share-Triage` bị thay đổi trong phiên
- [ ] Mọi tool mới tải / quyền dùng đều đã được user đồng ý và được ghi trong báo cáo
- [ ] Báo cáo user: danh sách artifacts + những gì KHÔNG thu được và lý do (thiếu quyền/thiếu tool)
