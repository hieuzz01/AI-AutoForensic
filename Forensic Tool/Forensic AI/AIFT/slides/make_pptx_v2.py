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

# Brand Colors (Viettel / VTNet Corporate Identity)
C_RED = RGBColor(192, 0, 0)          # Viettel Main Red #C00000
C_DARK_RED = RGBColor(153, 27, 27)    # Deep Red
C_LIGHT_RED = RGBColor(254, 242, 242) # Light Pink/Red Background
C_BORDER_RED = RGBColor(244, 63, 94)  # Border Red / Rose
C_TEXT_DARK = RGBColor(30, 41, 59)    # Slate 800
C_TEXT_MUTED = RGBColor(100, 116, 139)# Slate 500
C_WHITE = RGBColor(255, 255, 255)
C_BLUE_BG = RGBColor(239, 246, 255)   # Blue 50
C_BLUE_BORDER = RGBColor(59, 130, 246)# Blue 500
C_DARK_BLUE = RGBColor(30, 58, 138)   # Blue 900
C_YELLOW_BG = RGBColor(254, 243, 199) # Amber 50
C_YELLOW_BORDER = RGBColor(245, 158, 11) # Amber 500
C_GREEN_BG = RGBColor(236, 253, 245)  # Emerald 50
C_GREEN_BORDER = RGBColor(16, 185, 129)# Emerald 500
C_GRAY_BG = RGBColor(248, 250, 252)   # Slate 50
C_GRAY_BORDER = RGBColor(203, 213, 225) # Slate 300
C_DARK_SLATE = RGBColor(15, 23, 42)

def add_header(slide, title, subtitle, brand="VTNet"):
    # Red vertical indicator bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(0.35), Inches(0.12), Inches(0.65))
    bar.fill.solid()
    bar.fill.fore_color.rgb = C_RED
    bar.line.fill.background()
    
    # Title & Subtitle box
    tb = slide.shapes.add_textbox(Inches(0.62), Inches(0.3), Inches(10.5), Inches(0.8))
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
    
    # Brand logo text top-right
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


# ==============================================================================
# SLIDE 1: BỐI CẢNH & GIÁ TRỊ MANG LẠI (GIỮ NGUYÊN FORM ẢNH 2 USER GỬI)
# ==============================================================================
s1 = prs.slides.add_slide(blank_layout)
add_header(s1, "AI Forensics", "Sự cố do AI sinh khối lượng log khổng lồ \u2192 điều tra thủ công kéo dài \u2192 AI điều tra tự động", "viettel")

# Left Column: Xu Hướng AI 2026 Box
trend_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), Inches(1.2), Inches(4.0), Inches(4.3))
trend_box.fill.solid()
trend_box.fill.fore_color.rgb = C_LIGHT_RED
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

# Right: HẠN CHẾ CỦA CÔNG CỤ VÀ QUY TRÌNH HIỆN HỮU (4 Hộp)
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
val_bar.line.fill.background()

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


# ==============================================================================
# SLIDE 2: KIẾN TRÚC HỆ THỐNG (GIỮ NGUYÊN FORM ẢNH 1 USER GỬI)
# ==============================================================================
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
in_box.fill.fore_color.rgb = C_GRAY_BG
in_box.line.color.rgb = C_GRAY_BORDER
tf_in = in_box.text_frame
tf_in.word_wrap = True
tf_in.margin_left = Inches(0.1)
tf_in.margin_top = Inches(0.06)
p = tf_in.paragraphs[0]
p.text = "1 [INPUT] Submit XLSC Ticket"
p.font.name = "Arial"
p.font.size = Pt(8.5)
p.font.bold = True
p.font.color.rgb = C_RED
p2 = tf_in.add_paragraph()
p2.text = "CLIENT \u2014 SIBI Ticket XLSC \u00b7 Anomaly alert / Incident request"
p2.font.name = "Arial"
p2.font.size = Pt(7.5)
p2.font.color.rgb = RGBColor(100, 116, 139)

