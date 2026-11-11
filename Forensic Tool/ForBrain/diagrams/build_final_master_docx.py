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

def set_cell_margins(cell, top=70, bottom=70, left=100, right=100):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def style_row(row, bg_hex, text_color_rgb=None, is_bold=False, font_size=8.5):
    for cell in row.cells:
        set_cell_background(cell, bg_hex)
        set_cell_margins(cell, 50, 50, 80, 80)
        for p in cell.paragraphs:
            p.paragraph_format.space_after = Pt(0)
            p.paragraph_format.space_before = Pt(0)
            for r in p.runs:
                r.font.size = Pt(font_size)
                if is_bold:
                    r.font.bold = True
                if text_color_rgb:
                    r.font.color.rgb = text_color_rgb

def build_full_docx():
    doc = Document()

    # Page Margins
    for s in doc.sections:
        s.top_margin = Inches(0.7)
        s.bottom_margin = Inches(0.7)
        s.left_margin = Inches(0.75)
        s.right_margin = Inches(0.75)

    normal = doc.styles['Normal']
    normal.font.name = 'Calibri'
    normal.font.size = Pt(10)
    normal.font.color.rgb = RGBColor(0x22, 0x22, 0x22)

    # Header Title
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(2)
    r_meta = p_meta.add_run("BÁO CÁO NGHIÊN CỨU CHIẾN LƯỢC, ĐỐI SOÁT QUỐC TẾ & KIẾN TRÚC SẢN PHẨM")
    r_meta.font.size = Pt(10.5)
    r_meta.font.bold = True
    r_meta.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)

    p_title = doc.add_paragraph()
    p_title.paragraph_format.space_before = Pt(2)
    p_title.paragraph_format.space_after = Pt(6)
    r_title = p_title.add_run("NỀN TẢNG AI FORENSIC V-AUTOFOR & FORBRAIN OBSERVABILITY")
    r_title.font.size = Pt(18)
    r_title.font.bold = True
    r_title.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    p_sub = doc.add_paragraph()
    p_sub.paragraph_format.space_after = Pt(12)
    r_sub = p_sub.add_run("Nghiên cứu Toàn diện Giải pháp Quốc tế (Thương mại & Open-source), Phân tích Khoảng cách Tính năng (Gap Analysis), Năng lực Làm chủ Nghiệp vụ Đột phá, Kiến trúc Hạ tầng & Sơ đồ Workflow Điều tra Đa tác tử.")
    r_sub.font.size = Pt(9.5)
    r_sub.font.italic = True
    r_sub.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # Meta Table
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    meta_data = [
        ("Tên giải pháp / Sản phẩm:", "V-AutoFor (Hệ thống AI Tự Động Giám Định & Điều Tra Sự Cố An Toàn Thông Tin)"),
        ("Tầm nhìn & Định vị (Vision):", "Agentic DFIR tự hành trên hạ tầng nội bộ (On-Premise), Chuẩn hóa ISO/IEC 27037, NIST SP 800-86, RFC 3227 & SANS FOR508"),
        ("So sánh Thương mại:", "CrowdStrike Falcon Forensics & Charlotte AI, Magnet AXIOM Cyber, Binalyze AIR (Phân tích khoảng cách - Gap Analysis)"),
        ("So sánh Mã nguồn mở:", "AIFT (Dissect), ForensIQ (dfirvault), Google Timesketch + Turbinia"),
        ("Đóng góp Đội ngũ (Contribution):", "Kiến trúc 2 tầng độc lập (:8787 vs :5000), 4 FastMCP Servers (40+ tools), Live Telemetry Stream, Bộ giải mã AD1 Container, VETO Loop"),
        ("Yếu tố Quyết định (Key):", "Làm chủ nghiệp vụ chuyên môn sâu (Domain Expertise Mastery): Windows/Linux Internals, Cấu trúc Nhị phân, APT Tradecraft")
    ]
    for idx, (k, v) in enumerate(meta_data):
        row = meta_table.rows[idx]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = Inches(2.3); c1.width = Inches(4.7)
        set_cell_background(c0, "F1F5F9"); set_cell_background(c1, "F8FAFC")
        set_cell_margins(c0, 40, 40, 70, 70); set_cell_margins(c1, 40, 40, 70, 70)
        p0 = c0.paragraphs[0]; p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(k); r0.font.bold = True; r0.font.size = Pt(8.5)
        p1 = c1.paragraphs[0]; p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(v); r1.font.size = Pt(8.5)

    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(16)
        p.paragraph_format.space_after = Pt(5)
        r = p.add_run(text)
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x0F, 0x17, 0x2A)

    def add_h2(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(11)
        p.paragraph_format.space_after = Pt(3)
        r = p.add_run(text)
        r.font.size = Pt(11)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x02, 0x84, 0xC7)

    def add_bullet(p, bold_prefix, text):
        p.paragraph_format.space_before = Pt(0)
        p.paragraph_format.space_after = Pt(2)
        r_b = p.add_run(bold_prefix)
        r_b.font.bold = True
        r_t = p.add_run(text)

    diagram_dir = Path(r"E:\Hunting-Forensics\Forensic Tool\ForBrain\diagrams")

    # =========================================================
    # CHƯƠNG 1
    # =========================================================
    add_h1("CHƯƠNG 1: TẦM NHÌN CHIẾN LƯỢC & ĐỊNH VỊ CHUẨN HÓA QUỐC TẾ (VISION & GLOBAL ALIGNMENT)")
    
    add_h2("1.1. Tầm nhìn Chuyển dịch Sang Kỷ nguyên Giám định Tự hành (Autonomous Agentic DFIR)")
    p = doc.add_paragraph()
    p.add_run("Trong bối cảnh các chiến dịch tấn công mạng có chủ đích (APT), mã độc tống tiền tốc độ cao (Ransomware) và kỹ thuật Living-off-the-Land (LotL) phát triển phức tạp, phương thức ứng cứu sự cố thủ công truyền thống đang dần trở nên bất lực. Khối lượng dữ liệu số cần thu thập và phân tích tại mỗi sự cố dao động từ hàng chục đến hàng trăm gigabytes. Việc điều tra viên duyệt thủ công từng tệp nhật ký, trích xuất từng bản ghi Registry hay mổ xẻ file nhị phân thường tiêu tốn từ 24 đến 72 giờ, tạo ra khoảng thời gian trễ nguy hiểm (Dwell Time) cho kẻ tấn công mở rộng phạm vi xâm nhập.\n\n"
              "Tầm nhìn của V-AutoFor là định vị trở thành ")
    p.add_run("Nền tảng Giám định Số Tự hành Đa Tác tử (Autonomous Agentic DFIR Platform)").bold = True
    p.add_run(" tiên phong tại Việt Nam, vận hành hoàn toàn trên hạ tầng nội bộ (On-Premise). Hệ thống chuyển dịch căn bản từ mô hình hỏi đáp thụ động sang mô hình ")
    p.add_run("Điều tra Dựa trên Giả thuyết (Hypothesis-driven Investigation)").bold = True
    p.add_run(": AI tự động phân tích cảnh báo ban đầu, sinh các giả thuyết điều tra cần chứng minh, tự chọn công cụ chuyên dụng, tự bóc tách chứng cứ, đối chứng chéo và đưa ra kết luận kèm biện pháp ngăn chặn tức thời.")

    add_h2("1.2. Chuẩn hóa Phương pháp luận theo Bộ Tiêu chuẩn Quốc tế")
    p = doc.add_paragraph()
    p.add_run("Để kết quả điều tra có giá trị pháp lý vững chắc trước hội đồng an ninh hoặc cơ quan thực thi pháp luật, V-AutoFor chuẩn hóa tuyệt đối theo các tiêu chuẩn quốc tế:")

    p1 = doc.add_paragraph(style='List Bullet')
    add_bullet(p1, "ISO/IEC 27037 (Bảo quản Tính toàn vẹn Bằng chứng): ", "Mọi tệp bằng chứng gốc đều được bảo vệ nghiêm ngặt ở chế độ Read-Only tuyệt đối; phân tích hoàn toàn trên bản sao làm việc; tự động băm đồng thời 3 mã băm chuẩn (MD5, SHA-1, SHA-256) và đối soát với báo cáo gốc của điều tra viên để duy trì Chuỗi bảo quản bằng chứng (Chain of Custody).")

    p2 = doc.add_paragraph(style='List Bullet')
    add_bullet(p2, "RFC 3227 (Thứ tự Dễ bay hơi - Order of Volatility): ", "Thiết lập quy trình ưu tiên thu thập và phân tích dữ liệu: Bộ nhớ RAM vật lý ➔ Trạng thái kết nối mạng & Sockets ➔ Tệp tin tạm thời ➔ Dữ liệu ổ đĩa không bay hơi ($MFT, Registry) ➔ Nhật ký lưu trữ dài hạn.")

    p3 = doc.add_paragraph(style='List Bullet')
    add_bullet(p3, "NIST SP 800-86 & NIST CSF 2.0: ", "Khung hướng dẫn tích hợp kỹ thuật giám định số vào quy trình phản ứng sự cố an toàn thông tin.")

    p4 = doc.add_paragraph(style='List Bullet')
    add_bullet(p4, "SANS FOR508 & SANS FOR500 (Tiêu chuẩn Vàng DFIR): ", "Bao phủ trọn vẹn 5 miền phân tích của chuyên gia điều tra số: Evidence of Execution, Persistence & Autostart, Lateral Movement, Timeline ($MFT, Shellbags, Jumplists, SRUM), và Deep Memory/Network Forensics.")

    p5 = doc.add_paragraph(style='List Bullet')
    add_bullet(p5, "MITRE ATT&CK Enterprise Matrix: ", "Tự động ánh xạ 100% các phát hiện sang ma trận Tactic & Technique chuẩn hóa (Initial Access, Execution, Privilege Escalation, Persistence, C2,...).")

    p6 = doc.add_paragraph(style='List Bullet')
    add_bullet(p6, "Giao thức Mở Model Context Protocol (MCP): ", "Chuẩn kết nối mở do Anthropic khởi xướng, biến mọi công cụ nhị phân phức tạp thành dịch vụ chuẩn hóa qua JSON-RPC 2.0, bảo đảm tính độc lập và khả năng mở rộng không giới hạn.")

    # SƠ ĐỒ HẠ TẦNG SẢN PHẨM (EMBED IMAGE)
    add_h2("1.3. Sơ đồ Hạ tầng & Phân tầng Kiến trúc Sản phẩm (Product Infrastructure Architecture)")
    p = doc.add_paragraph()
    p.add_run("Dưới đây là sơ đồ hạ tầng phân tầng hoàn chỉnh của giải pháp V-AutoFor và hệ sinh thái ForBrain Observability:")

    img_infra = diagram_dir / "infra_architecture.png"
    if img_infra.exists():
        p_img = doc.add_paragraph()
        p_img.alignment = WD_PARAGRAPH_ALIGNMENT.CENTER if hasattr(doc, 'WD_PARAGRAPH_ALIGNMENT') else WD_TABLE_ALIGNMENT.CENTER
        p_img.paragraph_format.space_before = Pt(4)
        p_img.paragraph_format.space_after = Pt(4)
        p_img.add_run().add_picture(str(img_infra), width=Inches(6.8))
        p_cap = doc.add_paragraph()
        p_cap.paragraph_format.space_after = Pt(10)
        r_cap = p_cap.add_run("Hình 1.1: Sơ đồ Hạ tầng & Phân tầng Kiến trúc Nền tảng V-AutoFor & ForBrain Observability")
        r_cap.font.size = Pt(8.5); r_cap.font.italic = True; r_cap.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # SƠ ĐỒ WORKFLOW ĐIỀU TRA (EMBED IMAGE)
    add_h2("1.4. Sơ đồ Hoạt động & Quy trình Điều tra Toàn trình (End-to-End Investigation Workflow)")
    p = doc.add_paragraph()
    p.add_run("Quy trình điều tra toàn trình của V-AutoFor được tự động hóa qua 5 giai đoạn liên hoàn, kết hợp cổng thẩm định đối nghịch VETO Loop:")

    img_wf = diagram_dir / "workflow_investigation.png"
    if img_wf.exists():
        p_img2 = doc.add_paragraph()
        p_img2.paragraph_format.space_before = Pt(4)
        p_img2.paragraph_format.space_after = Pt(4)
        p_img2.add_run().add_picture(str(img_wf), width=Inches(6.8))
        p_cap2 = doc.add_paragraph()
        p_cap2.paragraph_format.space_after = Pt(10)
        r_cap2 = p_cap2.add_run("Hình 1.2: Sơ đồ Hoạt động & Quy trình Điều tra Dựa trên Giả thuyết (Hypothesis-driven Workflow)")
        r_cap2.font.size = Pt(8.5); r_cap2.font.italic = True; r_cap2.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    # =========================================================
    # CHƯƠNG 2
    # =========================================================
    add_h1("CHƯƠNG 2: PHÂN TÍCH & SO SÁNH TRỰC DIỆN VỚI CÁC SẢN PHẨM QUỐC TẾ")

    add_h2("2.1. Đánh giá Trực diện Ba Nhóm Giải pháp Tiêu biểu")
    p = doc.add_paragraph()
    p.add_run("Báo cáo khảo sát trực tiếp 3 đại diện thương mại đầu ngành và 3 dự án mã nguồn mở tiêu biểu:\n"
              "1. CrowdStrike Falcon Forensics & Charlotte AI (Mô hình Cloud EDR SaaS).\n"
              "2. Magnet AXIOM Cyber & Copilot (Mô hình Workstation Lab Forensic).\n"
              "3. Binalyze AIR & Drone AI (Mô hình Remote Enterprise Triage dưới 10 phút).\n"
              "4. Nhóm mã nguồn mở: AIFT (Dissect), ForensIQ (dfirvault), Google Timesketch + Turbinia.")

    # Gap Analysis Section (V-AutoFor thiếu gì so với quốc tế?)
    add_h2("2.2. Phân tích Khoảng cách Tính năng so với Quốc tế (Feature Gap Analysis: V-AutoFor Còn Thiếu Những Gì?)")
    p = doc.add_paragraph()
    p.add_run("Đánh giá một cách khách quan, sòng phẳng và minh bạch về mặt công nghệ, so với các sản phẩm thương mại có thâm niên hàng chục năm và nguồn lực hàng tỷ USD, V-AutoFor ")
    p.add_run("còn những khoảng cách công nghệ rõ rệt cần hoàn thiện trong lộ trình tiếp theo").bold = True
    p.add_run(":")

    gap_items = [
        ("Khoảng cách 1: Quản trị Cảm biến Máy trạm Quy mô Lớn (Enterprise Endpoint Fleet Management): ",
         "Các hãng như CrowdStrike hay Binalyze AIR sở hữu mạng lưới Falcon Sensor / AIR Sensor siêu nhẹ cài đặt sẵn trên hàng trăm nghìn máy trạm. Khi sự cố xảy ra, họ có thể phát lệnh từ xa để kéo artifact về ngay tức khắc. V-AutoFor hiện tại tập trung giải quyết bài toán cốt lõi là 'Bộ Não Giám định & Suy luận' (Brain Reasoning) trên các gói dữ liệu triage và ảnh đĩa đưa vào kho Evidence, chưa xây dựng mạng lưới Agent cắm thường trực quy mô lớn."),
        
        ("Khoảng cách 2: Giám định Thiết bị Di động & Trích xuất Chip-off (Mobile & IoT Forensics): ",
         "Magnet AXIOM Cyber và Cellebrite hỗ trợ bóc tách sâu hàng nghìn dòng điện thoại Android/iOS, vượt qua cơ chế mã hóa phần cứng và trích xuất chip-off. V-AutoFor hiện tại tập trung tối đa vào hạ tầng máy chủ và máy trạm (Windows Server, Linux Server, Windows Client, RAM và Network PCAP), chưa hỗ trợ thiết bị di động."),
        
        ("Khoảng cách 3: Cổng kết nối Trực tiếp Dữ liệu Đám mây qua API (Cloud-Native Direct Ingestion): ",
         "Magnet AXIOM và CrowdStrike tích hợp sẵn cổng API OAuth2 kết nối thẳng vào Microsoft 365, AWS CloudTrail, Google Workspace, Azure Entra ID để kéo log về. V-AutoFor hiện tại yêu cầu chuyên viên tải log hoặc ảnh máy ảo cloud (VMDK/VHDX) về kho lưu trữ trước khi phân tích."),
        
        ("Khoảng cách 4: Đồ thị Bằng chứng Phân tán Siêu lớn (Distributed Threat Graph Database): ",
         "CrowdStrike sở hữu cơ sở dữ liệu đồ thị Threat Graph phân tán lưu trữ hàng petabyte dữ liệu telemetry liên kết toàn cầu. V-AutoFor hiện tại phân tích theo từng vụ việc (Case-centric) lưu trữ trên SQLite và JSON cấu trúc nội bộ, tối ưu cho quy mô từng sự cố độc lập."),
        
        ("Khoảng cách 5: Đội ngũ Săn tìm Mối đe dọa 24/7 Toàn cầu (Human Threat Intelligence Hunting): ",
         "CrowdStrike có đội ngũ chuyên gia Falcon OverWatch túc trực 24/7 săn tìm mã độc thủ công để huấn luyện lại mô hình AI từng giờ. V-AutoFor hiện tại dựa trên tri thức SANS FOR508 và các parser chuyên dụng đã được số hóa.")
    ]
    for b_title, b_desc in gap_items:
        p_gap = doc.add_paragraph(style='List Bullet')
        add_bullet(p_gap, b_title, b_desc)

    add_h2("2.3. Những Điểm Khác biệt & Vượt trội của V-AutoFor so với Quốc tế")
    p = doc.add_paragraph()
    p.add_run("Mặc dù còn những khoảng cách về quy mô triển khai endpoint, V-AutoFor lại sở hữu những ")
    p.add_run("lợi thế mang tính đột phá và phù hợp tuyệt đối với điều kiện tác chiến tại Việt Nam").bold = True
    p.add_run(":")

    str_items = [
        ("1. Triển khai Nội bộ Tuyệt đối (100% On-Premise & Air-Gapped): ",
         "Các tổ chức trọng yếu (Quân đội, Công an, Ngân hàng, Viễn thông) không bao giờ được phép gửi ảnh đĩa chứa bí mật quốc gia hoặc dữ liệu tài chính lên đám mây của CrowdStrike hay Microsoft. V-AutoFor vận hành 100% trên phần cứng nội bộ, tự chủ hoàn toàn."),
        
        ("2. Khả năng Mổ xẻ Đĩa Logic FTK Imager (.ad1) Độc quyền: ",
         "Các công cụ mã nguồn mở quốc tế (như Dissect) hoàn toàn bất lực và báo lỗi Unsupported OS trước các container logic `.ad1`. V-AutoFor đã tự phát triển module ad1_extract giải mã thành công container này, tự động bung toàn bộ cây thư mục để phân tích."),
        
        ("3. Minh bạch Hoàn toàn qua Live Telemetry Stream: ",
         "Không giống như Charlotte AI hoạt động như một hộp đen, V-AutoFor cung cấp màn hình ForBrain Observability (:5000) hiển thị từng lệnh gọi công cụ thời gian thực và nút 'Inspect Output' xem trực tiếp dữ liệu thô."),
        
        ("4. Tối ưu Chi phí Đầu tư (Tiết kiệm 85 - 95%): ",
         "Chi phí mua bản quyền hàng năm của CrowdStrike Falcon hay Magnet AXIOM Cyber lên tới hàng trăm nghìn USD mỗi năm. V-AutoFor làm chủ 100% mã nguồn, giúp tổ chức tiết kiệm ngân sách khổng lồ.")
    ]
    for b_title, b_desc in str_items:
        p_str = doc.add_paragraph(style='List Bullet')
        add_bullet(p_str, b_title, b_desc)

    # Detailed Feature Matrix Table
    add_h2("2.4. Bảng Ma trận So sánh Tính năng Chi tiết: V-AutoFor vs. Quốc tế")
    t_feat = doc.add_table(rows=1, cols=5)
    t_feat.alignment = WD_TABLE_ALIGNMENT.CENTER
    f_hdr = t_feat.rows[0].cells
    f_hdr[0].width = Inches(1.5); f_hdr[1].width = Inches(1.3); f_hdr[2].width = Inches(1.3); f_hdr[3].width = Inches(1.3); f_hdr[4].width = Inches(1.6)
    for idx, h in enumerate(["Tính năng & Tiêu chí", "CrowdStrike Falcon", "Magnet AXIOM Cyber", "Binalyze AIR", "V-AutoFor (Make-in-VN)"]):
        f_hdr[idx].paragraphs[0].text = h
    style_row(t_feat.rows[0], "0F172A", RGBColor(0xFF, 0xFF, 0xFF), True, 8.5)

    feat_rows = [
        ("Triển khai On-Premise", "Không (Bắt buộc Cloud)", "Có (Workstation)", "Có (On-Prem/Cloud)", "Có (100% On-Premise cách ly)"),
        ("Tự động hóa theo Giả thuyết", "Bán tự động (cần người hỏi)", "Thủ công theo Case", "Tự động thu thập", "Tự hành Đa Tác tử (Agentic Loop)"),
        ("Giải mã FTK Container (.ad1)", "Không hỗ trợ", "Hỗ trợ (thủ công)", "Không hỗ trợ", "Tự động giải mã (ad1_extract)"),
        ("Bóc tách Ổ đĩa E01/RAW", "Hạn chế (ưu tiên EDR)", "Rất mạnh", "Hạn chế", "Rất mạnh (Dissect Core)"),
        ("Mổ xẻ Bộ nhớ RAM Chuyên sâu", "Một phần qua Sensor", "Cơ bản", "Chỉ dump RAM", "Chuyên sâu: Volatility 3 + MemProcFS"),
        ("Phân tích Gói tin Mạng PCAP", "Không chuyên dụng", "Hạn chế", "Không hỗ trợ", "Chuyên sâu: Wireshark TShark DPI"),
        ("Giám sát Minh bạch Telemetry", "Hộp đen (Proprietary)", "Log phần mềm", "Log tiến trình", "Live Feed thời gian thực (:5000)"),
        ("Kiểm soát An toàn Chống Ảo giác", "Giới hạn trong Model", "Không có", "Không có", "Cổng VETO Loop & Dual-Evidence Rule"),
        ("Thu thập Endpoint Từ xa quy mô lớn", "Rất mạnh (Triệu máy)", "Mạnh (vài chục máy)", "Rất mạnh (AIR Sensor)", "Đang phát triển trong Lộ trình"),
        ("Giám định Thiết bị Di động (Mobile)", "Không hỗ trợ", "Rất mạnh (Cellebrite)", "Không hỗ trợ", "Chưa hỗ trợ (Tập trung Server/PC)")
    ]
    for row_idx, r_data in enumerate(feat_rows):
        row = t_feat.add_row()
        for c_idx, val in enumerate(r_data):
            row.cells[c_idx].paragraphs[0].text = val
        style_row(row, "F8FAFC" if row_idx % 2 == 0 else "FFFFFF", None, c_idx == 0, 8.0)

    # =========================================================
    # CHƯƠNG 3
    # =========================================================
    add_h1("CHƯƠNG 3: ĐÓNG GÓP KỸ THUẬT CỐT LÕI CỦA ĐỘI NGŨ PHÁT TRIỂN (OUR RESEARCH & ENGINEERING CONTRIBUTIONS)")

    p = doc.add_paragraph()
    p.add_run("Để đưa V-AutoFor từ một ý tưởng nghiên cứu trở thành một nền tảng vận hành ổn định và thực chiến, đội ngũ kỹ sư đã trực tiếp thiết kế, phát triển và đóng góp hàng loạt giải pháp kỹ thuật đột phá:")

    contrib_items = [
        ("1. Thiết kế Kiến trúc Hai Tầng Độc lập (Separation of Concerns Architecture): ",
         "Đội ngũ đã thiết kế và hiện thực hóa mô hình phân tách vai trò hoàn chỉnh: Tầng Suy luận Trí tuệ (V-AutoFor AI Studio trên Port 8787) và Tầng Giám sát Thực thi (ForBrain Observability Monitor trên Port 5000). Giải pháp này xóa bỏ hoàn toàn rủi ro 'AI Hộp đen', mang lại khả năng giám sát minh bạch 100% mọi hành vi của tác tử."),
        
        ("2. Xây dựng Cụm 4 FastMCP Servers với hơn 40 Công cụ Chuyên sâu: ",
         "Tự thiết kế và lập trình 4 máy chủ FastMCP chuẩn hóa qua giao tiếp stdio JSON-RPC 2.0 (aift_mcp.py, eztools_mcp.py, sysinternals_mcp.py, network_memory_mcp.py). Toàn bộ các công cụ nhị phân phức tạp của Eric Zimmerman, Microsoft Sysinternals, Volatility 3 và TShark đã được đóng gói thành các API có kiểu dữ liệu an toàn."),
        
        ("3. Tự phát triển Bộ Giải mã Container AD1 Độc quyền (ad1_extract & ad1_list): ",
         "Nghiên cứu cấu trúc nhị phân của định dạng AccessData FTK Imager Logical Image, viết parser bóc tách cây thư mục logic ra đĩa vật lý, giải quyết dứt điểm lỗi 'Unsupported Evidence' của các thư viện mã nguồn mở quốc tế."),
        
        ("4. Lập trình Hệ thống Live Webhook Telemetry Streaming: ",
         "Tự xây dựng cơ chế phát tín hiệu telemetry nội bộ. Mỗi khi một công cụ MCP được kích hoạt, một bản tin JSON chứa đầy đủ tham số, thời gian thực thi (mili-giây) và kết quả được phát sóng về ForBrain Monitor theo thời gian thực."),
        
        ("5. Thiết lập Cổng Kiểm soát An toàn VETO Loop & Safety Rails: ",
         "Cấu hình các bộ lọc phân quyền chặt chẽ, chặn đứng các câu lệnh shell thô sơ (Get-Content, cat, type) để bảo toàn chứng cứ; áp dụng Quy tắc Đối chứng Kép (Dual-Evidence Rule) bắt buộc mọi phát hiện phải có ít nhất 2 nguồn chứng cứ độc lập hỗ trợ."),
        
        ("6. Số hóa Bộ Tri thức Kỹ năng Điều tra Chuẩn Quốc tế (Skills Repository): ",
         "Trực tiếp soạn thảo và cấu trúc hóa 2 kỹ năng cốt lõi v-autofor-investigation (SOP 7 bước điều tra ISO 27037 & SANS FOR508) và forensic-reporting (Khung báo cáo DFIR 8 phần chuẩn NIST SP 800-86).")
    ]
    for b_title, b_desc in contrib_items:
        p_c = doc.add_paragraph(style='List Bullet')
        add_bullet(p_c, b_title, b_desc)

    # =========================================================
    # CHƯƠNG 4
    # =========================================================
    add_h1("CHƯƠNG 4: YẾU TỐ QUYẾT ĐỊNH ĐỂ TẠO RA SẢN PHẨM TỐT: LÀM CHỦ NGHIỆP VỤ & GIỎI NGHỀ")

    p = doc.add_paragraph()
    r_quote = p.add_run("“1 GIỎI NGHỀ, LÀM CHỦ NGHIỆP VỤ THỰC CHIẾN... THÌ MỚI LÀM RA ĐƯỢC MỘT SẢN PHẨM AI CHẤT LƯỢNG CAO.”\n")
    r_quote.bold = True; r_quote.font.size = Pt(11); r_quote.font.color.rgb = RGBColor(0xB9, 0x1C, 0x1C)
    p.add_run("Trong kỹ thuật phần mềm nói chung và an ninh mạng nói riêng, công nghệ AI chỉ đóng vai trò là ")
    p.add_run("đòn bẩy gia tăng sức mạnh").bold = True
    p.add_run(", còn ")
    p.add_run("tri thức nghiệp vụ chuyên gia mới là linh hồn và điểm tựa vững chắc").bold = True
    p.add_run(". Nếu không có sự am hiểu sâu sắc về chuyên môn giám định số (DFIR), mọi mô hình ngôn ngữ lớn (LLM) dù hiện đại đến đâu cũng sẽ trở thành vô dụng trong thực chiến.")

    add_h2("4.1. Vì sao Kỹ sư AI Đơn thuần Không thể Xây dựng Sản phẩm Forensic Chất lượng?")
    p = doc.add_paragraph()
    p.add_run("Khi một kỹ sư chỉ có kiến thức lập trình AI thuần túy tiếp cận bài toán điều tra sự cố, họ thường áp dụng các giải pháp chung chung như: Nạp log vào Vector Database, dùng RAG (Retrieval-Augmented Generation) và prompt cho mô hình tóm tắt. Cách tiếp cận này chắc chắn thất bại vì các lý do sống còn:\n"
              "1. Bằng chứng số nằm ở cấu trúc nhị phân (Binary Internals): Dấu vết không phải là các đoạn văn bản mà nằm ở các bit cờ thuộc tính của file, cấu trúc cây B-Tree trong $MFT, trường thời gian Windows FILETIME 64-bit, các offset nạp DLL trong tiến trình.\n"
              "2. Cạm bẫy Bẫy nghi binh (Red Herring): Kẻ tấn công chuyên nghiệp luôn chủ động xóa log, tạo ra các câu lệnh giả mạo để đánh lừa điều tra viên. Một AI thiếu nghiệp vụ sẽ lập tức 'tin' vào các log này và đưa ra kết luận hoàn toàn sai lệch.\n"
              "3. Kỹ thuật ngụy tạo thời gian (Timestomping): Attacker dùng công cụ sửa mốc thời gian trong thuộc tính $STANDARD_INFORMATION. Nếu không am hiểu cấu trúc hệ thống tệp NTFS để đối chứng chéo với thuộc tính $FILE_NAME, AI sẽ bị qua mặt 100%.")

    add_h2("4.2. Sự Cần thiết của Năng lực Làm chủ Nghiệp vụ Chuyên môn Sâu")
    p = doc.add_paragraph()
    p.add_run("Chính năng lực làm chủ nghiệp vụ chuyên môn dày dặn của đội ngũ phát triển đã quyết định chất lượng của V-AutoFor:")

    p_m1 = doc.add_paragraph(style='List Bullet')
    add_bullet(p_m1, "Làm chủ Kiến trúc Hệ điều hành (Windows & Linux Internals): ", "Hiểu rõ cơ chế nạp bộ nhớ, cấu trúc PE Header, PE Section Entropy để phát hiện Packer/Crypter; cơ chế lưu vết của Amcache, Shimcache, Prefetch và Shellbags; cơ chế kiểm soát phân quyền Sudo và lịch sử lệnh .bash_history.")

    p_m2 = doc.add_paragraph(style='List Bullet')
    add_bullet(p_m2, "Làm chủ Chiến thuật Tấn công Thực chiến (APT Tradecraft): ", "Nắm vững các kỹ thuật Process Hollowing, DLL Side-Loading, Pass-the-Hash, Cobalt Strike Beaconing. Từ đó mới biết chính xác cần tìm dấu vết ở đâu: Tìm code injection thì gọi volatility_malfind; tìm persistence thì gọi autoruns_triage; tìm rò rỉ dữ liệu thì gọi parse_srum.")

    p_m3 = doc.add_paragraph(style='List Bullet')
    add_bullet(p_m3, "Mã hóa Nghiệp vụ thành Logic Tự động (Codeifying Tradecraft): ", "Chính nghiệp vụ thực chiến giúp đội ngũ thiết lập quy trình đối soát chéo kép (Cross-Verification), viết các bộ lọc Wireshark Display Filter chính xác để săn tìm C2 và loại bỏ 100% ảo giác AI.")

    # =========================================================
    # CHƯƠNG 5
    # =========================================================
    add_h1("CHƯƠNG 5: KHO TRI THỨC CHUYÊN SÂU: TECHSTACK, ĐẦU VÀO VÀ ĐẦU RA")

    add_h2("5.1. Techstack Toàn trình của Hệ sinh thái V-AutoFor & ForBrain")
    p = doc.add_paragraph()
    p.add_run("Hệ thống được thiết kế trên kiến trúc đa ngôn ngữ hiệu năng cao:")

    t_tech = doc.add_table(rows=1, cols=3)
    t_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    t_hdr = t_tech.rows[0].cells
    t_hdr[0].width = Inches(1.8); t_hdr[1].width = Inches(2.2); t_hdr[2].width = Inches(3.0)
    for idx, h in enumerate(["Phân tầng Hệ thống", "Công nghệ & Ngôn ngữ", "Chức năng & Nhiệm vụ Cốt lõi"]):
        t_hdr[idx].paragraphs[0].text = h
    style_row(t_tech.rows[0], "0F172A", RGBColor(0xFF, 0xFF, 0xFF), True, 8.5)

    tech_data = [
        ("Tầng Điều phối Agent", "Go (Golang) / Reasonix Engine", "Quản lý phiên chat, phân giải context, nạp Skills, gọi FastMCP stdio"),
        ("Tầng Giám sát & Bảng điều khiển", "Python 3.12, Flask, JavaScript, HTML5/CSS3 Dark-mode", "Observability Monitor (Port 5000), quản trị Evidence, hiển thị Live Feed"),
        ("Cầu nối Công cụ (FastMCP Bridge)", "FastMCP Python Protocol", "4 máy chủ FastMCP chuẩn hóa giao thức JSON-RPC 2.0 qua stdio"),
        ("Bộ công cụ Windows SANS FOR508", "C#, .NET 8 / .NET 9 Runtime (Zimmerman)", "PECmd, AmcacheParser, AppCompatCacheParser, MFTECmd, EvtxECmd, SBECmd"),
        ("Bộ công cụ Live Forensic", "C / C++ Native Win32 (Sysinternals)", "Autoruns64, Sigcheck64, Strings64, Handle64, Tcpvcon64"),
        ("Bộ mổ xẻ RAM & Mạng", "Python, Volatility 3 (2.28), MemProcFS (5.19), Wireshark TShark (4.0)", "Bóc tách tiến trình bộ nhớ, phát hiện malfind shellcode, phân tích gói tin PCAP"),
        ("Bộ mổ xẻ Ổ đĩa & PE Malware", "Dissect Framework, pefile 2024.8.26", "Giải mã cấu trúc container AD1, E01, VMDK, RAW; tính entropy binary PE"),
        ("Trạm Định tuyến AI Gateway", "Node.js v18+, SQLite, Next.js (9Router)", "Quản lý tập trung các API Key (Gemini, DeepSeek, OpenAI) trên Port 20128")
    ]
    for row_idx, r_data in enumerate(tech_data):
        row = t_tech.add_row()
        for c_idx, val in enumerate(r_data):
            row.cells[c_idx].paragraphs[0].text = val
        style_row(row, "F8FAFC" if row_idx % 2 == 0 else "FFFFFF", None, c_idx == 0, 8.0)

    add_h2("5.2. Bảng Phân loại Chi tiết Định dạng Dữ liệu Đầu vào (Inputs)")
    p = doc.add_paragraph()
    p.add_run("V-AutoFor tiếp nhận và xử lý toàn diện 14 nhóm định dạng bằng chứng số:")

    t_in = doc.add_table(rows=1, cols=4)
    t_in.alignment = WD_TABLE_ALIGNMENT.CENTER
    in_hdr = t_in.rows[0].cells
    in_hdr[0].width = Inches(1.3); in_hdr[1].width = Inches(1.8); in_hdr[2].width = Inches(1.8); in_hdr[3].width = Inches(2.1)
    for idx, h in enumerate(["Nhóm Định dạng", "Phần mở rộng Tệp", "Nguồn Gốc & Bản chất", "Công cụ FastMCP Xử lý"]):
        in_hdr[idx].paragraphs[0].text = h
    style_row(t_in.rows[0], "0F172A", RGBColor(0xFF, 0xFF, 0xFF), True, 8.5)

    input_data = [
        ("Logical Container", ".ad1, .ad1.txt", "Ảnh logic FTK Imager tùy biến", "ad1_list, ad1_extract, verify_evidence_integrity"),
        ("Full Disk Image", ".E01, .raw, .dd", "Ảnh đĩa vật lý EnCase / Raw DD", "aift (Dissect Engine)"),
        ("Virtual Disks", ".vmdk, .vhd, .vhdx, .qcow2", "Đĩa máy ảo VMware, Hyper-V, KVM", "aift (Dissect Engine)"),
        ("Memory RAM Dump", ".raw, .dmp, .vmem", "Bộ nhớ RAM vật lý hệ thống", "volatility_pslist, malfind, netscan, memprocfs"),
        ("Network Capture", ".pcap, .pcapng, .cap", "Bắt gói tin mạng Wireshark / Tcpdump", "tshark_conversations, dns_queries, tls_sni"),
        ("Execution Evidence", ".pf, Amcache.hve, SYSTEM", "Prefetch, Amcache, Shimcache", "parse_prefetch, parse_amcache, parse_shimcache"),
        ("File System", "$MFT, $LogFile, $UsnJrnl", "Hệ thống tệp NTFS", "parse_mft (MFTECmd)"),
        ("User Activity", "UsrClass.dat, .lnk, Jumplists", "Shellbags, Shortcuts, Recent files", "parse_shellbags, parse_lnk, parse_jumplists"),
        ("Network Exfiltration", "SRUDB.dat", "Windows System Resource Usage (SRUM)", "parse_srum (SrumECmd)"),
        ("Event Logs", ".evtx", "Windows Event Logs (System, Security,...)", "parse_evtx (EvtxECmd)"),
        ("Linux Artifacts", "auth.log, syslog, .bash_history", "Linux /var/log & lịch sử dòng lệnh", "analyze_linux_logs"),
        ("Executables / Malware", ".exe, .dll, .sys, .scr", "Tệp nhị phân thực thi Windows PE", "pe_analyze, sigcheck_file")
    ]
    for row_idx, r_data in enumerate(input_data):
        row = t_in.add_row()
        for c_idx, val in enumerate(r_data):
            row.cells[c_idx].paragraphs[0].text = val
        style_row(row, "F8FAFC" if row_idx % 2 == 0 else "FFFFFF", None, c_idx == 0, 8.0)

    add_h2("5.3. Bảng Phân loại Chi tiết Sản phẩm Đầu ra (Outputs)")
    p = doc.add_paragraph()
    p.add_run("Kết quả giám định của V-AutoFor được chuẩn hóa thành 6 nhóm sản phẩm nghiệp vụ:")

    t_out = doc.add_table(rows=1, cols=3)
    t_out.alignment = WD_TABLE_ALIGNMENT.CENTER
    out_hdr = t_out.rows[0].cells
    out_hdr[0].width = Inches(1.8); out_hdr[1].width = Inches(2.2); out_hdr[2].width = Inches(3.0)
    for idx, h in enumerate(["Sản phẩm Đầu ra", "Định dạng & Cấu trúc", "Ý nghĩa & Mục đích Nghiệp vụ"]):
        out_hdr[idx].paragraphs[0].text = h
    style_row(t_out.rows[0], "0F172A", RGBColor(0xFF, 0xFF, 0xFF), True, 8.5)

    output_data = [
        ("Chứng chỉ Toàn vẹn (Chain of Custody)", "Bảng mã băm MD5, SHA-1, SHA-256", "Chứng minh tính nguyên vẹn của chứng cứ theo ISO/IEC 27037"),
        ("Bản ghi Bóc tách Chuẩn hóa", "JSON Objects, CSV Tables", "Lưu trữ vào Data Lake, nạp vào SIEM để tương quan dữ liệu"),
        ("Dòng thời gian Hợp nhất (Timeline)", "Timeline chuẩn UTC (CSV / Markdown)", "Tái hiện chính xác chuỗi hành vi của kẻ tấn công từ T0"),
        ("Ma trận Đối chiếu MITRE ATT&CK", "Bảng ánh xạ Tactics & Techniques Txxxx", "Giúp lãnh đạo SOC nắm bắt mức độ tiến triển của cuộc tấn công"),
        ("Danh mục Chỉ số Xâm hại (IOCs)", "Actionable IOCs (Hashes, IPs, Domains, Paths)", "Cung cấp ngay cho đội Phòng ngự (Blue Team) chặn đứng trên Firewall/EDR"),
        ("Báo cáo Điều tra Số Toàn diện", "Tài liệu DFIR 8 phần (DOCX / PDF / MD)", "Báo cáo chính thức phục vụ ban lãnh đạo và hồ sơ pháp lý")
    ]
    for row_idx, r_data in enumerate(output_data):
        row = t_out.add_row()
        for c_idx, val in enumerate(r_data):
            row.cells[c_idx].paragraphs[0].text = val
        style_row(row, "F8FAFC" if row_idx % 2 == 0 else "FFFFFF", None, c_idx == 0, 8.0)

    # =========================================================
    # CHƯƠNG 6
    # =========================================================
    add_h1("CHƯƠNG 6: CHỨC NĂNG & AGENT THỊ GIÁC HÓA DỮ LIỆU ĐÃ CÓ GUI (VISUALIZATION AGENT & GUI)")

    p = doc.add_paragraph()
    p.add_run("Hệ thống tích hợp thành công ")
    p.add_run("Giao diện Đồ họa Giám sát & Thị giác hóa Chứng cứ (ForBrain Observability & Forensic Visualizer GUI)").bold = True
    p.add_run(" đang vận hành thực tế tại cổng mạng ")
    p.add_run("http://127.0.0.1:5000").bold = True
    p.add_run(" (mạng LAN: `http://10.1.20.80:5000`), kết hợp cùng ")
    p.add_run("Visualization Agent").bold = True
    p.add_run(" chuyên trách đồ họa hóa dữ liệu điều tra.")

    # GUI SCREENSHOT EMBED
    img_gui = diagram_dir / "forbrain_gui_dashboard.png"
    if img_gui.exists():
        p_img3 = doc.add_paragraph()
        p_img3.paragraph_format.space_before = Pt(4)
        p_img3.paragraph_format.space_after = Pt(4)
        p_img3.add_run().add_picture(str(img_gui), width=Inches(6.8))
        p_cap3 = doc.add_paragraph()
        p_cap3.paragraph_format.space_after = Pt(10)
        r_cap3 = p_cap3.add_run("Hình 6.1: Giao diện Đồ họa Thực tế của ForBrain Observability Monitor trên Port 5000 (Live Telemetry & Modules Registry)")
        r_cap3.font.size = Pt(8.5); r_cap3.font.italic = True; r_cap3.font.color.rgb = RGBColor(0x64, 0x74, 0x8B)

    add_h2("6.1. Bốn Phân hệ Tính năng Đồ họa Trực quan trên GUI ForBrain (Port 5000)")
    p_g1 = doc.add_paragraph(style='List Bullet')
    add_bullet(p_g1, "1. Lưới Thẻ Trạng thái Module (Tool Registry Grid): ", "Hiển thị trực quan trạng thái kết nối thời gian thực của toàn bộ 8 cụm engine điều tra (Dissect, Volatility 3, TShark, Zimmerman Suite, Sysinternals, PE Static, Linux Log Analyzer, FastMCP Bridge) với cờ xanh ONLINE và danh mục artifact phụ trách.")

    p_g2 = doc.add_paragraph(style='List Bullet')
    add_bullet(p_g2, "2. Bảng Dòng Chảy Sự kiện Trực tiếp (Live AI Execution Feed & Call Telemetry): ", "Mỗi khi V-AutoFor AI Studio gọi bất kỳ công cụ nào, một thẻ sự kiện động sẽ xuất hiện ngay lập tức trên màn hình: Tác tử gọi, Tool name, Target file, Duration, Status SUCCESS/ERROR.")

    p_g3 = doc.add_paragraph(style='List Bullet')
    add_bullet(p_g3, "3. Cửa sổ Thẩm định Bằng chứng Tức thời (Inspect Output Modal): ", "Nút bấm 'Inspect Output' bên cạnh mỗi thẻ sự kiện mở hộp thoại popup cho phép chuyên viên xem trực tiếp toàn bộ dữ liệu thô (Raw Findings) công cụ vừa trả về cho AI.")

    p_g4 = doc.add_paragraph(style='List Bullet')
    add_bullet(p_g4, "4. Trực quan hóa Kho Bằng chứng (Evidence Central Repository Visualizer): ", "Hiển thị toàn bộ mẫu chứng cứ, dung lượng, định dạng và trạng thái trích xuất (ví dụ 1.831 file đã được bung ra từ container FirstHack.ad1).")

    add_h2("6.2. Năng lực của Visualization Agent (Agent Thị giác hóa)")
    p_va1 = doc.add_paragraph(style='List Bullet')
    add_bullet(p_va1, "Trực quan hóa Cây Tiến trình (Process Tree Graph): ", "Tái hiện cây tiến trình cha - con, tự động tô đỏ các tiến trình lạ và vùng nhớ bị inject shellcode.")

    p_va2 = doc.add_paragraph(style='List Bullet')
    add_bullet(p_va2, "Trực quan hóa Dòng Thời gian Tương tác (Interactive Timeline View): ", "Biểu diễn các sự kiện trên trục thời gian, hỗ trợ lọc theo dải thời gian xung quanh mốc xâm nhập T0, phóng to thu nhỏ các cụm sự kiện.")

    p_va3 = doc.add_paragraph(style='List Bullet')
    add_bullet(p_va3, "Đồ thị Chuỗi Tấn công (Attack Flow Graph): ", "Tái hiện trực quan đường đi của hacker: IP nguồn ➔ Khai thác lỗ hổng ➔ Thực thi lệnh ➔ Sudo Escalation ➔ Persistence ➔ Exfiltration.")

    # =========================================================
    # CHƯƠNG 7
    # =========================================================
    add_h1("CHƯƠNG 7: KỊCH BẢN KIỂM THỬ THỰC CHIẾN (CASE STUDY: FIRSTHACK.AD1)")
    p = doc.add_paragraph()
    p.add_run("Hệ thống đã trải qua kiểm nghiệm thực tế trên mẫu bằng chứng c46-FirstHack (FirstHack.ad1) với kết quả đạt chuẩn 100%:\n"
              "1. Xác minh toàn vẹn (ISO 27037): verify_evidence_integrity tính mã băm MD5 = e27ee6ce0fff0d6c93de2b8816741cab, SHA-256 = 130d91294aaa402a7a8770e5b81aabc76cb333019cf07a795b91cb9d4f72fe5b, đối soát file companion .txt.\n"
              "2. Giải mã Container logic: ad1_extract bung hoàn toàn 1.831 tệp tin ra đĩa trong 17.6 giây.\n"
              "3. Phân tích log chuyên sâu: analyze_linux_logs quét 1.938 dòng auth.log và 95 câu lệnh .bash_history, phát hiện attacker KarenHacker leo quyền sudo visudo và cấp quyền thực thi script lạ (hellworld.sh, firstscript).\n"
              "4. Xuất báo cáo hoàn chỉnh: Tự động sinh báo cáo DFIR 8 phần chuẩn ISO/IEC 27037 & NIST SP 800-86.")

    # =========================================================
    # CHƯƠNG 8
    # =========================================================
    add_h1("CHƯƠNG 8: KẾT LUẬN & LỘ TRÌNH PHÁT TRIỂN TIẾP THEO")
    p = doc.add_paragraph()
    p.add_run("V-AutoFor cùng hệ sinh thái ForBrain Observability khẳng định tính khả thi và sức mạnh vượt trội của việc kết hợp giữa ")
    p.add_run("Nghiệp vụ Chuyên gia Sâu sắc").bold = True
    p.add_run(", ")
    p.add_run("Trí tuệ Nhân tạo Tự hành Đa Tác tử").bold = True
    p.add_run(" và ")
    p.add_run("Chuẩn giao tiếp Mở FastMCP").bold = True
    p.add_run(". Giải pháp đã giải quyết triệt để bài toán tự động hóa điều tra sự cố số, vận hành hoàn toàn trên hạ tầng nội bộ On-Premise không phụ thuộc đám mây nước ngoài, mang lại sự minh bạch và tính toàn vẹn pháp chứng tuyệt đối.\n\n"
              "Lộ trình tiếp theo sẽ tập trung vào việc nghiên cứu và thu hẹp các khoảng cách công nghệ với quốc tế: Xây dựng module Sensor thu thập máy trạm từ xa quy mô lớn và tích hợp kết nối Webhook hai chiều với các hệ thống SIEM/SOAR doanh nghiệp.")

    # Save to Desktop and Hunting-Forensics
    dest_desktop = Path(r"C:\Users\Acer\Desktop\Bao_Cao_Nghien_Cuu_AI_Forensic_Va_Kien_Truc_V_autoFor.docx")
    dest_desktop_v2 = Path(r"C:\Users\Acer\Desktop\Bao_Cao_Nghien_Cuu_AI_Forensic_Va_Kien_Truc_V_autoFor_v2.docx")
    dest_project = Path(r"E:\Hunting-Forensics\Bao_Cao_Nghien_Cuu_AI_Forensic_Va_Kien_Truc_V_autoFor.docx")

    try:
        doc.save(str(dest_desktop))
        print(f"[OK] Saved Desktop: {dest_desktop} ({dest_desktop.stat().st_size} bytes)")
    except PermissionError:
        doc.save(str(dest_desktop_v2))
        print(f"[NOTE] Desktop file is currently opened in Word! Saved updated version as: {dest_desktop_v2} ({dest_desktop_v2.stat().st_size} bytes)")

    doc.save(str(dest_project))
    print(f"[OK] Saved Project: {dest_project} ({dest_project.stat().st_size} bytes)")

if __name__ == "__main__":
    build_full_docx()
