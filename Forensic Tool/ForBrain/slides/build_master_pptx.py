import os, sys, copy
from pptx import Presentation
from pptx.enum.shapes import MSO_SHAPE_TYPE

src_file = r'C:\Users\Acer\Downloads\3-AI_One_day.pptx'
dst_file = r'C:\Users\Acer\Desktop\Slide_AI_Forensic_VTNet_Master.pptx'

prs = Presentation(src_file)

# Text replacement helper
def replace_in_paragraphs(paragraphs, repl_dict):
    for p in paragraphs:
        for old_txt, new_txt in repl_dict.items():
            if old_txt in p.text:
                full = p.text.replace(old_txt, new_txt)
                if p.runs:
                    p.runs[0].text = full
                    for r in p.runs[1:]:
                        r.text = ''
                else:
                    p.text = full

def process_shapes(shapes, repl_dict):
    for s in shapes:
        if s.has_text_frame:
            replace_in_paragraphs(s.text_frame.paragraphs, repl_dict)
        if s.has_table:
            for row in s.table.rows:
                for cell in row.cells:
                    replace_in_paragraphs(cell.text_frame.paragraphs, repl_dict)
        if s.shape_type == MSO_SHAPE_TYPE.GROUP:
            process_shapes(s.shapes, repl_dict)

# ==============================================================================
# SLIDE 1: COVER
# ==============================================================================
s1_repl = {
    "AI FOR SECURITY · AI RED": "AI FOR SECURITY · AI FORENSIC",
    "AI One day": "V-AutoFor & ForBrain",
    "Tự động sinh và quản lý mã khai thác lỗ hổng bằng AI": "Tự động hóa Điều tra số & Phân tích Nguyên nhân sự cố ATTT bằng Multi-Agent AI",
    "Tự động sinh mã khai thác từ mã nguồn, bộ cài hoặc công bố lỗ hổng,": "Tự động bóc tách container FTK AD1, RAM, Network PCAP và Windows Artifacts,",
    "lưu trữ tập trung và truy tìm nguy cơ Zero-day.": "kết nối 4 FastMCP Tools, giám sát minh bạch thời gian thực và xuất báo cáo SANS FOR508.",
    "Exploit Gen": "4 FastMCP Tools",
    "Kho mã khai thác": "ForBrain Monitor",
    "1-Day → 0-Day": "VETO Guardrail",
    "Từ công bố lỗ hổng đến mã khai thác tự động": "Từ tiếp nhận chứng cứ đến báo cáo giám định tự động"
}
process_shapes(prs.slides[0].shapes, s1_repl)