out_box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(6.6), Inches(1.35), Inches(3.8), Inches(0.55))
out_box.fill.solid()
out_box.fill.fore_color.rgb = C_GRAY_BG
out_box.line.color.rgb = C_GRAY_BORDER
tf_out = out_box.text_frame
tf_out.word_wrap = True
tf_out.margin_left = Inches(0.1)
tf_out.margin_top = Inches(0.06)
p = tf_out.paragraphs[0]
p.text = "6 [OUTPUT] Forensic Report"
p.font.name = "Arial"
p.font.size = Pt(8.5)
p.font.bold = True
p.font.color.rgb = C_RED
p2 = tf_out.add_paragraph()
p2.text = "OUTPUT \u2014 CEO & SOAR \u00b7 Executive Action Chart \u00b7 SOAR playbook"
p2.font.name = "Arial"
p2.font.size = Pt(7.5)
p2.font.color.rgb = RGBColor(100, 116, 139)

orch_bar = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(2.8), Inches(1.95), Inches(6.8), Inches(0.22))
orch_bar.fill.solid()
orch_bar.fill.fore_color.rgb = RGBColor(225, 29, 72)
orch_bar.line.fill.background()
p = orch_bar.text_frame.paragraphs[0]
p.text = "ORCHESTRATOR \u2014 LLM Orchestrator / Reasoning Engine"
p.alignment = PP_ALIGN.CENTER
p.font.name = "Arial"
p.font.size = Pt(8)
p.font.bold = True
p.font.color.rgb = C_WHITE

orch_pills = [
    ("Nhận & phân loại", "Dispatch incident \u2192 Agent 01", Inches(1.95)),
    ("LLM Reasoning", "TTP Inference \u2194 Agent 01", Inches(3.6)),
    ("LLM Planning", "Acquisition strategy \u2194 Agent 02", Inches(5.25)),
    ("LLM 5-Why", "Reasoning \u2194 Agent 03", Inches(6.9)),
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
    ("AGENT 01 \u2014 Hypothesis", "TTP \u00b7 IOC builder\nBuild Hypothesis JSON\nRoots > Websrv > Artifacts\n\u21d2 hypothesis JSON", Inches(1.95), Inches(2.95), Inches(1.6), Inches(1.15), C_BLUE_BG, C_BLUE_BORDER),
    ("AGENT 02 \u2014 Acquisition", "Chain of Custody\nRemote Forensic Acquisition\nArtifact Lineage\n\u21d2 evidence", Inches(3.65), Inches(2.95), Inches(1.6), Inches(1.15), C_BLUE_BG, C_BLUE_BORDER),
    ("AGENT 03 \u2014 Analysis (MCP)", "Findings Report \u00b7 ThreatAct\nIOC \u00b7 TrustScore \u00b7 5-Why\nCall MCP Server Pool\n\u21d2 findings", Inches(5.35), Inches(2.95), Inches(1.6), Inches(1.15), C_BLUE_BG, C_BLUE_BORDER),
    ("AGENT 04 \u2014 Adversarial", "Adversarial Review \u00b7 VETO\nMax 3 rounds \u00b7 50-life loop\nZero-Hallucination\n\u21d2 sign-off", Inches(7.05), Inches(2.95), Inches(1.6), Inches(1.15), C_YELLOW_BG, C_YELLOW_BORDER),
    ("BẮT BUỘC PHÊ DUYỆT", "\u2713 APPROVED (SIGN-OFF)\nKý duyệt báo cáo \u2192 xuất\nsign-off sang Forensic\nReport", Inches(8.75), Inches(2.95), Inches(1.75), Inches(1.15), RGBColor(217, 119, 6), RGBColor(180, 83, 9))
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
    p.font.color.rgb = C_WHITE if bg_col == RGBColor(217, 119, 6) else C_DARK_BLUE
    
    p2 = tf.add_paragraph()
    p2.text = desc
    p2.alignment = PP_ALIGN.CENTER
    p2.font.name = "Arial"
    p2.font.size = Pt(6.8)
    p2.font.color.rgb = C_WHITE if bg_col == RGBColor(217, 119, 6) else RGBColor(51, 65, 85)

mcp_items = [
    ("MCP SIEM", "Log Correlation"),
    ("MCP EDR", "Endpoint Detection"),
    ("MCP Endpoint Server", "Live Triage / Remote"),
    ("MCP Eric Zimmerman", "MFT, Registry, Prefetch"),
    ("MCP CLI Forensic", "Dissect & TShark"),
    ("MCP Velociraptor", "Fleet Artifact Hunter")
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
    ("SIEM", "Splunk, QRadar, ELK"),
    ("EDR", "CrowdStrike, Defender"),
    ("Endpoint Server", "Linux / Windows Srv"),
    ("Roots / Websrv / Artifacts", "Webshell, Auth Log"),
    ("SOAR", "Playbook Auto Response"),
    ("V-AutoFor Brain", "Live Telemetry Feed")
]

for idx, (s_name, s_sub) in enumerate(sys_items):
    s_left = Inches(1.95 + idx * 1.45)
    box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, s_left, Inches(4.78), Inches(1.38), Inches(0.48))
    box.fill.solid()
    box.fill.fore_color.rgb = C_GRAY_BG
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
p_v.text = "<-- VETO loop (max 3 rounds) --"
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
ai_card.fill.fore_color.rgb = C_BLUE_BG
ai_card.line.color.rgb = RGBColor(147, 197, 253)
tf_ac = ai_card.text_frame
tf_ac.word_wrap = True
tf_ac.margin_left = tf_ac.margin_right = Inches(0.08)
tf_ac.margin_top = Inches(0.06)
p = tf_ac.paragraphs[0]
p.text = "LLM ORCHESTRATOR\n(NETMIND LLM GATEWAY)"
p.alignment = PP_ALIGN.CENTER
p.font.name = "Arial"
p.font.size = Pt(7.8)
p.font.bold = True
p.font.color.rgb = C_DARK_BLUE
p2 = tf_ac.add_paragraph()
p2.text = "Reasoning Engine \u2013 Suy luận LLM 2 chiều (Agent \u2194 LLM Orchestrator)"
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
    ("\u2194 MCP connection", "Agent 03 \u2194 Eric Zimmerman / CLI", RGBColor(15, 23, 42)),
    ("[LLM] Agent sử dụng AI", "NetMind / Local LLM Engine", RGBColor(225, 29, 72))
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
luong_box.fill.fore_color.rgb = C_LIGHT_RED
luong_box.line.color.rgb = RGBColor(254, 205, 211)
luong_box.line.width = Pt(1.0)

