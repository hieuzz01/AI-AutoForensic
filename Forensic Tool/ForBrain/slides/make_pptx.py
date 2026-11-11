import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)
blank_layout = prs.slide_layouts[6]

# Colors matching Viettel / VTNet corporate identity
C_RED = RGBColor(192, 0, 0)
C_DARK_RED = RGBColor(160, 0, 0)
C_DARK_BLUE = RGBColor(13, 71, 161)
C_LIGHT_BLUE = RGBColor(227, 242, 253)
C_BORDER_BLUE = RGBColor(144, 202, 249)
C_TEXT_DARK = RGBColor(33, 33, 33)
C_TEXT_MUTED = RGBColor(100, 116, 139)
C_WHITE = RGBColor(255, 255, 255)
C_ORANGE_BG = RGBColor(255, 243, 224)
C_ORANGE_BORDER = RGBColor(255, 183, 77)
C_GREEN_BG = RGBColor(232, 245, 233)
C_GREEN_BORDER = RGBColor(129, 199, 132)
C_BOX_GRAY = RGBColor(248, 250, 252)
C_LINE_GRAY = RGBColor(226, 232, 240)
C_YELLOW_BG = RGBColor(254, 243, 199)
C_YELLOW_BORDER = RGBColor(245, 158, 11)

def add_header(slide, title, subtitle, brand="VTNet"):
    # Red indicator bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.35), Inches(0.12), Inches(0.65))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_RED
    bar.line.color.rgb = C_RED
    
    # Title & Subtitle box
    tb = slide.shapes.add_textbox(Inches(0.6), Inches(0.3), Inches(10.5), Inches(0.8))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Arial"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = C_TEXT_DARK
    
    p2 = tf.add_paragraph()
    p2.text = subtitle
    p2.font.name = "Arial"
    p2.font.size = Pt(11)
    p2.font.color.rgb = C_TEXT_MUTED
    
    # Brand logo text
    tb_b = slide.shapes.add_textbox(Inches(11.2), Inches(0.3), Inches(1.7), Inches(0.6))
    tf_b = tb_b.text_frame
    tf_b.margin_left = tf_b.margin_top = tf_b.margin_right = tf_b.margin_bottom = 0
    p_b = tf_b.paragraphs[0]
    p_b.text = brand
    p_b.alignment = PP_ALIGN.RIGHT
    p_b.font.name = "Arial"
    p_b.font.size = Pt(22)
    p_b.font.bold = True
    p_b.font.color.rgb = C_RED

# ==========================================
# SLIDE 1: BỐI CẢNH & GIÁ TRỊ MANG LẠI
# ==========================================
s1 = prs.slides.add_slide(blank_layout)
add_header(s1, "AI Forensics", "Sự cố do AI sinh khối lượng log khổng lồ \u2192 điều tra thủ công kéo dài \u2192 AI điều tra tự động", "viettel")

# Left Column: Xu Hướng AI 2026
trend_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), Inches(1.2), Inches(4.0), Inches(4.3))
trend_box.fill.solid()
trend_box.fill.fore_color.rgb = RGBColor(254, 242, 242)
trend_box.line.color.rgb = C_RED
trend_box.line.width = Pt(1.5)

tf_tr = trend_box.text_frame
tf_tr.word_wrap = True
tf_tr.margin_left = tf_tr.margin_right = Inches(0.2)
tf_tr.margin_top = Inches(0.2)

p = tf_tr.paragraphs[0]
p.text = "XU HƯỚNG AI 2026"
p.font.name = "Arial"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_RED

p = tf_tr.add_paragraph()
p.text = "1.100 USD"
p.font.name = "Arial"
p.font.size = Pt(36)
p.font.bold = True
p.font.color.rgb = C_RED

p = tf_tr.add_paragraph()
p.text = "chi phí mỗi giờ một vụ vi phạm chưa xử lý xong;\ntrung bình 4,99 triệu USD/vụ (+12%) \u2013 IBM 2026\n"
p.font.name = "Arial"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_TEXT_DARK