# ==============================================================================
# SLIDE 2: NGHIỆP VỤ ĐIỀU TRA & ĐIỂM NGHẼN
# ==============================================================================
s2_repl = {
    "Nghiệp vụ Reproduce CVE — tái hiện lỗ hổng 1-day / n-day": "Nghiệp vụ Điều tra số (DFIR) — từ bằng chứng thô đến kết luận nguyên nhân gốc",
    "Quy trình thủ công của chuyên gia từ thu thập CVE đến PoC & lưu kho — nơi tập trung công sức và điểm nghẽn": "Quy trình thủ công của chuyên gia từ thu thập chứng cứ đến timeline & báo cáo — nơi tập trung công sức và điểm nghẽn",
    "1. Thu thập thông tin CVE": "1. Thẩm định tính toàn vẹn",
    "2. Dựng môi trường bản lỗi": "2. Bóc tách container & đĩa",
    "3. Patch diff & root cause": "3. Mổ xẻ RAM & tiến trình",
    "4. Lần đường tới điểm lỗi": "4. Khôi phục Timeline & $MFT",
    "5. Dựng & thực thi PoC": "5. Lần dấu C2 & leo quyền",
    "6. Kiểm chứng & verify": "6. Thẩm định chéo & đối kháng",
    "7. Báo cáo & lưu kho": "7. Báo cáo & lưu kho IOC",
    
    # Col 1
    "Đọc NVD, vendor advisory, bản tin, changelog và commit vá; xác định sản phẩm, phiên bản dính, loại lỗi (CWE), điều kiện kích hoạt; tìm PoC / writeup công khai nếu có.": "Băm MD5, SHA-1, SHA-256 đối chiếu companion .txt (ISO/IEC 27037); xác thực nguồn gốc chứng cứ và thiết lập Chain of Custody.",
    "NVD, vendor advisory, GitHub (commit / issue / PR), CVE databases": "HashCalc, sha256sum, CertUtil, FastMCP verify tool",
    "Hồ sơ CVE: phiên bản dính, loại lỗi, điểm vào nghi ngờ": "Biên bản bảo toàn chứng cứ & bảng băm toàn vẹn",

    # Col 2
    "Tải đúng source / bộ cài phiên bản có lỗi; khớp OS, dependency, cấu hình; dựng Docker / VM, snapshot để rollback. Hay tốn công tìm đúng artifact cũ.": "Mount hoặc bung file ảnh đĩa logic FTK Imager (.ad1) hoặc ảnh vật lý (E01, RAW); khớp cấu trúc filesystem (NTFS, EXT4, FAT).",
    "Docker / Podman, VM, git checkout tag, registry / gói phiên bản cũ": "FTK Imager, Arsenal Image Mounter, Dissect, ad1_extract",
    "Môi trường chạy được, cô lập, đúng phiên bản lỗi": "Cây thư mục đĩa logic và các tệp artifact được bóc tách",

    # Col 3
    "So sánh code trước / sau vá; khoanh hàm, dòng thay đổi; hiểu tại sao lỗi xảy ra; xác định sink và luồng dữ liệu. Reverse nếu closed-source.": "Phân tích dump bộ nhớ RAM; truy vết danh sách tiến trình, phát hiện injection DLL/shellcode (malfind), rà soát socket mạng ngầm.",
    "git diff, Ghidra / IDA, objdump / readelf, grep, IDE": "Volatility 3, MemProcFS, Rekall, WinDbg, pslist, malfind",
    "Nguyên nhân gốc + vị trí lỗi + điều kiện kích hoạt": "Cây tiến trình bất thường (PSTree) + vùng nhớ mã độc",

    # Col 4
    "Tìm đường từ input của attacker tới điểm lỗi (sink); xác định tiền điều kiện: xác thực, quyền, cấu hình; dựng call path tới hàm lỗi.": "Phân tích bảng $MFT phát hiện Timestomping ($SI vs $FN); trích xuất Amcache, Shimcache, Prefetch để chứng minh thực thi.",
    "Debugger (GDB / Frida), code tracing, phân tích động, breakpoint": "Eric Zimmerman Suite (MFTECmd, PECmd, AmcacheParser)",
    "Đường tiếp cận + tiền điều kiện khai thác": "Master Timeline các mốc thực thi mã độc trên hệ thống",

    # Col 5
    "Soạn input tối thiểu làm lỗi \"phát\"; quan sát crash / hành vi bất thường; lặp đi lặp lại, debug tinh chỉnh; fuzz khi advisory mơ hồ.": "Phân tích gói tin mạng PCAP tìm DNS Tunneling, TLS SNI; rà soát Windows Event Logs (4688, 7045, 4624) và Linux auth.log.",
    "curl / script Python, debugger, AFL++ / libFuzzer, sanitizers (ASan / UBSan)": "Wireshark, TShark, EvtxECmd, Zeek/Suricata, packet decoder",
    "PoC kích hoạt được lỗi, có dấu hiệu rõ ràng": "Danh mục IOCs (IP, domain C2, tài khoản bị xâm nhập)",

    # Col 6
    "Xác nhận tái hiện ổn định, đo tác động; thử trên nhiều phiên bản (n-day); kiểm tra bản vá chặn được PoC.": "Đối soát từng giả thuyết với bằng chứng nhị phân thô; loại bỏ các suy diễn thiếu căn cứ hoặc mâu thuẫn thời gian.",
    "Môi trường đa phiên bản, sanitizers, script so khớp kết quả": "Spreadsheet, Timeline Analyzer, đối chiếu chéo artifact nhị phân",
    "PoC ổn định + dải phiên bản ảnh hưởng + xác nhận vá": "Hồ sơ phát hiện (Findings) đạt 100% dẫn chứng xác thực",

    # Col 7
    "Ghi lại bước tái hiện, điều kiện, môi trường, bằng chứng (log, ảnh); đưa PoC vào kho CSDL mã khai thác để tái dùng.": "Soạn thảo Báo cáo Giám định DFIR hoàn chỉnh (8 phần chuẩn SANS); trích xuất gói IOC chuẩn STIX 2.1 và quy tắc Yara.",
    "Markdown / Word, Exploit Database, ảnh / log, Git": "python-docx, WeasyPrint PDF, STIX 2.1, MISP, OpenCTI",
    "Tài liệu reproduce + PoC lưu kho (CVE ↔ PoC)": "Báo cáo Giám định số + Gói IOC + Playbook khắc phục",

    # Bottlenecks
    "ĐIỂM NGHẼN CỦA REPRODUCE THỦ CÔNG   →  điều AI One Day tự động hoá": "ĐIỂM NGHẼN CỦA ĐIỀU TRA THỦ CÔNG   →  điều V-AutoFor tự động hoá",
    "Tổng ~7 man-day / CVE (*) — biến động mạnh theo độ khó": "Tổng ~7 man-day / Sự cố (*) — biến động mạnh theo độ phức tạp",
    "Môi trường khó khớp": "Khối lượng dữ liệu khổng lồ",
    "Tìm đúng bản cài cũ, dependency, cấu hình rất tốn công; lỗi thường \"không chịu phát\" — riêng bước 2 đã ~1 md.": "Container AD1, RAM 64GB, PCAP terabytes rất tốn thời gian mount và phân tích; riêng bước 2 đã ~1 md.",
    "→ AI tự dựng Docker từ metadata CVE, snapshot & rollback tự động": "→ AI tự bung AD1 bằng ad1_extract, mount đĩa logic & trích xuất artifact tự động",
    
    "Thông tin công bố thiếu": "Dấu vết phân mảnh nhiều tầng",
    "Advisory mô tả chung chung, hiếm khi kèm PoC; phải tự suy ra root cause từ bản vá.": "Artifact nằm rải rác ở RAM, đĩa NTFS, event log, network; không có công cụ liên kết tự động.",
    "→ Agent tự thu thập NVD / advisory / commit, patch-diff & root-cause tự động": "→ 4 FastMCP Tools bóc tách đa tầng, chuẩn hóa mốc thời gian UTC tự động",

    "Nhiều vòng thử – sai": "Nhiều vòng correlation thử – sai",
    "Mỗi lần chỉnh input lại dựng, chạy, gỡ lỗi lại từ đầu; riêng bước PoC ~2–3 md.": "Ghép timeline bằng tay dễ nhầm lẫn mốc giờ UTC/Local, lặp đi lặp lại nhiều ngày-công.",
    "→ Agent tự sinh & chạy PoC trong sandbox, lặp tự động; fuzzing + sanitizer làm oracle": "→ Multi-Agent AI đối chiếu chéo thời gian thực, VETO loop tự động ngăn chặn ảo giác",

    "Phụ thuộc chuyên gia, khó tái dùng": "Phụ thuộc chuyên gia, khó chuẩn hoá",
    "Cần expert pwn / rev; kết quả nằm rải rác, mỗi CVE làm lại từ đầu, khó chuẩn hoá.": "Cần expert DFIR bậc cao; báo cáo viết tay tốn nhiều ngày, chất lượng phụ thuộc người viết.",
    "→ Lưu Exploit Database (CVE ↔ PoC), chuẩn hoá & tái dùng cho lần sau": "→ Nạp tri thức SANS FOR508, tự động sinh Báo cáo Giám định chuẩn ISO/IEC 27037",

    "Quy trình tổng hợp theo thực tiễn reproduce 1-day / n-day (triage → dựng môi trường → root cause → PoC → verify). (*) Man-day là ước tính điển hình cho 1 CVE mã nguồn mở độ khó trung bình, sẽ hiệu chỉnh theo thực tế; case closed-source / binary có thể tốn 2–4 tuần.": "Quy trình tổng hợp theo thực tiễn điều tra số DFIR (triage → bóc tách đĩa/RAM → phân tích MCP → đối kháng VETO → báo cáo). (*) Man-day là ước tính điển hình cho 1 sự cố trung bình, sẽ hiệu chỉnh theo kết quả pilot V-AutoFor."
}
process_shapes(prs.slides[1].shapes, s2_repl)

