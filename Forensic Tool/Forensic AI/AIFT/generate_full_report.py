import os
from pathlib import Path
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_background(cell, fill_hex):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def generate_docx():
    doc = Document()
    
    # Page Margins
    for s in doc.sections:
        s.top_margin = Inches(0.75)
        s.bottom_margin = Inches(0.75)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)

    # Base Font
    normal = doc.styles['Normal']
    normal.font.name = 'Calibri'
    normal.font.size = Pt(10)
    normal.font.color.rgb = RGBColor(0x33, 0x33, 0x33)

    # Header Title
    p_pre = doc.add_paragraph()
    p_pre.paragraph_format.space_before = Pt(0)
    p_pre.paragraph_format.space_after = Pt(2)
    r_pre = p_pre.add_run("BÁO CÁO GIẢI PHÁP KỸ THUẬT & HƯỚNG DẪN VẬN HÀNH TOÀN DIỆN")
    r_pre.font.size = Pt(10)
    r_pre.font.bold = True
    r_pre.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(0)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("NỀN TẢNG AI FORENSIC V-AUTOFOR & FORBRAIN OBSERVABILITY")
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_desc = doc.add_paragraph()
    p_desc.paragraph_format.space_after = Pt(12)
    r_desc = p_desc.add_run("Tích hợp Chuẩn SANS FOR508 (2025), Bộ công cụ Eric Zimmerman, Sysinternals Suite, Volatility 3, TShark, FastMCP Bridge và Cơ chế Telemetry Real-time.\nChuẩn hóa điều tra theo ISO/IEC 27037, NIST SP 800-86 và MITRE ATT&CK Enterprise Matrix.")
    r_desc.font.size = Pt(9.5)
    r_desc.font.italic = True
    r_desc.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # Meta Table
    meta = [
        ("Nền tảng mục tiêu:", "V-AutoFor AI Studio (:8787), ForBrain Observability (:5000), 9Router Gateway (:20128)"),
        ("Tài liệu tham chiếu:", "SANS FOR508: Advanced Incident Response, Threat Hunting & Digital Forensics (2025)"),
        ("Phạm vi bằng chứng:", "Memory (RAM), Network (PCAP), Disk Images (E01/Raw), Logical Container (AD1), Windows & Linux Artifacts"),
        ("Trạng thái triển khai:", "100% Hoàn tất tại E:\\Hunting-Forensics, 4 Cụm FastMCP, 40+ Công cụ Chuyên sâu, Live Telemetry Stream")
    ]
    t_meta = doc.add_table(rows=4, cols=2)
    t_meta.alignment = WD_TABLE_ALIGNMENT.CENTER
    for i, (k, v) in enumerate(meta):
        r = t_meta.rows[i]
        c0, c1 = r.cells[0], r.cells[1]
        c0.width = Inches(2.0)
        c1.width = Inches(5.0)
        set_cell_background(c0, "F1F5F9")
        set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0, 40, 40, 80, 80)
        set_cell_margins(c1, 40, 40, 80, 80)
        p0 = c0.paragraphs[0]; p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(k); r0.font.bold = True; r0.font.size = Pt(9)
        p1 = c1.paragraphs[0]; p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(v); r1.font.size = Pt(9)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    def add_h(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(4)
        r = p.add_run(text)
        r.font.size = Pt(12)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    # 1. Architecture
    add_h("1. TỔNG QUAN GIẢI PHÁP & PHÂN TÁCH VAI TRÒ KIẾN TRÚC")
    p = doc.add_paragraph()
    p.add_run("Hệ thống V-AutoFor được kiến trúc theo mô hình 4 thành phần tách biệt:\n"
              "1. V-AutoFor AI Studio (Port 8787): Điều tra viên AI trí tuệ cao, giao tiếp với người dùng, nạp sẵn bộ kỹ năng (skills) và ràng buộc bắt buộc gọi công cụ MCP forensic.\n"
              "2. ForBrain Observability Monitor (Port 5000): Bộ Não giám sát tập trung, quản lý kho chứng cứ và trực quan hóa luồng Live AI Execution Feed & Call Telemetry theo thời gian thực.\n"
              "3. 9Router AI Gateway (Port 20128): Trạm định tuyến proxy và quản lý API Key tập trung (Gemini, OpenAI, DeepSeek, Groq, Claude) với cơ chế failover tự động.\n"
              "4. FastMCP Bridge: 4 máy chủ FastMCP cung cấp hơn 40 công cụ giám định nhị phân chuyên sâu qua giao thức IPC stdio chuẩn.")

    # 2. Local deployment guide
    add_h("2. HƯỚNG DẪN CÀI ĐẶT TỪ ĐẦU SANG MÁY KHÁC (LOCAL DEPLOYMENT GUIDE)")
    p = doc.add_paragraph()
    p.add_run("Để triển khai hệ thống sang máy chủ/máy trạm Windows mới:\n"
              "• Bước 1: Cài đặt Python 3.10+, Node.js v18+, .NET 8/9 Runtime và Wireshark (tại C:\\Program Files\\Wireshark).\n"
              "• Bước 2: Tạo thư mục E:\\Hunting-Forensics cùng các thư mục con Evidence, skills, Forensic Tool.\n"
              "• Bước 3: Cài đặt Node modules toàn cục: npm install -g reasonix 9router.\n"
              "• Bước 4: Tạo Python virtualenv tại E:\\Hunting-Forensics\\Forensic Tool\\Forensic AI\\AIFT\\.venv và cài đặt: pip install flask fastmcp dissect pefile pypdf volatility3 requests.\n"
              "• Bước 5: Tạo liên kết thư mục NTFS Junctions cho ForBrain và MCP-Servers.\n"
              "• Bước 6: Copy bộ nhị phân Eric Zimmerman Tools và Sysinternals Suite vào Forensic Tool.\n"
              "• Bước 7: Đăng ký hai lệnh v-autofor.cmd và v-autofor-stop.cmd vào thư mục npm.")

    # 3. API Config
    add_h("3. HƯỚNG DẪN LẤY VÀ CẤU HÌNH API KEY VÀO HỆ THỐNG")
    p = doc.add_paragraph()
    p.add_run("• Nguồn lấy API Key:\n"
              "   - Google Gemini: Đăng ký miễn phí tại https://aistudio.google.com/app/apikey (Mô hình gemini-3.8-flash).\n"
              "   - OpenAI: Lấy tại https://platform.openai.com/api-keys (Mô hình gpt-4o, o3-mini).\n"
              "   - DeepSeek: Lấy tại https://platform.deepseek.com/api_keys (Mô hình deepseek-chat, deepseek-reasoner).\n"
              "• Cách nạp API Key:\n"
              "   - Cách 1 (Khuyến nghị): Mở giao diện 9Router tại http://127.0.0.1:20128, vào menu Providers ➔ Add Provider ➔ Dán API Key ➔ Save & Test.\n"
              "   - Cách 2: Khai báo trực tiếp trong C:\\Users\\<User>\\AppData\\Roaming\\reasonix\\config.toml tại mục [[providers]] và file .env.")

    # 4. SANS FOR508 Artifacts Matrix
    add_h("4. MA TRẬN BẰNG CHỨNG & CÔNG CỤ CHUẨN SANS FOR508 (2025)")
    t_sans = doc.add_table(rows=1, cols=4)
    t_sans.alignment = WD_TABLE_ALIGNMENT.CENTER
    hdr = t_sans.rows[0].cells
    hdr[0].width = Inches(1.1); hdr[1].width = Inches(1.8); hdr[2].width = Inches(1.8); hdr[3].width = Inches(2.3)
    col_names = ["Artifact / Định dạng", "Vị trí & Bản chất", "Công cụ FastMCP (ForBrain)", "Mục tiêu điều tra SANS FOR508"]
    for idx, name in enumerate(col_names):
        set_cell_background(hdr[idx], "0F172A")
        set_cell_margins(hdr[idx], 60, 60, 80, 80)
        p = hdr[idx].paragraphs[0]; p.paragraph_format.space_after = Pt(0)
        r = p.add_run(name); r.font.bold = True; r.font.size = Pt(8.5); r.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)

    rows = [
        (".ad1", "Logical Container (FTK Imager)", "ad1_list, ad1_extract", "Trích xuất container logic ra cây thư mục đĩa."),
        (".txt / .log metadata", "Báo cáo đi kèm file ảnh", "verify_evidence_integrity", "Băm MD5, SHA-1, SHA-256 đối soát với hash gốc (ISO 27037)."),
        (".pf (Prefetch)", "C:\\Windows\\Prefetch", "parse_prefetch (PECmd)", "Chứng minh thực thi: số lần chạy, 8 mốc thời gian, DLLs."),
        ("Amcache.hve", "appcompat\\Programs", "parse_amcache (AmcacheParser)", "SHA-1 của binary, đường dẫn thực thi, compile time."),
        ("SYSTEM (Shimcache)", "AppCompatCache", "parse_shimcache (AppCompatCacheParser)", "Xác nhận file nhị phân đã từng tồn tại và kích hoạt."),
        ("$MFT (Master File Table)", "Root phân vùng NTFS", "parse_mft (MFTECmd)", "Phát hiện Timestomping ($SI vs $FN), lịch sử tạo/xóa file."),
        (".evtx (Event Logs)", "System32\\winevt\\Logs", "parse_evtx (EvtxECmd)", "Triage Logon (4624/4625), Sudo (4672), RDP, PowerShell."),
        ("UsrClass.dat (Shellbags)", "AppData\\Local", "parse_shellbags (SBECmd)", "Chứng minh kẻ tấn công duyệt thư mục (kể cả đã xóa)."),
        (".lnk & Jumplists", "Recent, AutomaticDestinations", "parse_lnk, parse_jumplists", "Lịch sử mở tệp gần nhất, serial ổ đĩa USB ngoài."),
        ("SRUDB.dat (SRUM)", "System32\\sru", "parse_srum (SrumECmd)", "Lượng bytes mạng gửi ra ngoài theo tiến trình (Exfiltration)."),
        (".exe, .dll, .sys (PE)", "Binary thực thi, malware", "pe_analyze, sigcheck_file", "Tính Entropy (Packer detection), Imphash, hàm WinAPI."),
        ("auth.log, .bash_history", "Linux /var/log/ & root", "analyze_linux_logs", "Phát hiện SSH brute-force, leo quyền sudo, lệnh bash."),
        (".dmp, .raw (RAM)", "Dump bộ nhớ RAM vật lý", "volatility_*, memprocfs_mount", "Tìm code injection (malfind), tiến trình ngầm, socket mạng."),
        (".pcap, .pcapng", "Lưu lượng bắt gói tin mạng", "tshark_*", "Phân tích hội thoại TCP, truy vấn DNS lạ, TLS SNI.")
    ]
    for r_data in rows:
        row = t_sans.add_row()
        for idx, text in enumerate(r_data):
            c = row.cells[idx]
            set_cell_background(c, "F8FAFC" if len(t_sans.rows) % 2 == 0 else "FFFFFF")
            set_cell_margins(c, 40, 40, 60, 60)
            p = c.paragraphs[0]; p.paragraph_format.space_after = Pt(0)
            r = p.add_run(text); r.font.size = Pt(8)
            if idx == 0: r.font.bold = True

    # 5. Training Skills
    add_h("5. HƯỚNG DẪN THÊM VÀ HUẤN LUYỆN TRI THỨC CHO AI (SKILL.MD)")
    p = doc.add_paragraph()
    p.add_run("• Vị trí lưu trữ tri thức: Mọi kỹ năng của AI được lưu tại E:\\Hunting-Forensics\\skills\\<tên-kỹ-năng>\\SKILL.md.\n"
              "• Cơ chế hoạt động: Khi V-AutoFor khởi động, nó tự động quét thư mục skills. Mỗi tệp SKILL.md bao gồm phần Frontmatter YAML mô tả tình huống kích hoạt, danh sách QUY TẮC BẮT BUỘC, quy trình SOP từng bước và định dạng báo cáo đầu ra.\n"
              "• Thêm kỹ năng mới: Để huấn luyện AI điều tra một loại tấn công mới (như Ransomware hay Cloud Forensics), chỉ cần tạo thư mục và file SKILL.md tương ứng. Hệ thống sẽ tự động học và áp dụng ngay trong phiên làm việc tiếp theo.")

    # 6. FirstHack Case Study
    add_h("6. KỊCH BẢN THỰC HÀNH ĐIỀU TRA MẪU FIRSTHACK.AD1")
    p = doc.add_paragraph()
    p.add_run("• Bước 1: Khởi động hệ thống kép bằng lệnh v-autofor.\n"
              "• Bước 2: Prompt tại Port 8787 yêu cầu xác minh tính toàn vẹn ➔ AI gọi verify_evidence_integrity, băm SHA-256 (130d91294aaa...), đối soát metadata, sự kiện hiển thị trên ForBrain Port 5000.\n"
              "• Bước 3: Prompt yêu cầu trích xuất dữ liệu ➔ AI gọi ad1_extract, bung toàn bộ 1.831 file ra thư mục extracted trong 17.6s.\n"
              "• Bước 4: Prompt yêu cầu phân tích log ➔ AI gọi analyze_linux_logs, phát hiện kẻ tấn công KarenHacker leo quyền sudo (sudo visudo) và các câu lệnh thực thi script nguy hiểm trong .bash_history.\n"
              "• Bước 5: Prompt yêu cầu xuất báo cáo ➔ AI sinh Báo cáo DFIR hoàn chỉnh chuẩn ISO/IEC 27037 & NIST SP 800-86 gồm 8 phần.")

    # 7. Safe maintenance
    add_h("7. BẢO TRÌ, DỌN DẸP RÁC VÀ TẮT HỆ THỐNG AN TOÀN")
    p = doc.add_paragraph()
    p.add_run("• Tắt hệ thống: Gõ lệnh v-autofor-stop để giải phóng hoàn toàn hai cổng mạng 8787 và 5000.\n"
              "• Dọn dẹp an toàn: Đã loại bỏ các tệp rác như web_backup (28MB), crash dumps, file docx trùng lặp và 13 thư mục __pycache__. Quy trình này bảo đảm không ảnh hưởng đến bất kỳ luồng hoạt động nào của hệ thống.")

    out = Path(r"E:\Hunting-Forensics\Bao_Cao_Kien_Truc_va_Van_Hanh_V-AutoFor.docx")
    doc.save(str(out))
    print(f"DOCX Report successfully saved to {out} (Size: {out.stat().st_size} bytes)")

if __name__ == "__main__":
    generate_docx()