luong_bar = s2.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(1.8), Inches(5.85), Inches(0.08), Inches(1.2))
luong_bar.fill.solid()
luong_bar.fill.fore_color.rgb = C_RED
luong_bar.line.fill.background()

phases = [
    ("1 Tiếp nhận ticket", "Submit XLSC Ticket \u2192 LLM Orchestrator nhận & phân loại"),
    ("2 Sinh giả thuyết", "Agent 01 + LLM Reasoning dựng Build Hypothesis JSON"),
    ("3 Thu thập chứng cứ", "Agent 02 + LLM Planning thực hiện Remote Forensic Acquisition"),
    ("4 Phân tích (MCP)", "Agent 03 + LLM 5-Why truy vấn MCP Server Pool lập Findings"),
    ("5 Duyệt đối kháng", "Agent 04 + LLM Re-evaluate kiểm tra VETO (tối đa 3 vòng)"),
    ("6 Duyệt & báo cáo", "Ký duyệt (APPROVED Sign-off) \u2192 Forensic Report & SOAR")
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


# ==============================================================================
# SLIDE 3: DIAGRAM LUỒNG WORKFLOW HOẠT ĐỘNG (CHUẨN FORM VTNET)
# ==============================================================================
s3 = prs.slides.add_slide(blank_layout)
add_header(s3, "AI FORENSICS - DIAGRAM LUỒNG WORKFLOW HOẠT ĐỘNG", "Quy trình điều tra 5 giai đoạn khép kín theo chuẩn SANS FOR508 & Cơ chế kiểm tra đối kháng VETO", "VTNet")

workflow_phases = [
    ("PHASE 1: TIẾP NHẬN & TRIAGE", 
     "• Tiếp nhận Ticket sự cố / Bằng chứng (.ad1, .raw, .dmp, .pcap)\n• Thẩm định tính toàn vẹn Chain of Custody: Băm MD5, SHA-1, SHA-256 (ISO 27037)\n• Triage sơ bộ: Phân loại OS, kiến trúc & bề mặt tấn công", 
     Inches(0.4), C_BLUE_BG, C_BLUE_BORDER),
    
    ("PHASE 2: LẬP GIẢ THUYẾT (TTP)", 
     "• Agent 01 phân rã IOC và mô tả sự cố ban đầu\n• Ánh xạ chiến thuật MITRE ATT&CK (Initial Access, Execution, Persistence, C2)\n• Sinh cây giả thuyết Hypothesis JSON định hướng trích xuất chứng cứ", 
     Inches(2.9), C_BLUE_BG, C_BLUE_BORDER),
     
    ("PHASE 3: BÓC TÁCH CONTAINER", 
     "• Agent 02 chạy ad1_extract hoặc Dissect giải mã ảnh đĩa logic FTK Imager\n• Bóc tách cấu trúc nhị phân: $MFT, Amcache.hve, Prefetch, Registry, Event Logs\n• Phân tách artifact bộ nhớ RAM và luồng gói tin PCAP", 
     Inches(5.4), C_BLUE_BG, C_BLUE_BORDER),
     
    ("PHASE 4: PHÂN TÍCH CHUYÊN SÂU", 
     "• Agent 03 gọi 4 FastMCP Servers song song:\n  - Volatility 3: Rà quét tiến trình RAM, malfind\n  - Eric Zimmerman: MFTECmd timestomping\n  - TShark: Lọc DNS Tunneling, TLS SNI\n• Bắn Live Telemetry Webhook về ForBrain (:5000)", 
     Inches(7.9), C_BLUE_BG, C_BLUE_BORDER),
     
    ("PHASE 5: VETO & SIGN-OFF", 
     "• Agent 04 đối soát chéo từng kết luận với bằng chứng số nhị phân gốc\n• VETO Loop (Tối đa 3 vòng): Bác bỏ suy diễn ảo giác, yêu cầu đào sâu lại\n• APPROVED Sign-off: Xuất SANS DOCX/PDF, Master Timeline và STIX 2.1 IOCs", 
     Inches(10.4), C_YELLOW_BG, C_YELLOW_BORDER)
]

for title, desc, l, bg_col, bdr_col in workflow_phases:
    box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, Inches(1.3), Inches(2.4), Inches(4.3))
    box.fill.solid()
    box.fill.fore_color.rgb = bg_col
    box.line.color.rgb = bdr_col
    box.line.width = Pt(1.5)
    
    # Top card tag
    tag = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, Inches(1.3), Inches(2.4), Inches(0.45))
    tag.fill.solid()
    tag.fill.fore_color.rgb = RGBColor(225, 29, 72) if bg_col == C_YELLOW_BG else RGBColor(30, 58, 138)
    tag.line.fill.background()
    p_t = tag.text_frame.paragraphs[0]
    p_t.text = title
    p_t.alignment = PP_ALIGN.CENTER
    p_t.font.name = "Arial"
    p_t.font.size = Pt(8.5)
    p_t.font.bold = True
    p_t.font.color.rgb = C_WHITE
    
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.12)
    tf.margin_top = Inches(0.55)
    
    p = tf.paragraphs[0]
    p.text = desc
    p.font.name = "Arial"
    p.font.size = Pt(8.5)
    p.font.color.rgb = RGBColor(30, 41, 59)