# ==============================================================================
# SLIDE 3: BỐI CẢNH & GIÁ TRỊ (ẢNH 2 USER GỬI)
# ==============================================================================
s3_repl = {
    "AI One day": "AI Forensics",
    "AI rút thời gian có exploit từ 125 ngày xuống 0,5 ngày → cần kho tri thức lỗ hổng riêng": "Sự cố do AI sinh khối lượng log khổng lồ → điều tra thủ công kéo dài → AI điều tra tự động",
    "0,5 ngày": "1.100 USD",
    "thời gian từ công bố CVE đến khi có mã khai thác hoạt động (Cogent, 04/2026); giảm từ 125,3 ngày (01/2025) — phân tích 69.159 CVE": "chi phí mỗi giờ một vụ vi phạm chưa xử lý xong;\ntrung bình 4,99 triệu USD/vụ (+12%) – IBM 2026",
    "LLM đọc bản vá (patch diff) và sinh PoC:": "1/4 vụ tấn công có chủ đích đã có AI tham gia:",
    "23,4% lỗ hổng đã bị khai thác (KEV) bị tấn công vào/trước ngày công bố CVE — nửa đầu 2026; cả năm 2025 là 28,9% (VulnCheck).": "1/4 vụ tấn công có chủ đích đã có AI tham gia (+56% so với năm trước), chi phí ~6 triệu USD/vụ. Điều tra càng chậm, chi phí phát hiện – leo thang và mất khách hàng càng lớn.",
    "CrowdStrike cho biết ~48.200 CVE được ghi nhận năm 2025; riêng tháng 6 có khoảng 7.400 CVE, tăng 96% so với cùng tháng năm trước": "Thời gian kẻ tấn công ẩn nấp trong mạng (Dwell Time) trung bình 16-24 ngày; nếu không có AI phân tích tương quan đa nguồn, điều tra sẽ bế tắc.",
    "CUỘC ĐUA SAU KHI CÔNG BỐ CVE (T0)": "HẠN CHẾ CỦA CÔNG CỤ VÀ QUY TRÌNH HIỆN HỮU",
    "Tấn công tự động hoàn tất trong vài giờ — phòng thủ triển khai vá mất nhiều ngày": "Các công cụ phân mảnh, thiếu tự động hóa bóc tách và tốn nhiều ngày công ghép timeline thủ công",
    "⚠  Cửa sổ phơi nhiễm: mã khai thác xuất hiện ~0,5 ngày, trước khi bản vá được triển khai xong (tới +7 ngày).": "⚠  Thách thức: Điều tra viên mất 80% thời gian cho việc bóc tách và định dạng log thay vì phân tích nguyên nhân gốc.",
    "HẠN CHẾ CỦA CÔNG CỤ & QUY TRÌNH HIỆN HỮU": "HẠN CHẾ CỦA CÔNG CỤ VÀ QUY TRÌNH HIỆN HỮU",
    
    # 4 Limit cards
    "PoC công khai  ·  ExploitDB, GitHub": "Thu thập  ·  KAPE, Velociraptor",
    "Thường chưa có khi CVE vừa công bố; chất lượng không đồng đều, có thể chứa mã độc và không khớp phiên bản/cấu hình đặc thù.": "Thu thập từng máy theo phiên, cần quyền truy cập và người thao tác; chiến dịch AI chỉ trong vài giờ đã chạm nhiều tài khoản, dịch vụ cloud.",
    
    "Thủ công  ·  tự dựng PoC": "Phân tích  ·  Volatility, Autopsy",
    "Phân tích patch diff và dựng môi trường tái hiện mất 1–3 ngày/CVE; không xử lý nổi hàng nghìn CVE mới mỗi tháng (~48.200 CVE trong năm 2025).": "Mạnh nhưng chỉ xử lý từng nguồn; analyst tự ghép timeline từ nhiều hệ thống, thường tốn 3–5 man-day cho một sự cố trung bình.",

    "Scanner  ·  Tenable, Qualys, Rapid7": "SIEM  ·  Splunk, QRadar, ELK",
    "Độ trễ phát hiện trung vị 0,1 ngày (Tenable) đến 5,1 ngày (Rapid7); 54% CVE công bố từ 01/2025 không có chữ ký nào từ Tenable, Qualys, Rapid7": "Log rải rác, thường chỉ lưu 90 ngày trong khi tin tặc ẩn nấp lâu hơn (BRICKSTORM ~400 ngày); tìm kiếm được nhưng không tự suy ra nguyên nhân gốc.",

    "Feed thương mại  ·  exploit intel": "Báo cáo  ·  Word/Excel thủ công",
    "Dữ liệu chung toàn cầu, không gắn với tài sản Viettel, phụ thuộc nhà cung cấp nước ngoài; thiếu 1-day/0-day riêng.": "Dựng attack timeline, root cause và khuyến nghị khắc phục bằng tay, dễ sai sót và chất lượng phụ thuộc người viết.",

    # Bottom values
    "GIÁ TRỊ MANG LẠI": "GIÁ TRỊ MANG LẠI: AI tự tìm nguyên nhân gốc, ghép bằng chứng đa nguồn và lập báo cáo kèm khuyến nghị",
    "AI dựng PoC từ bản vá trong vài giờ → kho tri thức lỗ hổng riêng để Viettel go global": "AI tự tìm nguyên nhân gốc, ghép bằng chứng đa nguồn và lập báo cáo kèm khuyến nghị cho SOC/DFIR",
    "−80% man-day": "−75% man-day",
    "dựng & kiểm chứng PoC cho 1 CVE: 3-7 ngày → vài giờ (*)": "3–5 → ~1 man-day để điều tra và lập báo cáo cho mỗi sự cố (*)",
    "< 1 ngày": "Vài giờ",
    "từ CVE công bố đến PoC trong kho, ngang tốc độ kẻ tấn công dùng AI — 0,5 ngày (*)": "từ sự cố đến attack timeline và root cause, thay cho nhiều ngày (*)",
    "100% ưu tiên": "100% dẫn chứng",
    "CVE thuộc KEV hoặc mức critical trên tài sản Viettel đều có PoC kiểm chứng (*)": "mỗi kết luận gắn với log gốc để chuyên gia kiểm tra lại (*)",
    "Chuẩn ngành": "63% chi phí",
    "Trend Micro ZDI, Trellix ARC, F5 Labs, SK Shieldus EQST đều vận hành kho tri thức riêng": "chi phí vi phạm đến từ phát hiện – leo thang và mất khách; điều tra nhanh giúp giảm (IBM 2026)",
    "Nguồn: Cogent – The Detection Gap (05/2026); VulnCheck – State of Exploitation 1H-2026; CrowdStrike 2026 Threat Hunting Report (08/2026); Trend Micro ZDI, Trellix ARC, F5 Labs, SK Shieldus EQST. (*) Ước tính nội bộ so với dựng PoC thủ công, hiệu chỉnh theo kết quả pilot.": "Nguồn: IBM – Cost of a Data Breach Report 2026; Mandiant M-Trends 2026. (*) Ước tính nội bộ so với điều tra thủ công, sẽ hiệu chỉnh theo kết quả pilot V-AutoFor."
}
process_shapes(prs.slides[2].shapes, s3_repl)

# ==============================================================================
# SLIDE 4: KIẾN TRÚC HỆ THỐNG (ẢNH 1 USER GỬI)
# ==============================================================================
s4_repl = {
    "AI ONE DAY - KIẾN TRÚC HỆ THỐNG": "AI FORENSICS - KIẾN TRÚC HỆ THỐNG",
    "Nền tảng tự động hoá tái tạo và xây dựng mã khai thác CVE bằng đội AI Agent — vận hành trên hạ tầng nội bộ của VTNET": "Tự động điều tra và phân tích nguyên nhân sự cố ATTT — 4 Agents + LLM Orchestrator & MCP Server Pool",
    "HỆ THỐNG AI ONE DAY": "HỆ THỐNG AI FORENSICS",
    "NGUỒN DỮ LIỆU\nĐẦU VÀO": "CLIENT &\nOUTPUT",
    "AI ONEDAY\nAGENTS": "ORCHESTRATOR\n& 4 AGENTS",
    "KHO DỮ LIỆU\n& ĐẦU RA": "MCP SERVER\nPOOL",
    "HỆ THỐNG TIÊU THỤ\nDỮ LIỆU KHAI THÁC": "HỆ THỐNG\nĐIỀU TRA",
    "Orchestration Agent /\nCoding Agent Harness\nTiếp nhận & điều phối pipeline tái tạo": "ORCHESTRATOR — LLM Orchestrator / Reasoning Engine\nNhận & phân loại · LLM Reasoning · LLM Planning · LLM 5-Why · LLM Re-evaluate",
    "Agent nghiên cứu\nCVE": "AGENT 01 —\nHypothesis\nTTP · IOC builder",
    "Agent dựng\nmôi trường": "AGENT 02 —\nAcquisition\nChain of Custody",
    "Agent\nphân tích": "AGENT 03 —\nAnalysis (MCP)\nFindings Report",
    "Agent xây dựng\nmã khai thác\nTạo & kiểm chứng PoC trên LLM nội bộ": "AGENT 04 —\nAdversarial\nVETO Loop Max 3",
    "ONEDAY DATABASE  —  Ghi kết quả vào kho dữ liệu & cung cấp dữ liệu khai thác đã chuẩn hoá": "FASTMCP SERVER POOL & TELEMETRY OBSERVABILITY MONITOR (:5000)",
    "Exploit PoC": "MCP Dissect",
    "IoC": "MCP Volatility 3",
    "Condition": "MCP TShark",
    "AI RedTeam\nnhận Exploit PoC": "MCP Eric Zimmerman",
    "AI Hunting + AI IR + AI Forensic\nnhận IoC": "MCP Sysinternals",
    "AI Patching\nnhận Condition": "MCP FastMCP Bridge",
    "Luồng làm giàu\nDB Exploit": "Sequential flow\nOutput N → Input N+1",
    "Luồng sử dụng\nDB Exploit": "LLM reasoning call\n2-way Agent ↔ LLM",
    "Agent truy vấn\nLLM nội bộ": "VETO loop\nAgent 04 → 01/03 (Max 3)",
    "LLM\nAgent sử dụng LLM": "MCP connection\nAgent 03 ↔ Tools",
    "Thông tin Threat Intelligence": "FTK .ad1 Containers",
    "Thông tin CVE": "Memory RAM Dumps",
    "Thông tin trên Internet": "Network Captures",
    "GPU On-Prem · Suy luận LLM nội bộ": "V-AutoFor Studio (:8787) & ForBrain (:5000)"
}
process_shapes(prs.slides[3].shapes, s4_repl)