p = tf_tr.add_paragraph()
p.text = "1/4 vụ tấn công có chủ đích đã có AI tham gia (+56% so với năm trước), chi phí ~6 triệu USD/vụ. Điều tra càng chậm, chi phí phát hiện \u2013 leo thang và mất khách hàng càng lớn."
p.font.name = "Arial"
p.font.size = Pt(10.5)
p.font.color.rgb = RGBColor(71, 85, 105)

# Right 4 Boxes: HẠN CHẾ CỦA CÔNG CỤ VÀ QUY TRÌNH HIỆN HỮU
h_lim = s1.shapes.add_textbox(Inches(4.6), Inches(1.15), Inches(8.3), Inches(0.4))
p = h_lim.text_frame.paragraphs[0]
p.text = "HẠN CHẾ CỦA CÔNG CỤ VÀ QUY TRÌNH HIỆN HỮU"
p.font.name = "Arial"
p.font.size = Pt(12)
p.font.bold = True
p.font.color.rgb = C_TEXT_DARK

limit_cards = [
    ("Thu thập \u00b7 KAPE, Velociraptor", "Thu thập từng máy theo phiên, cần quyền truy cập và người thao tác; chiến dịch AI chỉ trong vài giờ đã chạm nhiều tài khoản, dịch vụ cloud.", Inches(4.6), Inches(1.55)),
    ("Phân tích \u00b7 Volatility, Autopsy", "Mạnh nhưng chỉ xử lý từng nguồn; analyst tự ghép timeline từ nhiều hệ thống, thường tốn 3\u20135 man-day cho một sự cố trung bình.", Inches(8.8), Inches(1.55)),
    ("SIEM \u00b7 Splunk, QRadar, ELK", "Log rải rác, thường chỉ lưu 90 ngày trong khi tin tặc ẩn nấp lâu hơn (BRICKSTORM ~400 ngày); tìm kiếm được nhưng không tự suy ra nguyên nhân gốc.", Inches(4.6), Inches(3.4)),
    ("Báo cáo \u00b7 Word/Excel thủ công", "Dựng attack timeline, root cause và khuyến nghị khắc phục bằng tay, dễ sai sót và chất lượng phụ thuộc người viết.", Inches(8.8), Inches(3.4))
]

for title, desc, l, t in limit_cards:
    box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, Inches(4.0), Inches(1.75))
    box.fill.solid()
    box.fill.fore_color.rgb = C_WHITE
    box.line.color.rgb = RGBColor(249, 115, 22)
    box.line.width = Pt(1.5)
    
    tf_b = box.text_frame
    tf_b.word_wrap = True
    tf_b.margin_left = tf_b.margin_right = Inches(0.2)
    tf_b.margin_top = Inches(0.15)
    
    p = tf_b.paragraphs[0]
    p.text = title
    p.font.name = "Arial"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(194, 65, 12)
    
    p2 = tf_b.add_paragraph()
    p2.text = desc
    p2.font.name = "Arial"
    p2.font.size = Pt(10)
    p2.font.color.rgb = RGBColor(71, 85, 105)

# Bottom Section: GIÁ TRỊ MANG LẠI
val_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), Inches(5.65), Inches(12.5), Inches(1.4))
val_box.fill.solid()
val_box.fill.fore_color.rgb = RGBColor(255, 247, 237)
val_box.line.color.rgb = RGBColor(254, 215, 170)
val_box.line.width = Pt(1.0)

val_bar = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(5.65), Inches(0.08), Inches(1.4))
val_bar.fill.solid()
val_bar.fill.fore_color.rgb = C_RED
val_bar.line.color.rgb = C_RED

tf_v = val_box.text_frame
tf_v.word_wrap = True
tf_v.margin_left = Inches(0.25)
tf_v.margin_top = Inches(0.1)

p = tf_v.paragraphs[0]
p.text = "GIÁ TRỊ MANG LẠI: AI tự tìm nguyên nhân gốc, ghép bằng chứng đa nguồn và lập báo cáo kèm khuyến nghị"
p.font.name = "Arial"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_TEXT_DARK