# Arrow indicators between phases
for idx in range(4):
    arrow_left = Inches(2.82 + idx * 2.5)
    tb_a = s3.shapes.add_textbox(arrow_left, Inches(3.2), Inches(0.3), Inches(0.3))
    p_a = tb_a.text_frame.paragraphs[0]
    p_a.text = "\u25b6"
    p_a.font.name = "Arial"
    p_a.font.size = Pt(14)
    p_a.font.bold = True
    p_a.font.color.rgb = C_RED

# VETO Loop bottom return banner
veto_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), Inches(5.75), Inches(12.4), Inches(1.3))
veto_box.fill.solid()
veto_box.fill.fore_color.rgb = C_LIGHT_RED
veto_box.line.color.rgb = C_BORDER_RED
veto_box.line.width = Pt(1.2)

veto_bar = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), Inches(5.75), Inches(0.08), Inches(1.3))
veto_bar.fill.solid()
veto_bar.fill.fore_color.rgb = C_RED
veto_bar.line.fill.background()

tf_vb = veto_box.text_frame
tf_vb.word_wrap = True
tf_vb.margin_left = Inches(0.25)
tf_vb.margin_top = Inches(0.1)

p = tf_vb.paragraphs[0]
p.text = "CƠ CHẾ VÒNG LẶP ĐỐI KHÁNG VETO (ZERO-HALLUCINATION GUARDRAILS) & HIỆU QUẢ THỰC THI"
p.font.name = "Arial"
p.font.size = Pt(11)
p.font.bold = True
p.font.color.rgb = C_DARK_RED