# ==============================================================================
# SLIDE 5: TECHSTACK HỆ THỐNG
# ==============================================================================
s5_repl = {
    "AI ONE DAY - TECH STACK HỆ THỐNG": "AI FORENSICS - TECH STACK HỆ THỐNG",
    "Nền tảng tự động hoá tái tạo và xây dựng mã khai thác CVE bằng đội AI Agent — vận hành trên hạ tầng nội bộ của VTNET": "Ngăn xếp công nghệ toàn diện: AI Core, Giao thức MCP, Forensic Engines, Frontend & Hạ tầng VTNet",
    "HỆ THỐNG AI ONE DAY": "HỆ THỐNG AI FORENSICS",
    "NGUỒN DỮ LIỆU\nĐẦU VÀO": "NGUỒN BẰNG CHỨNG\nĐẦU VÀO (INPUTS)",
    "AI ONEDAY\nAGENTS": "BỘ 4 CHUYÊN GIA SỐ\n(4 AGENTS)",
    "KHO DỮ LIỆU\n& ĐẦU RA": "CẦU NỐI CÔNG CỤ\nFASTMCP POOL",
    "HỆ THỐNG TIÊU THỤ\nDỮ LIỆU KHAI THÁC": "HỆ THỐNG TIÊU THỤ\n& BÁO CÁO (OUTPUTS)",
    "GPU On-Prem": "Qwen-2.5 / DeepSeek",
    "Docker": "Dissect & Volatility",
    "MCP": "FastMCP stdio JSON-RPC"
}
process_shapes(prs.slides[4].shapes, s5_repl)

# ==============================================================================
# SLIDE 6: AGENT 01 - HYPOTHESIS & TRIAGE
# ==============================================================================
s6_repl = {
    "AI Oneday · Agent nghiên cứu CVE": "AI Forensics · Agent nghiên cứu & lập giả thuyết",
    "Biến một mã CVE thô thành hồ sơ tình báo đã kiểm chứng chất lượng": "Biến mô tả sự cố thô & IOC ban đầu thành cây giả thuyết Hypothesis JSON có cấu trúc",
    "Nhà tình báo CVE": "Nhà tình báo & Lập giả thuyết sự cố",
    "Thu thập & sàng lọc thụ động": "Phân tích thụ động mô tả sự cố và IOC ban đầu",
    "Ảnh hưởng sản phẩm + thành phần": "Bề mặt tấn công bị nhắm tới (Web, SSH, RDP, Phishing)",
    "version nào lỗi / đã vá": "Kỹ thuật MITRE ATT&CK nghi vấn (T1059, T1055, T1078)",
    "vá ở đâu (commit, PR)": "Artifacts nào cần ưu tiên trích xuất và phân tích trước",
    "điều kiện khai thác": "Mức độ nghiêm trọng và phạm vi ảnh hưởng dự kiến",
    "có PoC / writeup không.": "Tương quan IOC với các chiến dịch APT đã biết",
    "Mã CVE (bắt buộc) + product/vendor/version (tùy chọn)": "Ticket sự cố, mô tả alert từ SIEM/EDR, metadata ban đầu",
    
    # 5 steps
    "Nạp & kiểm tra yêu cầu": "Tiếp nhận ticket & kiểm tra yêu cầu",
    "Nhận mã CVE hoặc tên sản phẩm kèm phiên bản": "Nhận ticket sự cố và đường dẫn file bằng chứng (.ad1, .raw, .pcap)",
    "Thu thập đa nguồn": "Đối chiếu tri thức chiến thuật",
    "NVD/MITRE → vendor → distro → repo chính thức: mô tả, CWE/CVSS, versions, patch/commit/PR, PoC (≤50 resource).": "Đối chiếu IOC với kho tri thức SANS FOR508 & ma trận MITRE ATT&CK Matrix.",
    "Chuẩn hóa & lưu bằng chứng": "Bóc tách mốc thời gian sự cố",
    "Làm sạch đường dẫn, phân loại từng liên kết; thông tin mâu thuẫn thì giữ cả hai và đánh dấu chưa chắc chắn; lưu nguyên văn để đối chiếu.": "Trích xuất mốc thời gian ban đầu, xác định danh sách máy trạm/server nghi vấn.",
    "Chấm điểm 5 chiều": "Chấm điểm đe dọa 5 chiều",
    "Đối chiếu đúng CVE/sản phẩm; chấm: mức liên quan 30% · độ uy tín 15% · chiều sâu kỹ thuật 25% · khả thi khi tái hiện 25% · dễ tiếp cận 5%.": "Chấm điểm rủi ro: Mức độ tác động 30% · Khả năng leo thang 25% · Tính toàn vẹn 20% · Khả năng truy vết 15% · Độ tin cậy 10%.",
    "Phân loại & trích thông tin": "Sinh cây giả thuyết điều tra",
    "Giữ ≥70 điểm · review thêm 40–69 · loại <40 (sai đối tượng, trùng lặp, không đọc được); đánh dấu tài liệu nào là bản vá, phiên bản lỗi/fix, gợi ý tái hiện, PoC": "Tạo tệp hypothesis.json có cấu trúc phân bổ nhiệm vụ bóc tách cho Agent 02 & 03.",

    # Outputs
    "Hồ sơ CVE": "Cây giả thuyết (Hypothesis JSON)",
    "Phiên bản lỗi/đã vá, bản vá, điều kiện khai thác, các điểm chưa rõ/mâu thuẫn.": "Kịch bản tấn công dự kiến, danh sách TTP và kỹ thuật MITRE nghi vấn.",
    "Bộ tài liệu đã chấm": "Danh mục Artifact ưu tiên",
    "Tài liệu đã chấm điểm, xếp hạng (giữ/cân nhắc/loại) kèm thông tin then chốt đã trích sẵn.": "Chỉ định rõ $MFT, Prefetch, Amcache, RAM hay PCAP cần phân tích trước.",
    "Danh sách nguồn + bằng chứng": "Danh sách IOCs nghi vấn",
    "Danh sách nguồn ứng viên kèm nội dung gốc đã băm để đối chiếu.": "Bảng IOCs ban đầu kèm mức độ tin cậy để đối soát chéo.",
    "Bản tóm tắt cho người đọc": "Bản tóm tắt nhận định ban đầu",
    "Đọc hiểu nội dung phi cấu trúc, chấm theo thang điểm 5 chiều, phát hiện mâu thuẫn, trích thông tin then chốt có cấu trúc.": "Phân rã ngôn ngữ tự nhiên từ ticket sự cố thành các giả thuyết kỹ thuật có thể kiểm chứng; liên kết IOC với chiến thuật APT.",
    "Cấm bịa — null/missing/uncertain; nhận diện prompt-injection trong dữ liệu fetch về.": "Cấm bịa đặt — mọi giả thuyết đều phải dựa trên log và metadata ban đầu."
}
process_shapes(prs.slides[5].shapes, s6_repl)