metrics = [
    ("-75% man-day", "3\u20135 \u2192 ~1 man-day để điều tra và lập báo cáo cho mỗi sự cố (*)", Inches(0.7)),
    ("Vài giờ", "từ sự cố đến attack timeline và root cause, thay cho nhiều ngày (*)", Inches(3.8)),
    ("100% dẫn chứng", "mỗi kết luận gắn với log gốc để chuyên gia kiểm tra lại (*)", Inches(6.9)),
    ("63% chi phí", "chi phí vi phạm đến từ phát hiện \u2013 leo thang và mất khách; điều tra nhanh giúp giảm (IBM 2026)", Inches(10.0))
]

for m_title, m_desc, m_left in metrics:
    m_tb = s1.shapes.add_textbox(m_left, Inches(6.05), Inches(2.9), Inches(0.9))
    tf_m = m_tb.text_frame
    tf_m.word_wrap = True
    tf_m.margin_left = tf_m.margin_top = tf_m.margin_right = tf_m.margin_bottom = 0
    p = tf_m.paragraphs[0]
    p.text = m_title
    p.font.name = "Arial"
    p.font.size = Pt(16)
    p.font.bold = True
    p.font.color.rgb = C_RED
    
    p2 = tf_m.add_paragraph()
    p2.text = m_desc
    p2.font.name = "Arial"
    p2.font.size = Pt(8.5)
    p2.font.color.rgb = RGBColor(100, 116, 139)

fn = s1.shapes.add_textbox(Inches(0.4), Inches(7.15), Inches(12.5), Inches(0.3))
p_fn = fn.text_frame.paragraphs[0]
p_fn.text = "Nguồn: IBM \u2013 Cost of a Data Breach Report 2026; Mandiant M-Trends 2026. (*) Ước tính nội bộ so với điều tra thủ công, sẽ hiệu chỉnh theo kết quả pilot V-AutoFor."
p_fn.font.name = "Arial"
p_fn.font.size = Pt(7.5)
p_fn.font.color.rgb = RGBColor(148, 163, 184)


# ==========================================
# SLIDE 2: KIẾN TRÚC HỆ THỐNG V-AUTOFOR & FORBRAIN
# ==========================================
s2 = prs.slides.add_slide(blank_layout)
add_header(s2, "AI FORENSICS - KIẾN TRÚC HỆ THỐNG", "Tự động điều tra và phân tích nguyên nhân sự cố ATTT \u2014 4 Agents + LLM Orchestrator & MCP Server Pool", "VTNet")

badges = [
    ("CLIENT & OUTPUT", Inches(1.15), Inches(0.85), RGBColor(225, 29, 72)),
    ("ORCHESTRATOR & 4 AGENTS", Inches(2.05), Inches(2.4), RGBColor(225, 29, 72)),
    ("MCP SERVER POOL", Inches(4.5), Inches(0.6), RGBColor(51, 65, 85)),
    ("HỆ THỐNG ĐIỀU TRA", Inches(5.15), Inches(0.6), RGBColor(51, 65, 85)),
    ("LUỒNG XỬ LÝ", Inches(5.8), Inches(1.3), RGBColor(225, 29, 72))
]

for b_text, b_top, b_height, b_color in badges:
    b_shape = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.3), b_top, Inches(1.4), b_height)
    b_shape.fill.solid()
    b_shape.fill.fore_color.rgb = b_color
    b_shape.line.fill.background()
    tf_b = b_shape.text_frame
    tf_b.word_wrap = True
    tf_b.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf_b.margin_left = tf_b.margin_right = Inches(0.08)
    p = tf_b.paragraphs[0]
    p.text = b_text
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Arial"
    p.font.size = Pt(9)
    p.font.bold = True
    p.font.color.rgb = C_WHITE

main_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(1.15), Inches(8.8), Inches(4.6))
main_box.fill.solid()
main_box.fill.fore_color.rgb = RGBColor(255, 255, 255)
main_box.line.color.rgb = RGBColor(244, 63, 94)
main_box.line.width = Pt(1.5)

top_tag = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.1), Inches(1.05), Inches(2.2), Inches(0.25))
top_tag.fill.solid()
top_tag.fill.fore_color.rgb = RGBColor(225, 29, 72)
top_tag.line.fill.background()
p = top_tag.text_frame.paragraphs[0]
p.text = "HỆ THỐNG AI FORENSICS"
p.alignment = PP_ALIGN.CENTER
p.font.name = "Arial"
p.font.size = Pt(8.5)
p.font.bold = True
p.font.color.rgb = C_WHITE