p2 = tf_vb.add_paragraph()
p2.text = "\u25c0 VETO Feedback Loop: Nếu Agent 04 phát hiện bất kỳ kết luận nào không có dẫn chứng nhị phân thô do Tools trả về \u2192 Kích hoạt quyền VETO bác bỏ, gửi trả giả thuyết về Phase 2 & 4 để thực thi đào sâu lại (tối đa 3 vòng lặp) trước khi cho phép ký duyệt."
p2.font.name = "Arial"
p2.font.size = Pt(8.8)
p2.font.color.rgb = RGBColor(71, 85, 105)

p3 = tf_vb.add_paragraph()
p3.text = "\u2714 Hiệu năng đo đạc thực tế: Giảm thời gian điều tra trung bình từ 3\u20135 ngày-công xuống còn 45\u201390 phút; bảo đảm 100% chứng cứ có giá trị pháp lý theo chuẩn ISO/IEC 27037."
p3.font.name = "Arial"
p3.font.size = Pt(8.8)
p3.font.bold = True
p3.font.color.rgb = RGBColor(5, 150, 105)


# ==============================================================================
# SLIDE 4: SƠ ĐỒ MÔ HÌNH HỆ THỐNG (SYSTEM MODEL & COMPONENT TOPOLOGY)
# ==============================================================================
s4 = prs.slides.add_slide(blank_layout)
add_header(s4, "AI FORENSICS - SƠ ĐỒ MÔ HÌNH HỆ THỐNG", "Kiến trúc phân tầng 4 lớp độc lập: Giao diện, Điều phối AI, Cầu nối FastMCP & Engine thực thi", "VTNet")

layers_data = [
    ("LỚP 1: GIAO DIỆN & GIÁM SÁT (UI & OBSERVABILITY)",
     "• V-AutoFor AI Studio (Port 8787): Giao diện trò chuyện, giao nhiệm vụ điều tra, hiển thị kết quả phân tích và báo cáo hoàn chỉnh.\n• ForBrain Observability Monitor (Port 5000): Giám sát trạng thái 8 cụm tool forensic, Live Telemetry Webhook Feed, Inspect Raw Output.\n• 9Router Gateway Dashboard (Port 20128): Quản lý tập trung API Key, theo dõi lưu lượng token, cân bằng tải và failover.",
     Inches(1.2), Inches(1.15), C_BLUE_BG, C_BLUE_BORDER),
     
    ("LỚP 2: ĐIỀU PHỐI & SUY LUẬN AI (REASONING & MULTI-AGENT ENGINE)",
     "• Reasonix Orchestrator Core: Quản lý session, state machine, phân rã mục tiêu điều tra thành các micro-tasks độc lập.\n• Bộ 4 Chuyên gia số (4 Agents): Agent 01 (Hypothesis TTP), Agent 02 (Acquisition AD1), Agent 03 (Deep Analysis), Agent 04 (Reviewer).\n• Kho Tri thức Chiến thuật (SKILL.md): Định hướng phương pháp luận SANS FOR508, ISO/IEC 27037 và quy tắc cấm dùng PowerShell.",
     Inches(2.55), Inches(1.15), C_BLUE_BG, C_BLUE_BORDER),
     
    ("LỚP 3: CẦU NỐI CHUẨN HÓA FASTMCP (FASTMCP PROTOCOL BRIDGE)",
     "• aift_mcp.py: Dissect Core Engine, bóc tách cấu trúc đĩa logic và ảnh vật lý (E01, RAW, VMDK).\n• eztools_mcp.py: Eric Zimmerman Tools (.NET 9), PE Malware Analyzer (pefile), Linux Log Engine (auth.log, bash_history).\n• sysinternals_mcp.py: Microsoft Sysinternals Suite (Autoruns64, Sigcheck64, Strings64, Handles64, Tcpvcon64).\n• network_memory_mcp.py: Volatility 3 RAM analysis, Wireshark TShark PCAP decoder, AD1 Container Auto-Unpacker.",
     Inches(3.9), Inches(1.3), C_LIGHT_RED, C_BORDER_RED),
     
    ("LỚP 4: BỘ NHỊ PHÂN THỰC THI & KHO BẰNG CHỨNG (ENGINES & EVIDENCE)",
     "• Động cơ thực thi nhị phân: Volatility 3 (2.28.2), Wireshark TShark (4.0.6), Dissect (2024.8), Zimmerman Suite, Sysinternals Suite.\n• Kho bằng chứng số tập trung (E:\\Hunting-Forensics\\Evidence): Chứa ảnh đĩa AD1, E01, RAM Dumps, PCAP, thư mục bóc tách extracted/.",
     Inches(5.4), Inches(1.15), C_GRAY_BG, C_GRAY_BORDER)
]