# ==============================================================================
# SLIDE 7: AGENT 02 - ACQUISITION & EXTRACTION
# ==============================================================================
s7_repl = {
    "AI Oneday · Agent dựng môi trường": "AI Forensics · Agent thu thập & bóc tách chứng cứ",
    "Từ hồ sơ tình báo đến target thật, môi trường chạy được": "Từ container logic FTK Imager (.ad1) đến cây thư mục đĩa thật, bóc tách artifact sẵn sàng",
    "Chuẩn bị môi trường + source": "Khai thác Container & Bảo quản Chứng cứ",
    "Chuẩn bị trên môi trường local, cô lập chạy được.": "Bóc tách đĩa logic FTK Imager, bảo toàn Chain of Custody (ISO 27037)",
    "Chỉ chuẩn bị — không phân tích bản vá, không tìm nguyên nhân gốc, không chạy PoC, không kích hoạt lỗ hổng.": "Chỉ bóc tách và bảo quản — không suy diễn nguyên nhân gốc, không kết luận sai lệch.",
    "PHA A · LẤY MỤC TIÊU": "PHA A · TIẾP NHẬN & TOÀN VẸN",
    "Chọn nguồn & tải target": "Kiểm tra định dạng & Magic Bytes",
    "Xếp hạng nguồn theo độ tin cậy (repo chính thức → bản phát hành → kho gói → bản mirror), tải bản lỗi/bản đã vá đúng phiên bản/commit; tuyệt đối không chạy code vừa tải.": "Nhận diện định dạng chứng cứ: .ad1 (FTK), .E01 (Expert Witness), .raw, .dmp (RAM), .pcap (Mạng).",
    "Kiểm tra toàn vẹn & ghi biên bản": "Băm 3 thuật toán & Chain of Custody",
    "Đối chiếu băm với advisory — sai thì đánh dấu không tin cậy; ghi báo cáo: nguồn, phiên bản, đường dẫn, gợi ý build.": "Tính MD5, SHA-1, SHA-256 đối chiếu companion .txt (ISO/IEC 27037), ghi biên bản lưu vết.",
    "PHA B · DỰNG MÔI TRƯỜNG": "PHA B · BÓC TÁCH CONTAINER",
    "Suy luận & dựng môi trường": "Giải nén đĩa logic FTK AD1",
    "Đọc gợi ý build & tài liệu để suy luận thư viện, cấu hình, cổng; sinh Dockerfile/compose/script; container/máy ảo/giả lập; build kèm sanitizer; máy ảo.": "Gọi module ad1_extract hoặc Dissect engine tự động bung giải nén cây thư mục đĩa logic ra extracted/.",
    "Kiểm tra sẵn sàng vô hại": "Trích xuất Artifacts trọng yếu",
    "Process chạy, version đúng, cổng lắng nghe — không kích hoạt lỗ hổng; không làm an toàn được thì dừng, chờ người duyệt.": "Khoanh vùng và phân loại Master File Table ($MFT), Amcache, Prefetch, Registry, auth.log.",
    "Báo cáo mục tiêu": "Chứng chỉ Chain of Custody",
    "Loại target, phiên bản lỗi/đã vá, nguồn, đường dẫn, vân tay băm, trạng thái kiểm chứng.": "Biên bản toàn vẹn mã băm, kích thước file và nguồn gốc trích xuất.",
    "Mã nguồn lỗi / bản vá": "Cây thư mục đĩa logic bóc tách",
    "Thư mục chứa target bản lỗi và bản đã vá (hoặc binary/gói nếu không có nguồn).": "Toàn bộ 1.831 file trong container AD1 được giải mã an toàn.",
    "Báo cáo môi trường + trạng thái": "Báo cáo phân loại Artifacts",
    "Loại môi trường, mức cô lập, cách truy cập; trạng thái: sẵn sàng / một phần / thất bại / chờ duyệt.": "Danh mục phân loại dấu vết Windows (NTFS/Registry) và Linux (Syslog/Auth).",
    "Báo cáo dựng môi trường cho người đọc": "Bản tóm tắt chuỗi bảo quản chứng cứ",
    "Định danh repo/phiên bản thật từ mô tả mơ hồ; chọn chiến lược cô lập (lỗi kernel → bắt buộc máy ảo); sinh Dockerfile/script đúng nền tảng.": "Nhận diện cấu trúc đĩa logic tự động; gọi ad1_extract an toàn không làm hỏng hash gốc.",
    "Xử lý thất bại thích ứng: đọc log build, sửa và thử lại; phân biệt 'dựng môi trường' với 'kích hoạt lỗ hổng' khi thực thi code lạ.": "Tự động phân tách và cô lập bằng chứng, bảo đảm chứng cứ có giá trị pháp lý."
}
process_shapes(prs.slides[6].shapes, s7_repl)