in_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.95), Inches(1.35), Inches(3.8), Inches(0.55))
in_box.fill.solid()
in_box.fill.fore_color.rgb = RGBColor(248, 250, 252)
in_box.line.color.rgb = RGBColor(203, 213, 225)
tf_in = in_box.text_frame
tf_in.word_wrap = True
tf_in.margin_left = Inches(0.1)
tf_in.margin_top = Inches(0.06)
p = tf_in.paragraphs[0]
p.text = "1 [INPUT] Submit Evidence / Ticket"
p.font.name = "Arial"
p.font.size = Pt(8.5)
p.font.bold = True
p.font.color.rgb = C_RED
p2 = tf_in.add_paragraph()
p2.text = "CLIENT \u2014 FTK .ad1, .raw, .pcap, .evtx / Incident request"
p2.font.name = "Arial"
p2.font.size = Pt(7.5)
p2.font.color.rgb = RGBColor(100, 116, 139)

out_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.6), Inches(1.35), Inches(3.8), Inches(0.55))
out_box.fill.solid()
out_box.fill.fore_color.rgb = RGBColor(248, 250, 252)
out_box.line.color.rgb = RGBColor(203, 213, 225)
tf_out = out_box.text_frame
tf_out.word_wrap = True
tf_out.margin_left = Inches(0.1)
tf_out.margin_top = Inches(0.06)
p = tf_out.paragraphs[0]
p.text = "6 [OUTPUT] Forensic Report & Playbook"
p.font.name = "Arial"
p.font.size = Pt(8.5)
p.font.bold = True
p.font.color.rgb = C_RED
p2 = tf_out.add_paragraph()
p2.text = "OUTPUT \u2014 SANS DOCX/PDF, STIX 2.1 IOC, Process Tree, Action Chart"
p2.font.name = "Arial"
p2.font.size = Pt(7.5)
p2.font.color.rgb = RGBColor(100, 116, 139)

orch_bar = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.8), Inches(1.95), Inches(6.8), Inches(0.22))
orch_bar.fill.solid()
orch_bar.fill.fore_color.rgb = RGBColor(225, 29, 72)
orch_bar.line.fill.background()
p = orch_bar.text_frame.paragraphs[0]
p.text = "ORCHESTRATOR \u2014 Reasonix LLM Orchestrator / Reasoning Engine (:8787)"
p.alignment = PP_ALIGN.CENTER
p.font.name = "Arial"
p.font.size = Pt(8)
p.font.bold = True
p.font.color.rgb = C_WHITE

orch_pills = [
    ("Nhận & phân loại", "Dispatch incident \u2192 Agent 01", Inches(1.95)),
    ("LLM Reasoning", "TTP Inference \u2194 Agent 01", Inches(3.6)),
    ("LLM Planning", "Acquisition strategy \u2194 Agent 02", Inches(5.25)),
    ("LLM 5-Why", "Root cause \u2194 Agent 03", Inches(6.9)),
    ("LLM Re-evaluate", "Counterfact check \u2194 Agent 04", Inches(8.55))
]