for title, desc, top, height, bg_col, bdr_col in layers_data:
    box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), top, Inches(12.5), height)
    box.fill.solid()
    box.fill.fore_color.rgb = bg_col
    box.line.color.rgb = bdr_col
    box.line.width = Pt(1.5)
    
    # Left tag on each layer
    tag = s4.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.4), top, Inches(3.6), Inches(0.35))
    tag.fill.solid()
    tag.fill.fore_color.rgb = RGBColor(225, 29, 72) if bg_col == C_LIGHT_RED else (RGBColor(30, 58, 138) if bg_col == C_BLUE_BG else RGBColor(51, 65, 85))
    tag.line.fill.background()
    p_t = tag.text_frame.paragraphs[0]
    p_t.text = title.split(":")[0] + ":" + title.split(":")[1][:22]
    p_t.alignment = PP_ALIGN.CENTER
    p_t.font.name = "Arial"
    p_t.font.size = Pt(8.5)
    p_t.font.bold = True
    p_t.font.color.rgb = C_WHITE
    
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(3.8)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.12)
    
    p = tf.paragraphs[0]
    p.text = desc
    p.font.name = "Arial"
    p.font.size = Pt(8.8)
    p.font.color.rgb = RGBColor(30, 41, 59)

# Footnote
fn4 = s4.shapes.add_textbox(Inches(0.4), Inches(6.9), Inches(12.5), Inches(0.3))
p_fn4 = fn4.text_frame.paragraphs[0]
p_fn4.text = "Ghi chú: Mô hình bảo đảm tính độc lập module (Decoupled Architecture) \u2013 Cho phép nâng cấp mô hình AI hoặc thay thế công cụ phân tích mà không ảnh hưởng tới toàn bộ hệ thống."
p_fn4.font.name = "Arial"
p_fn4.font.size = Pt(7.8)
p_fn4.font.color.rgb = RGBColor(100, 116, 139)


# ==============================================================================
# SLIDE 5: TECHSTACK CỦA SẢN PHẨM AI FORENSIC CỦA VTNET (CHUẨN FORM VTNET)
# ==============================================================================
s5 = prs.slides.add_slide(blank_layout)
add_header(s5, "AI FORENSICS - TECHSTACK SẢN PHẨM VTNET", "Ngăn xếp công nghệ toàn diện: AI Core, Giao thức MCP, Forensic Engines, Frontend & Hạ tầng", "VTNet")