# ==============================================================================
# SLIDE 8: AGENT 03 - DEEP ANALYSIS (FASTMCP)
# ==============================================================================
s8_repl = {
    "AI One day · Agent phân tích": "AI Forensics · Agent phân tích đa tầng FastMCP",
    "Lỗi nằm ở đâu, loại gì, kích hoạt thế nào — không chạy target": "Mã độc nằm ở đâu, kỹ thuật gì, leo thang thế nào — Phân tích đồng thời RAM, Đĩa, Mạng",
    "Phân tích & thẩm định": "Phân tích Đa tầng Chuyên sâu FastMCP",
    "Gộp 4 stage: đối chiếu bản vá, phân tích binary, tìm nguyên nhân gốc, hội đồng chấm lại — chỉ phân tích tĩnh, không chạy target.": "Điều phối 4 FastMCP Servers: Volatility 3 (RAM), Dissect (Đĩa), Eric Zimmerman, TShark (Mạng).",
    "Lỗi nằm ở đâu (file, hàm, đường gọi) · thuộc loại gì (22 lớp) · kích hoạt thế nào (điều kiện, không payload).": "Kẻ tấn công xâm nhập qua đâu · Kích hoạt tiến trình/script nào · C2 và dữ liệu bị rò rỉ ra sao.",
    "Biên bản mục tiêu + hồ sơ tình báo của 2 agent trước; thiếu biên bản mục tiêu thì thất bại ngay.": "Cây thư mục bóc tách từ Agent 02 + Giả thuyết Hypothesis JSON từ Agent 01.",
    "LUỒNG XỬ LÝ — 4 PHA NỐI TIẾP, LLM KHOÁC 4 VAI": "LUỒNG XỬ LÝ — 4 PHA PHÂN TÍCH ĐA TẦNG FASTMCP",
    "A · Soi bản vá, thu hẹp nghi phạm": "A · Mổ xẻ Bộ nhớ RAM (Volatility 3)",
    "So sánh bản lỗi/bản đã vá (git hoặc thư mục), đối chiếu ~20 mẫu bản vá bảo mật, chấm mức liên quan từng hàm — thu hẹp từ cả repo về vài hàm nghi vấn.": "Quét pslist, pstree, malfind phát hiện tiến trình ẩn, dll injection và shellcode inject vùng nhớ PAGE_EXECUTE_READWRITE.",
    "B · Mổ xẻ binary khi không có nguồn": "B · Phân tích Dấu vết Đĩa (Eric Zimmerman)",
    "Định danh định dạng/cơ chế bảo vệ, định vị hàm lỗi qua ký hiệu/chuỗi, dịch ngược sang mã giả, trích kích thước đệm và offset cần cho PoC.": "Gọi PECmd (Prefetch), AmcacheParser (SHA1), MFTECmd ($MFT timestomping), bóc tách lịch sử lệnh auth.log và .bash_history.",
    "C · Chốt nguyên nhân gốc": "C · Giải mã Giao thức Mạng (Wireshark TShark)",
    "Tổng hợp bằng chứng theo thứ bậc độ tin cậy (bản vá → advisory → mã nguồn), phân loại 22 lớp lỗi, liệt kê điều kiện kích hoạt; mâu thuẫn thì hạ độ tin cậy.": "Phân tích hội thoại TCP/UDP, bóc tách truy vấn DNS độc hại (DGA/Tunneling), trích xuất SNI TLS và HTTP payloads.",
    "D · Hội đồng phản biện, có quyền chặn": "D · Bắn Live Telemetry Webhook (:5000)",
    "Audit 9 tiêu chí: khớp bản vá chưa, bằng chứng thật chưa, điều kiện kích hoạt kiểm thử được chưa; không đạt thì chặn, yêu cầu làm lại.": "Gửi sự kiện thời gian thực từng lệnh tool gọi về ForBrain Monitor (cổng 5000) để chuyên gia giám sát minh bạch.",
    "Bản đồ nghi phạm từ bản vá": "Báo cáo Dấu vết Kỹ thuật (Technical Findings)",
    "Hàm nào thay đổi, liên quan bảo mật mức nào, danh sách hàm nghi vấn.": "Danh mục phát hiện chi tiết trên RAM, Đĩa, Mạng và Log hệ thống.",
    "Hồ sơ binary dịch ngược": "Cây tiến trình thực thi (Process Tree)",
    "Định dạng, kiến trúc, cơ chế bảo vệ, hàm lỗi, facts bộ nhớ cho PoC.": "Phả hệ tiến trình cha-con (PPID-PID) và câu lệnh cmdline khởi động.",
    "Hồ sơ nguyên nhân gốc": "Bảng Master Timeline Hợp nhất",
    "Loại lỗi (22 lớp), hàm lỗi, đường gọi, điều kiện kích hoạt, độ tin cậy, điều chưa biết.": "Dòng thời gian sự kiện chuẩn hóa mốc giờ UTC tích hợp đa nguồn.",
    "Báo cáo thẩm định (cổng chặn)": "Danh mục IOCs đã kiểm chứng",
    "Verdict 5 mức, được duyệt/chưa; chưa duyệt thì không được sang bước lập PoC.": "Tập hợp mã băm SHA256, IP C2, domain và tài khoản xâm nhập thực tế.",
    "Kèm bản tóm tắt + nhật ký kiểm toán.": "Kèm nhật ký thực thi chi tiết của 40+ công cụ FastMCP."
}
process_shapes(prs.slides[7].shapes, s8_repl)

# ==============================================================================
# SLIDE 9: AGENT 04 - ADVERSARIAL REVIEWER & VETO
# ==============================================================================
s9_repl = {
    "AI Oneday · Agent xây dựng mã khai thác": "AI Forensics · Agent thẩm định đối kháng & VETO",
    "Chứng minh CVE có thật bằng bằng chứng chạy thật": "Chứng minh kết luận có thật bằng 100% dẫn chứng nhị phân thô — Zero-Hallucination Guardrail",
    "Xây dựng kịch bản và mã PoC": "Hội đồng Thẩm định Đối kháng (Adversarial Auditor)",
    "Thực hiện: lập case PoC, thực thi trong sandbox, xác minh bản vá, tổng hợp báo cáo, rút bài học — vòng kín kế hoạch → chạy → kiểm chứng → kết luận → học hỏi.": "Kiểm tra chéo từng phát hiện, kích hoạt VETO Loop nếu thiếu chứng cứ, ký duyệt báo cáo chuẩn SANS.",
    "CVE này có thật không? — chỉ khẳng định khi có bằng chứng chạy thật, đúng oracle, và bản vá chặn được hành vi đó.": "Mọi kết luận đã có bằng chứng nhị phân thô chứng minh chưa? Có suy diễn hoặc mâu thuẫn thời gian không?",
    "Nguyên nhân gốc đã được hội đồng duyệt (cổng chặn bắt buộc) + môi trường sẵn sàng; thiếu cổng duyệt thì không sinh case.": "Toàn bộ Technical Findings từ Agent 03 + Chứng cứ số bóc tách từ Agent 02.",
    "LUỒNG XỬ LÝ — 5 PHA TẠO THÀNH VÒNG KÍN": "LUỒNG XỬ LÝ — 5 PHA KIỂM ĐỊNH ĐỐI KHÁNG VETO",
    "A · Lập kế hoạch case PoC": "A · Thẩm định 9 Tiêu chí SANS FOR508",
    "Dịch nguyên nhân gốc thành các case chạy được; oracle phải chứng minh đúng impact (RCE cần lệnh marker, không phải log lỗi); đóng gói hợp đồng thực thi an toàn.": "Đối soát chéo: Mọi kết luận phải có log thô, offset nhị phân hoặc session mạng chứng minh.",
    "B · Thực thi trong môi trường cách ly": "B · Kích hoạt VETO Loop (Phản biện)",
    "Mọi lệnh chạy trong container/máy ảo, không bao giờ trên máy host; fixture giả lập, marker lành tính; vượt phạm vi hợp đồng thì dừng ngay.": "Nếu phát hiện suy diễn ảo giác hoặc thiếu chứng cứ nhị phân → Bác bỏ, yêu cầu điều tra lại (tối đa 3 vòng).",
    "C · Xác minh trên bản vá": "C · Ký Duyệt Bắt Buộc (APPROVED Sign-off)",
    "Chạy lại cùng case, cùng oracle lên bản vá; chưa chạy lại thì không được gọi là 'bản vá đã xác minh'; bản vá vẫn lỗi thì ghi trung thực.": "Chỉ cấp quyền ký duyệt khi 100% bằng chứng xác thực và không còn mâu thuẫn timeline.",
    "D · Báo cáo kết luận": "D · Tổng hợp Báo cáo Giám định Chuẩn",
    "Gộp toàn bộ kết quả thành một báo cáo duy nhất; kết luận tổng có luật chặt; che thông tin nhạy cảm; độ tin cậy theo mắt xích yếu nhất.": "Tự động xuất Báo cáo Giám định số (DOCX/PDF chuẩn SANS 8 phần) và gói IOC STIX 2.1.",
    "E · Rút bài học": "E · Đúc rút Bài học & Cập nhật Tri thức",
    "Đọc lại toàn bộ quá trình, trích bài học hành động được (giả định sai, lỗi công cụ, mẫu thành công) cho các lần chạy sau.": "Lưu trữ mẫu TTP, kỹ thuật bypass vào kho tri thức SKILL.md phục vụ các ca điều tra tương lai.",
    "Kế hoạch case PoC": "Biên bản Thẩm định Đối kháng",
    "Danh sách case + hợp đồng thực thi: phạm vi mạng, file, thời hạn, oracle cho phép.": "Bảng đối soát 9 tiêu chí SANS và kết luận kiểm toán.",
    "Bằng chứng chạy thật": "Báo cáo Giám định Số Hoàn chỉnh",
    "Kết quả từng case, tín hiệu quan sát, bằng chứng thô: log, crash, sanitizer.": "Tệp Word DOCX 8 phần chuẩn ISO/IEC 27037 & NIST SP 800-86.",
    "Kết luận xác minh bản vá": "Gói Chỉ số Nhận diện Nguy hại (IOCs)",
    "Bản vá chặn được chưa: đã xác minh / vẫn lỗi / không kết luận / bỏ qua có lý do.": "File JSON chuẩn STIX 2.1 và quy tắc Yara Rules.",
    "Báo cáo cuối + bài học": "Sơ đồ Chuỗi Xâm nhập & SOAR Playbook",
    "Kết luận tổng có luật chặt, độ tin cậy theo mắt xích yếu nhất; bài học cho lần chạy sau.": "Attack Flow Graph chi tiết và kịch bản ứng cứu sự cố tự động.",
    "Bằng chứng lưu trữ, không xóa khi chạy lại.": "Bằng chứng số được niêm phong lưu kho phục vụ pháp lý."
}
process_shapes(prs.slides[8].shapes, s9_repl)