for title, sub, l in orch_pills:
    pill = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, Inches(2.22), Inches(1.55), Inches(0.65))
    pill.fill.solid()
    pill.fill.fore_color.rgb = C_WHITE
    pill.line.color.rgb = RGBColor(225, 29, 72)
    pill.line.width = Pt(1.0)
    tf = pill.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.05)
    tf.margin_top = Inches(0.05)
    p = tf.paragraphs[0]
    p.text = "[LLM] " + title
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Arial"
    p.font.size = Pt(7.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(225, 29, 72)
    p2 = tf.add_paragraph()
    p2.text = sub
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = "Arial"
    p2.font.size = Pt(6.5)
    p2.font.color.rgb = RGBColor(100, 116, 139)

agents_data = [
    ("AGENT 01 \u2014 Hypothesis", "TTP \u00b7 IOC builder\nBuild Hypothesis JSON\nRoots > Websrv > Artifacts\n\u21d2 hypothesis JSON", Inches(1.95), Inches(2.95), Inches(1.6), Inches(1.15), RGBColor(239, 246, 255), RGBColor(59, 130, 246)),
    ("AGENT 02 \u2014 Acquisition", "Chain of Custody\nad1_extract & Mount\nArtifact Lineage\n\u21d2 evidence verified", Inches(3.65), Inches(2.95), Inches(1.6), Inches(1.15), RGBColor(239, 246, 255), RGBColor(59, 130, 246)),
    ("AGENT 03 \u2014 Analysis (MCP)", "Findings Report \u00b7 ThreatAct\nIOC \u00b7 TrustScore \u00b7 5-Why\nCall MCP Server Pool\n\u21d2 findings JSON", Inches(5.35), Inches(2.95), Inches(1.6), Inches(1.15), RGBColor(239, 246, 255), RGBColor(59, 130, 246)),
    ("AGENT 04 \u2014 Reviewer", "Adversarial Review\nVETO Loop Max 3 rounds\nZero-Hallucination\n\u21d2 sign-off check", Inches(7.05), Inches(2.95), Inches(1.6), Inches(1.15), RGBColor(254, 243, 199), RGBColor(245, 158, 11)),
    ("BẮT BUỘC PHÊ DUYỆT", "\u2713 APPROVED (SIGN-OFF)\nKý duyệt báo cáo \u2192 xuất\nchính thức sang Báo cáo\nForensic Report", Inches(8.75), Inches(2.95), Inches(1.75), Inches(1.15), RGBColor(217, 119, 6), RGBColor(180, 83, 9))
]

for title, desc, l, t, w, h, bg_col, bdr_col in agents_data:
    box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    box.fill.solid()
    box.fill.fore_color.rgb = bg_col
    box.line.color.rgb = bdr_col
    box.line.width = Pt(1.2)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.06)
    tf.margin_top = Inches(0.06)
    p = tf.paragraphs[0]
    p.text = title
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Arial"
    p.font.size = Pt(7.5)
    p.font.bold = True
    p.font.color.rgb = C_WHITE if bg_col == RGBColor(217, 119, 6) else RGBColor(30, 58, 138)
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = "Arial"
    p2.font.size = Pt(6.8)
    p2.font.color.rgb = C_WHITE if bg_col == RGBColor(217, 119, 6) else RGBColor(51, 65, 85)

mcp_items = [
    ("MCP Dissect", "AD1 & Target Parser"),
    ("MCP Volatility 3", "Memory RAM Dump"),
    ("MCP TShark", "PCAP Network Decoder"),
    ("MCP Eric Zimmerman", "MFT, Registry, Prefetch"),
    ("MCP Sysinternals", "Autoruns, Sigcheck, CLI"),
    ("MCP FastMCP Bridge", "IPC JSON-RPC Telemetry")
]

for idx, (m_name, m_sub) in enumerate(mcp_items):
    m_left = Inches(1.95 + idx * 1.45)
    box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, m_left, Inches(4.2), Inches(1.38), Inches(0.48))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(241, 245, 249)
    box.line.color.rgb = RGBColor(71, 85, 105)
    box.line.width = Pt(1.0)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.04)
    p = tf.paragraphs[0]
    p.text = m_name
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Arial"
    p.font.size = Pt(7.2)
    p.font.bold = True
    p.font.color.rgb = RGBColor(15, 23, 42)
    p2 = tf.add_paragraph()
    p2.text = m_sub
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = "Arial"
    p2.font.size = Pt(6)
    p2.font.color.rgb = RGBColor(100, 116, 139)

sys_items = [
    ("FTK .ad1 Containers", "Logical Disk Images"),
    ("Raw / E01 Images", "Bit-stream Storage"),
    ("Memory RAM Dumps", "Volatile Artifacts"),
    ("PCAP Network Logs", "Traffic Decryption"),
    ("NTFS / EVTX / Registry", "Execution & Timelines"),
    ("ForBrain Telemetry (:5000)", "Real-time Observability")
]