tech_columns = [
    ("AI CORE & MULTI-AGENT",
     "• Multi-Agent Engine: Reasonix Framework (Python/Node CLI bridge)\n• Local / Private LLM: Qwen-2.5-Coder-32B, DeepSeek-R1, NetMind Gateway\n• Cloud Gateway: Gemini 3.8 Flash, GPT-4o qua 9Router Hub (:20128)\n• Structured Inference: JSON-RPC schema binding, 128K\u20131M token context\n• Guardrails: VETO Loop verification, Zero-Hallucination policy",
     Inches(0.4), C_BLUE_BG, C_BLUE_BORDER),
     
    ("FORENSIC ENGINES",
     "• Container & Disk: Dissect Engine (2024.8), ad1_extract, libvshadow\n• Memory Forensics: Volatility 3 (2.28.2), MemProcFS (5.19)\n• Windows Artifacts: Eric Zimmerman Tools (.NET 9 - PECmd, MFTECmd, EvtxECmd)\n• Malware Analysis: pefile (Entropy, Imphash), Microsoft Sigcheck64, Autoruns64\n• Network Decoders: Wireshark TShark (4.0.6), libpcap",
     Inches(2.9), C_BLUE_BG, C_BLUE_BORDER),
     
    ("PROTOCOLS & APIS",
     "• Tool Communication: FastMCP Protocol (Python SDK, stdio JSON-RPC)\n• Live Telemetry Stream: Asynchronous HTTP Webhook POST (/api/telemetry)\n• AI Endpoint Standard: OpenAI-compatible RESTful API (v1 routes)\n• Real-time Streaming: Server-Sent Events (SSE), WebSockets Duplex\n• Data Interchange: STIX 2.1 JSON, Yara Rules, Parquet / SQLite",
     Inches(5.4), C_LIGHT_RED, C_BORDER_RED),
     
    ("FRONTEND & OBSERVABILITY",
     "• Web Core: Flask 3.0 / Starlette Async ASGI\n• Design System: Modern Dark Neumorphism, Tailwind CSS, Heroicons\n• Visualization: D3.js Process Tree, Mermaid.js attack flow, SVG renderer\n• Live Dashboards: Tool Registry Grid, Live AI Call Telemetry, Inspect Output Modal\n• Reporting Engine: python-docx, WeasyPrint PDF, Chart.js",
     Inches(7.9), C_BLUE_BG, C_BLUE_BORDER),
     
    ("HẠ TẦNG & BẢO MẬT",
     "• Deployment Model: 100% On-Premise / Air-Gapped cô lập mạng\n• Chain of Custody: Băm MD5, SHA-1, SHA-256 (ISO/IEC 27037)\n• Evidence Ingestion: FTK AD1, E01, RAW/DD, VMDK, DMP, PCAP, EVTX\n• Runtime: Python 3.10+, Node.js LTS, .NET 8/9 Runtime, Windows Srv\n• Security: Zero cloud dependencies, dữ liệu không rời khỏi hạ tầng VTNet",
     Inches(10.4), C_GREEN_BG, C_GREEN_BORDER)
]

for title, desc, l, bg_col, bdr_col in tech_columns:
    box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, Inches(1.3), Inches(2.4), Inches(4.7))
    box.fill.solid()
    box.fill.fore_color.rgb = bg_col
    box.line.color.rgb = bdr_col
    box.line.width = Pt(1.5)
    
    tag = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, Inches(1.3), Inches(2.4), Inches(0.48))
    tag.fill.solid()
    tag.fill.fore_color.rgb = RGBColor(225, 29, 72) if bg_col == C_LIGHT_RED else (RGBColor(16, 185, 129) if bg_col == C_GREEN_BG else RGBColor(30, 58, 138))
    tag.line.fill.background()
    p_t = tag.text_frame.paragraphs[0]
    p_t.text = title
    p_t.alignment = PP_ALIGN.CENTER
    p_t.font.name = "Arial"
    p_t.font.size = Pt(8.2)
    p_t.font.bold = True
    p_t.font.color.rgb = C_WHITE
    
    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = tf.margin_right = Inches(0.12)
    tf.margin_top = Inches(0.58)
    
    p = tf.paragraphs[0]
    p.text = desc
    p.font.name = "Arial"
    p.font.size = Pt(8.2)
    p.font.color.rgb = RGBColor(30, 41, 59)

# Summary bottom banner
sum_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.4), Inches(6.15), Inches(12.4), Inches(0.95))
sum_box.fill.solid()
sum_box.fill.fore_color.rgb = C_GRAY_BG
sum_box.line.color.rgb = C_GRAY_BORDER
sum_box.line.width = Pt(1.0)

tf_s = sum_box.text_frame
tf_s.word_wrap = True
tf_s.margin_left = Inches(0.2)
tf_s.margin_top = Inches(0.1)

p = tf_s.paragraphs[0]
p.text = "TỔNG KẾT NĂNG LỰC CÔNG NGHỆ SẢN PHẨM VTNET AI FORENSICS"
p.font.name = "Arial"
p.font.size = Pt(10)
p.font.bold = True
p.font.color.rgb = C_DARK_RED

p2 = tf_s.add_paragraph()
p2.text = "Sự kết hợp hoàn hảo giữa Mô hình Ngôn ngữ Lớn chuyên sâu (Reasoning LLM), Giao thức kết nối công cụ chuẩn hóa (FastMCP Protocol), Bộ công cụ Forensic thực chiến hàng đầu thế giới (Dissect, Volatility, Eric Zimmerman, Sysinternals) và Nền tảng Giám sát minh bạch thời gian thực (ForBrain Telemetry)."
p2.font.name = "Arial"
p2.font.size = Pt(8.2)
p2.font.color.rgb = RGBColor(71, 85, 105)

# Save presentation to both locations
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