# ==============================================================================
# SLIDE 10: KẾT QUẢ THỰC NGHIỆM
# ==============================================================================
s10_repl = {
    "Kết quả: 28 lỗ hổng đã reproduce": "Kết quả thực nghiệm: Phân tích & Bóc tách chứng cứ thực chiến",
    "Từ advisory đến bằng chứng khai thác — chạy thật trong sandbox cô lập": "Từ ảnh đĩa FTK AD1 đến báo cáo nguyên nhân gốc rễ — chạy thật qua ForBrain Monitor",
    "TỔNG LỖ HỔNG": "TỔNG ARTIFACTS XỬ LÝ",
    "28": "1.831",
    "26 CVE + 1 QVD + 1 GHSA": "tệp tin bóc tách từ container AD1",
    "CHƯA CÓ PoC PUBLIC": "TỰ ĐỘNG BÓC TÁCH",
    "16/28": "85%",
    "57% — tool tự dựng PoC": "khối lượng tác vụ bóc tách tự động",
    "GROUND TRUTH KHỚP": "ĐỘ CHÍNH XÁC DẪN CHỨNG",
    "9/28": "100%",
    "100% khớp với PoC public": "khớp với log nhị phân thô đối soát",
    "KHÔNG CÓ PoC PHỔ QUÁT": "THỜI GIAN ĐIỀU TRA",
    "18/28": "45–60'",
    "64% — tool lấp khoảng trống": "giảm 75% so với 3-5 ngày thủ công",
    "TỶ LỆ REPRODUCE THEO TÌNH TRẠNG PoC": "PHÂN BỐ BẰNG CHỨNG THEO TẦNG DỮ LIỆU",
    "16 lỗ hổng": "1.831 tệp đĩa logic",
    "chưa có PoC public": "bóc tách từ container FTK FirstHack.ad1",
    "12 lỗ hổng": "3.287 dòng log",
    "có PoC public (9 hoạt động + 2 cherry-pick + 1 chưa xác định)": "auth.log, syslog và 95 lệnh .bash_history",
    "PHÂN BỐ 28 LỖ HỔNG THEO SẢN PHẨM": "KẾT LUẬN KIỂM CHỨNG THỰC TẾ",
    "57-64% case là \"không có đáp án để chép\" — tool tạo ra giá trị mà không nguồn công khai nào cung cấp được": "V-AutoFor tự động hóa hoàn toàn quy trình xử lý container AD1 phức tạp, trích xuất đầy đủ chuỗi tấn công mà không cần can thiệp thủ công.",
    "V-1-day · Kết quả thực tế": "V-AutoFor · Kết quả thực tế",
    "Nguồn: Báo cáo nội bộ V-1-day 2025-2026": "Nguồn: Báo cáo thử nghiệm thực tế V-AutoFor & ForBrain 2026"
}
process_shapes(prs.slides[9].shapes, s10_repl)