for idx, (s_name, s_sub) in enumerate(sys_items):
    s_left = Inches(1.95 + idx * 1.45)
    box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, s_left, Inches(4.78), Inches(1.38), Inches(0.48))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(248, 250, 252)
    box.line.color.rgb = RGBColor(148, 163, 184)
    box.line.width = Pt(0.8)
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.04)
    tf.margin_top = Inches(0.04)
    p = tf.paragraphs[0]
    p.text = s_name
    p.alignment = PP_ALIGN.CENTER
    p.font.name = "Arial"
    p.font.size = Pt(7)
    p.font.bold = True
    p.font.color.rgb = RGBColor(30, 41, 59)
    p2 = tf.add_paragraph()
    p2.text = s_sub
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = "Arial"
    p2.font.size = Pt(5.8)
    p2.font.color.rgb = RGBColor(148, 163, 184)

veto_ann = s2.shapes.add_textbox(Inches(6.8), Inches(4.02), Inches(3.5), Inches(0.2))
p_v = veto_ann.text_frame.paragraphs[0]
p_v.text = "<-- VETO Loop (Max 3 rounds: Bác bỏ nếu thiếu chứng cứ thực tế) --"
p_v.font.name = "Arial"
p_v.font.size = Pt(6.8)
p_v.font.bold = True
p_v.font.color.rgb = RGBColor(217, 119, 6)

right_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.75), Inches(1.15), Inches(2.25), Inches(4.6))
right_box.fill.solid()
right_box.fill.fore_color.rgb = C_WHITE
right_box.line.color.rgb = RGBColor(59, 130, 246)
right_box.line.width = Pt(1.5)

tf_r = right_box.text_frame
tf_r.word_wrap = True
tf_r.margin_left = tf_r.margin_right = Inches(0.1)
tf_r.margin_top = Inches(0.1)

p = tf_r.paragraphs[0]
p.text = "HẠ TẦNG AI"
p.alignment = PP_ALIGN.CENTER
p.font.name = "Arial"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = RGBColor(29, 78, 216)

ai_card = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.9), Inches(1.5), Inches(1.95), Inches(1.4))
ai_card.fill.solid()
ai_card.fill.fore_color.rgb = RGBColor(239, 246, 255)
ai_card.line.color.rgb = RGBColor(147, 197, 253)
tf_ac = ai_card.text_frame
tf_ac.word_wrap = True
tf_ac.margin_left = tf_ac.margin_right = Inches(0.08)
tf_ac.margin_top = Inches(0.06)
p = tf_ac.paragraphs[0]
p.text = "LLM ORCHESTRATOR\n(V-AutoFor Studio :8787)"
p.alignment = PP_ALIGN.CENTER
p.font.name = "Arial"
p.font.size = Pt(7.8)
p.font.bold = True
p.font.color.rgb = RGBColor(30, 58, 138)
p2 = tf_ac.add_paragraph()
p2.text = "Reasoning Engine: Suy luận 2 chiều (Agent \u2194 LLM Orchestrator).\nForBrain Telemetry (:5000): Stream Live webhook."
p2.font.name = "Arial"
p2.font.size = Pt(6.8)
p2.font.color.rgb = RGBColor(71, 85, 105)

leg_h = s2.shapes.add_textbox(Inches(10.85), Inches(2.95), Inches(2.0), Inches(0.25))
p = leg_h.text_frame.paragraphs[0]
p.text = "CHÚ GIẢI"
p.font.name = "Arial"
p.font.size = Pt(9)
p.font.bold = True
p.font.color.rgb = C_TEXT_DARK

legend_items = [
    ("\u2192 Sequential flow", "Output N \u2192 Input N+1 (Tuần tự)", RGBColor(225, 29, 72)),
    ("\u2194 LLM reasoning call", "2-way Agent \u2194 LLM Engine", RGBColor(59, 130, 246)),
    ("\u2504 VETO loop", "Agent 04 \u2192 Agent 01/03 (Max 3)", RGBColor(217, 119, 6)),
    ("\u2194 MCP connection", "Agent 03 \u2194 Dissect/Volat/TShark", RGBColor(15, 23, 42)),
    ("[LLM] Agent sử dụng AI", "Qwen-2.5-Coder / DeepSeek-R1", RGBColor(225, 29, 72))
]

for idx, (l_title, l_desc, l_col) in enumerate(legend_items):
    tb_l = s2.shapes.add_textbox(Inches(10.85), Inches(3.2 + idx * 0.48), Inches(2.1), Inches(0.45))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    tf_l.margin_left = tf_l.margin_top = tf_l.margin_right = tf_l.margin_bottom = 0
    p = tf_l.paragraphs[0]
    p.text = l_title
    p.font.name = "Arial"
    p.font.size = Pt(7.2)
    p.font.bold = True
    p.font.color.rgb = l_col
    p2 = tf_l.add_paragraph()
    p2.text = l_desc
    p2.font.name = "Arial"
    p2.font.size = Pt(6.2)
    p2.font.color.rgb = RGBColor(100, 116, 139)

luong_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.8), Inches(5.85), Inches(11.2), Inches(1.2))
luong_box.fill.solid()
luong_box.fill.fore_color.rgb = RGBColor(254, 242, 242)
luong_box.line.color.rgb = RGBColor(254, 205, 211)
luong_box.line.width = Pt(1.0)

luong_bar = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.8), Inches(5.85), Inches(0.08), Inches(1.2))
luong_bar.fill.solid()
luong_bar.fill.fore_color.rgb = C_RED
luong_bar.line.color.rgb = C_RED

phases = [
    ("1 Tiếp nhận ticket", "Submit Evidence \u2192 LLM Orchestrator nhận & phân loại"),
    ("2 Sinh giả thuyết", "Agent 01 + LLM Reasoning dựng Build Hypothesis JSON"),
    ("3 Thu thập chứng cứ", "Agent 02 + LLM Planning chạy ad1_extract & đĩa logic"),
    ("4 Phân tích (MCP)", "Agent 03 + LLM 5-Why gọi FastMCP Server Pool lập Findings"),
    ("5 Duyệt đối kháng", "Agent 04 + LLM Re-evaluate kiểm tra VETO (tối đa 3 vòng)"),
    ("6 Duyệt & báo cáo", "Ký duyệt (APPROVED Sign-off) \u2192 Forensic Report & IOCs")
]

for idx, (p_num, p_desc) in enumerate(phases):
    p_left = Inches(1.95 + idx * 1.83)
    p_tb = s2.shapes.add_textbox(p_left, Inches(5.95), Inches(1.75), Inches(1.0))
    tf_p = p_tb.text_frame
    tf_p.word_wrap = True
    tf_p.margin_left = tf_p.margin_top = tf_p.margin_right = tf_p.margin_bottom = 0
    p = tf_p.paragraphs[0]
    p.text = p_num
    p.font.name = "Arial"
    p.font.size = Pt(8)
    p.font.bold = True
    p.font.color.rgb = C_RED
    p2 = tf_p.add_paragraph()
    p2.text = p_desc
    p2.font.name = "Arial"
    p2.font.size = Pt(7)
    p2.font.color.rgb = RGBColor(71, 85, 105)


# ==========================================
# SLIDE 3: VÒNG LẶP CHẠY FORENSIC & LUỒNG PROMPT -> BÁO CÁO
# ==========================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "AI FORENSICS - VÒNG LẶP THỰC THI & QUY TRÌNH TỪ PROMPT ĐẾN BÁO CÁO", "Chu trình khép kín: User Prompt \u2192 Reasonix Orchestrator \u2192 FastMCP Tools \u2192 ForBrain Telemetry \u2192 VETO Loop \u2192 Báo cáo", "VTNet")