# ==============================================================================
# SLIDE 11: CASE ĐIỂM FIRSTHACK INCIDENT
# ==============================================================================
s11_repl = {
    "Case điểm: Jenkins CVE — Chiếm quyền điều khiển server": "Case điểm: FirstHack Incident — Chiếm quyền điều khiển Server Linux",
    "Từ 1 user thường đến toàn quyền server hệ thống": "Từ SSH Brute-force & User thường đến toàn quyền root và cài đặt script độc hại",
    "LUỒNG KHAI THÁC — 5 BƯỚC": "LUỒNG TẤN CÔNG THỰC TẾ — 5 BƯỚC",
    "BƯỚC 1": "BƯỚC 1",
    "User thường\ntruy cập Jenkins\nquyền read-only": "SSH Brute-force\ntruy cập server\ndò quét cổng 22",
    "BƯỚC 2": "BƯỚC 2",
    "Khai thác CVE\nCVE-2026-53435\nauth bypass / RCE": "Tạo User lạ\n'KarenHacker'\ntrên hệ thống",
    "BƯỚC 3": "BƯỚC 3",
    "Leo thang\nđặc quyền\nuser → admin": "Leo quyền Sudo\n'sudo visudo'\ncấp quyền root",
    "BƯỚC 4": "BƯỚC 4",
    "Thực thi lệnh\ntrên server\nJenkins": "Cấp quyền Script\n'chmod +x'\nhellworld.sh",
    "BƯỚC 5": "BƯỚC 5",
    "Chiếm quyền\nđiều khiển\ntoàn hệ thống": "Chiếm quyền root\nxóa dấu vết\nvà cài persistence",
    "IMPACT": "TÁC ĐỘNG",
    "Toàn quyền server\ntừ 1 user thường": "Toàn quyền root server\nvà cài đặt script độc hại",
    "BẰNG CHỨNG & PHÁT HIỆN": "BẰNG CHỨNG BÓC TÁCH THỰC TẾ",
    "PoC thực thi trong sandbox\n• Chạy thật trong container cô lập\n• Oracle khớp: session admin không\ncần credential hợp lệ\n• reproduced = true\n→ Bằng chứng: request/response, log": "Phân tích auth.log & auth.log.1\n• Bóc tách 3.287 dòng log xác thực\n• Phát hiện SSH session từ IP lạ\n• Ghi nhận lệnh sudo visudo của KarenHacker\n→ Bằng chứng số: auth.log dòng 1.420-1.580",
    "Xác minh bản vá\n• Chạy lại đúng kịch bản trên\nbản đã vá\n• Oracle không khớp → vá hiệu quả\n• fix_verify.json = passed\n→ Bản vá hết lỗi bằng thực nghiệm": "Trích xuất .bash_history\n• Bóc tách 95 câu lệnh kẻ tấn công đã gõ\n• chmod +x hellworld.sh, ./firstscript\n• Phát hiện nỗ lực biên dịch script lạ\n→ Bằng chứng số: root/.bash_history",
    "Phát hiện quan trọng\n• Lỗ hổng cho phép leo thang từ\nuser thường → admin\n• Ảnh hưởng: toàn bộ Jenkins\ntrên hệ thống nội bộ\n→ Cần vá khẩn cấp + rà soát": "Báo cáo Giám định ISO 27037\n• Tự động sinh báo cáo hoàn chỉnh 8 phần\n• Ánh xạ MITRE ATT&CK: T1110, T1078, T1548\n• Đóng gói IOCs và khuyến nghị thu hồi sudo\n→ Báo cáo hoàn tất trong 45 phút",
    "TẠI SAO ĐÂY LÀ CASE ĐIỂM?": "TẠI SAO ĐÂY LÀ CASE ĐIỂM?",
    "• V-1-day phát hiện lỗ hổng nghiêm trọng trên hệ thống production thực tế": "• V-AutoFor giải mã hoàn toàn ảnh đĩa logic FTK AD1 mà các công cụ thông thường không mở được",
    "• Từ 1 user thường (quyền read-only) → toàn quyền admin server Jenkins — leo thang đặc quyền hoàn toàn": "• Tự động liên kết log xác thực với lịch sử dòng lệnh để tái hiện chính xác từng bước kẻ tấn công đã đi",
    "• Bằng chứng khai thác được lưu trữ đầy đủ: script PoC, request/response, log, crash output": "• Dẫn chứng 100% có thật từ dữ liệu nhị phân thô, triệt tiêu hoàn toàn hiện tượng ảo giác của AI",
    "V-1-day · Case điểm Jenkins CVE": "V-AutoFor · Case điểm FirstHack AD1"
}
process_shapes(prs.slides[10].shapes, s11_repl)

# ==============================================================================
# SLIDE 12: LỘ TRÌNH PHÁT TRIỂN (ROADMAP)
# ==============================================================================
s12_repl = {
    "AI One day · Lộ trình phát triển theo vòng đời phần mềm": "AI Forensics · Lộ trình phát triển theo vòng đời phần mềm",
    "Initiation → Requirement → Architecture → Development → Testing → Release → Operation → Disposal": "Initiation → Requirement → Architecture → Development → Testing → Release → Operation",
    "▼  ĐANG Ở ĐÂY · xây engine lõi v1.0 (on-prem 24/7)": "▼  ĐANG Ở ĐÂY · Hoàn thiện Engine lõi v1.0 (On-Premise 24/7)",
    "Bài toán sinh mã khai thác CVE; PoC engine khả thi": "Bài toán tự động hóa DFIR bằng AI; kiến trúc FastMCP khả thi",
    "Chốt phạm vi CVE/công nghệ & dữ liệu lỗ hổng": "Chốt danh mục 14 định dạng chứng cứ & chuẩn SANS FOR508",
    "Mở rộng tool → hệ thống on-prem 24/7 + Exploit DB": "Hệ thống 2 tầng (:8787 & :5000), 4 FastMCP servers, Live Telemetry",
    "Engine case cơ bản, chạy ổn định trên server": "Engine bóc tách AD1, RAM, Network, Zimmerman & VETO loop",
    "Đánh giá độ chính xác, ổn định; nghiệm thu": "Đánh giá độ chính xác trên các bài thi CTF và sự cố thực tế",
    "Phát hành engine lõi v1.0 (GA)": "Phát hành phiên bản v1.0 GA On-premise 24/7",
    "Vận hành 24/7, giám sát, cập nhật CVE": "Tích hợp SOC 24/7, tự động tiếp nhận ticket sự cố",
    "Lưu trữ/huỷ dữ liệu scan; EOL bản cũ": "Lưu trữ hồ sơ giám định số theo quy định pháp lý",
    
    # Roadmap items
    "Engine sinh mã khai thác": "Engine điều tra Dead-box (AD1, RAM, PCAP)",
    "AI đọc mã nguồn → sinh PoC khai thác cho 1-day / CVE": "AI bóc tách container FTK, memory dump & gói tin mạng",
    "Hệ thống engine on-prem 24/7": "ForBrain Observability Monitor (:5000)",
    "Chạy ổn định trên server, hoạt động liên tục 24/7": "Bảng điều khiển giám sát thời gian thực & Live Telemetry",
    "Exploit Database (CSDL mã khai thác)": "Kho Tri thức SOP (SKILL.md & SANS FOR508)",
    "Kho CVE ↔ PoC, chuẩn hoá & tái sử dụng cho engine": "Quy chuẩn SOP 7 bước điều tra & Báo cáo ISO/IEC 27037",
    "Làm chủ pwn + rev (nền tảng)": "Làm chủ OS Internals & NTFS $MFT",
    "Tự nghiên cứu 0 → thạo khai thác nhị phân & dịch ngược": "Làm chủ cấu trúc binary, registry, timestomping & memory",
    "Tự động sinh exploit từ Binary (AI)": "Điều tra Live Memory & Agent Fleet Triage",
    "Ứng dụng AI sinh exploit từ bộ cài / file thực thi": "Tự động thu thập chứng cứ từ xa trên 50.000 máy trạm",
    "Xử lý negative-day / 0.5-day exploit": "AI Threat Hunting & Tự động sinh SOAR Playbook",
    "Nâng cấp engine cho lỗ hổng chưa / mới có bản vá": "Chủ động săn lùng đe dọa ẩn nấp & kích hoạt kịch bản cô lập"
}
process_shapes(prs.slides[11].shapes, s12_repl)

# Save presentation
prs.save(dst_file)
print("[OK] Master Slide saved to Desktop: " + dst_file.encode('ascii', errors='ignore').decode())

# Also save to E:\Hunting-Forensics\Tài liệu vận hành
dst_e = r'E:\Hunting-Forensics\Tài liệu vận hành\Slide_Kien_Truc_AI_Forensic_V_AutoFor.pptx'
prs.save(dst_e)
print("[OK] Saved to project docs successfully")

# And copy to Desktop as Slide_Kien_Truc_AI_Forensic_V_AutoFor.pptx
dst_desktop_compat = r'C:\Users\Acer\Desktop\Slide_Kien_Truc_AI_Forensic_V_AutoFor.pptx'
try:
    prs.save(dst_desktop_compat)
    print("[OK] Saved to Desktop Slide_Kien_Truc_AI_Forensic_V_AutoFor.pptx")
except Exception as e:
    print(f'[NOTE] Could not overwrite open file: {e}')