steps_data = [
    ("BƯỚC 1: KHỞI TẠO & PROMPT", "Người dùng nhập yêu cầu điều tra tại V-AutoFor Studio (:8787) kèm đường dẫn bằng chứng (FirstHack.ad1, memory.dmp, incident.txt).", Inches(0.4), Inches(1.3), RGBColor(239, 246, 255), RGBColor(59, 130, 246)),
    ("BƯỚC 2: PHÂN RÃ GIẢ THUYẾT", "Orchestrator kích hoạt Agent 01 (Hypothesis). Đọc metadata, bóc tách định dạng, ánh xạ MITRE ATT&CK và tạo danh sách giả thuyết.", Inches(3.6), Inches(1.3), RGBColor(239, 246, 255), RGBColor(59, 130, 246)),
    ("BƯỚC 3: BÓC TÁCH CONTAINER", "Agent 02 (Acquisition) thực thi lệnh tự động ad1_extract hoặc mount đĩa logic qua Dissect, kiểm tra SHA256 Chain of Custody.", Inches(6.8), Inches(1.3), RGBColor(239, 246, 255), RGBColor(59, 130, 246)),
    ("BƯỚC 4: MCP TOOL EXECUTION", "Agent 03 (Analysis) gọi 4 FastMCP servers: Volatility (pslist, malfind), Dissect (target), TShark (dns, tls), EZTools (MFTECmd).", Inches(10.0), Inches(1.3), RGBColor(239, 246, 255), RGBColor(59, 130, 246)),
    
    ("BƯỚC 5: LIVE TELEMETRY STREAM", "Từng lệnh gọi MCP Tool và output trả về được bắn Webhook thời gian thực sang ForBrain Monitor (:5000) để chuyên viên giám sát.", Inches(0.4), Inches(4.3), RGBColor(241, 245, 249), RGBColor(71, 85, 105)),
    ("BƯỚC 6: VÒNG LẶP ĐỐI KHÁNG (VETO)", "Agent 04 (Reviewer) thẩm định kết quả. Nếu phát hiện suy diễn thiếu bằng chứng nhị phân -> Kích hoạt VETO Loop (tối đa 3 vòng) điều tra lại.", Inches(3.6), Inches(4.3), RGBColor(254, 243, 199), RGBColor(245, 158, 11)),
    ("BƯỚC 7: KÝ DUYỆT (SIGN-OFF)", "Khi mọi giả thuyết đã có dẫn chứng nhị phân 100% khớp, Agent 04 ký APPROVED Sign-off và chuyển dữ liệu sang bộ sinh báo cáo.", Inches(6.8), Inches(4.3), RGBColor(236, 253, 245), RGBColor(16, 185, 129)),
    ("BƯỚC 8: BÁO CÁO TOÀN DIỆN", "Hệ thống tự động xuất Báo cáo Giám định (DOCX/PDF chuẩn SANS), Master Timeline CSV, Cây tiến trình Process Tree và Tập hợp IOC STIX 2.1.", Inches(10.0), Inches(4.3), RGBColor(254, 242, 242), RGBColor(225, 29, 72))
]

for title, desc, l, t, bg_col, bdr_col in steps_data:
    box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, Inches(2.9), Inches(2.6))
    box.fill.solid()
    box.fill.fore_color.rgb = bg_col
    box.line.color.rgb = bdr_col
    box.line.width = Pt(1.5)
    
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.15)
    
    p = tf.paragraphs[0]
    p.text = title
    p.font.name = "Arial"
    p.font.size = Pt(10)
    p.font.bold = True
    p.font.color.rgb = C_DARK_RED if bg_col == RGBColor(254, 242, 242) else (RGBColor(180, 83, 9) if bg_col == RGBColor(254, 243, 199) else (RGBColor(6, 95, 70) if bg_col == RGBColor(236, 253, 245) else RGBColor(30, 58, 138)))
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.font.name = "Arial"
    p2.font.size = Pt(9.2)
    p2.font.color.rgb = RGBColor(51, 65, 85)

# Save presentations
out_project = r"E:\Hunting-Forensics\Slide_Kien_Truc_AI_Forensic_V_AutoFor.pptx"
prs.save(out_project)
print(f"[OK] Saved Project Slide: {out_project}")

out_desktop = r"C:\Users\Acer\Desktop\Slide_Kien_Truc_AI_Forensic_V_AutoFor.pptx"
try:
    prs.save(out_desktop)
    print(f"[OK] Saved Desktop Slide: {out_desktop}")
except Exception as e:
    out_desktop_v2 = r"C:\Users\Acer\Desktop\Slide_Kien_Truc_AI_Forensic_V_AutoFor_v2.pptx"
    prs.save(out_desktop_v2)
    print(f"[NOTE] Saved as v2 on Desktop: {out_desktop_v2}")
