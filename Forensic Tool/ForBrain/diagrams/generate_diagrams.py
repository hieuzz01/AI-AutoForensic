import matplotlib.pyplot as plt
import matplotlib.patches as patches
from pathlib import Path

def generate_diagrams():
    out_dir = Path(r"E:\Hunting-Forensics\Forensic Tool\ForBrain\diagrams")
    out_dir.mkdir(parents=True, exist_ok=True)
    
    # -------------------------------------------------------------
    # DIAGRAM 1: SƠ ĐỒ HẠ TẦNG & KIẾN TRÚC SẢN PHẨM (INFRASTRUCTURE ARCHITECTURE)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 7.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')
    
    # Title
    ax.text(50, 96, "SƠ ĐỒ HẠ TẦNG VÀ PHÂN TẦNG KIẾN TRÚC NỀN TẢNG V-AUTOFOR & FORBRAIN", 
            ha='center', va='center', fontsize=13, fontweight='bold', color='#0F172A')
    ax.text(50, 93, "Mô hình Phân tách Độc lập: AI Reasoning Agent Studio (Port 8787) - Observability Monitor (Port 5000) - FastMCP Bridge", 
            ha='center', va='center', fontsize=8.5, fontstyle='italic', color='#475569')

    # Color definitions
    c_tier_bg = ['#F8FAFC', '#EFF6FF', '#F0FDF4', '#FAF5FF', '#FFFBEB']
    c_tier_border = ['#94A3B8', '#3B82F6', '#10B981', '#8B5CF6', '#F59E0B']

    # Tier 1: User & UI Layer
    rect1 = patches.FancyBboxPatch((4, 76), 92, 14, boxstyle="round,pad=0.8", ec=c_tier_border[1], fc='#EFF6FF', lw=1.5)
    ax.add_patch(rect1)
    ax.text(6, 87.5, "TẦNG 1: GIAO DIỆN NGƯỜI DÙNG & GIÁM SÁT TRỰC QUAN (USER & OBSERVABILITY INTERFACE)", fontsize=8.5, fontweight='bold', color='#1E40AF')
    
    box_u1 = patches.FancyBboxPatch((6, 78), 27, 8, boxstyle="round,pad=0.5", ec='#3B82F6', fc='#FFFFFF', lw=1)
    ax.add_patch(box_u1)
    ax.text(19.5, 83, "V-AutoFor AI Studio", ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')
    ax.text(19.5, 80, "Port 8787 (Multi-turn Chat & Prompt)", ha='center', va='center', fontsize=7, color='#64748B')

    box_u2 = patches.FancyBboxPatch((36.5, 78), 27, 8, boxstyle="round,pad=0.5", ec='#0284C7', fc='#FFFFFF', lw=1)
    ax.add_patch(box_u2)
    ax.text(50, 83, "ForBrain Observability Monitor", ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')
    ax.text(50, 80, "Port 5000 (Live Telemetry Feed & GUI)", ha='center', va='center', fontsize=7, color='#64748B')

    box_u3 = patches.FancyBboxPatch((67, 78), 27, 8, boxstyle="round,pad=0.5", ec='#0D9488', fc='#FFFFFF', lw=1)
    ax.add_patch(box_u3)
    ax.text(80.5, 83, "9Router AI Model Hub", ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')
    ax.text(80.5, 80, "Port 20128 (Key Management & Proxy)", ha='center', va='center', fontsize=7, color='#64748B')

    # Tier 2: Agent Reasoning & Brain Layer
    rect2 = patches.FancyBboxPatch((4, 58), 92, 14, boxstyle="round,pad=0.8", ec=c_tier_border[3], fc='#FAF5FF', lw=1.5)
    ax.add_patch(rect2)
    ax.text(6, 69.5, "TẦNG 2: BỘ NÃO SUY LUẬN & ĐIỀU PHỐI ĐA TÁC TỬ (AGENTIC ORCHESTRATION & REASONING CORE)", fontsize=8.5, fontweight='bold', color='#6B21A8')

    box_r1 = patches.FancyBboxPatch((6, 60), 27, 8, boxstyle="round,pad=0.5", ec='#8B5CF6', fc='#FFFFFF', lw=1)
    ax.add_patch(box_r1)
    ax.text(19.5, 65, "Reasonix Go Agent Engine", ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')
    ax.text(19.5, 62, "Task Planner, Context, VETO Rails", ha='center', va='center', fontsize=7, color='#64748B')

    box_r2 = patches.FancyBboxPatch((36.5, 60), 27, 8, boxstyle="round,pad=0.5", ec='#A855F7', fc='#FFFFFF', lw=1)
    ax.add_patch(box_r2)
    ax.text(50, 65, "Mô hình AI: Gemini 3.8 / DeepSeek-R1", ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')
    ax.text(50, 62, "Chuỗi tư duy Chain-of-Thought", ha='center', va='center', fontsize=7, color='#64748B')

    box_r3 = patches.FancyBboxPatch((67, 60), 27, 8, boxstyle="round,pad=0.5", ec='#C084FC', fc='#FFFFFF', lw=1)
    ax.add_patch(box_r3)
    ax.text(80.5, 65, "Kho Tri thức (Skills Repository)", ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')
    ax.text(80.5, 62, "SOP 7 bước & Khung Báo cáo DFIR", ha='center', va='center', fontsize=7, color='#64748B')

    # Tier 3: FastMCP Gateway Layer
    rect3 = patches.FancyBboxPatch((4, 38), 92, 16, boxstyle="round,pad=0.8", ec=c_tier_border[2], fc='#F0FDF4', lw=1.5)
    ax.add_patch(rect3)
    ax.text(6, 51.5, "TẦNG 3: CẦU NỐI CÔNG CỤ FASTMCP VÀ LIVE TELEMETRY STREAM (40+ FORENSIC TOOLS)", fontsize=8.5, fontweight='bold', color='#065F46')

    box_m1 = patches.FancyBboxPatch((6, 40), 20, 10, boxstyle="round,pad=0.5", ec='#10B981', fc='#FFFFFF', lw=1)
    ax.add_patch(box_m1)
    ax.text(16, 47, "aift_mcp.py", ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')
    ax.text(16, 44, "Dissect Core Engine", ha='center', va='center', fontsize=7, color='#047857')
    ax.text(16, 41.5, "E01, RAW, VMDK, VHD", ha='center', va='center', fontsize=6.5, color='#64748B')

    box_m2 = patches.FancyBboxPatch((28.5, 40), 20, 10, boxstyle="round,pad=0.5", ec='#10B981', fc='#FFFFFF', lw=1)
    ax.add_patch(box_m2)
    ax.text(38.5, 47, "eztools_mcp.py", ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')
    ax.text(38.5, 44, "Zimmerman, PE & Linux", ha='center', va='center', fontsize=7, color='#047857')
    ax.text(38.5, 41.5, "Prefetch, Amcache, $MFT, Log", ha='center', va='center', fontsize=6.5, color='#64748B')

    box_m3 = patches.FancyBboxPatch((51, 40), 20, 10, boxstyle="round,pad=0.5", ec='#10B981', fc='#FFFFFF', lw=1)
    ax.add_patch(box_m3)
    ax.text(61, 47, "sysinternals_mcp.py", ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')
    ax.text(61, 44, "Sysinternals Suite", ha='center', va='center', fontsize=7, color='#047857')
    ax.text(61, 41.5, "Autoruns, Sigcheck, Handles", ha='center', va='center', fontsize=6.5, color='#64748B')

    box_m4 = patches.FancyBboxPatch((73.5, 40), 22.5, 10, boxstyle="round,pad=0.5", ec='#10B981', fc='#FFFFFF', lw=1)
    ax.add_patch(box_m4)
    ax.text(84.7, 47, "network_memory_mcp.py", ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')
    ax.text(84.7, 44, "Volatility 3, TShark & AD1", ha='center', va='center', fontsize=7, color='#047857')
    ax.text(84.7, 41.5, "RAM Malfind, PCAP, ad1_extract", ha='center', va='center', fontsize=6.5, color='#64748B')

    # Tier 4: Execution & Storage Layer
    rect4 = patches.FancyBboxPatch((4, 18), 92, 16, boxstyle="round,pad=0.8", ec=c_tier_border[4], fc='#FFFBEB', lw=1.5)
    ax.add_patch(rect4)
    ax.text(6, 31.5, "TẦNG 4: CÁC BỘ NHỊ PHÂN THỰC THI CHUYÊN SÂU & KHO BẰNG CHỨNG (Ổ E:\\)", fontsize=8.5, fontweight='bold', color='#92400E')

    box_e1 = patches.FancyBboxPatch((6, 20), 43, 10, boxstyle="round,pad=0.5", ec='#F59E0B', fc='#FFFFFF', lw=1)
    ax.add_patch(box_e1)
    ax.text(27.5, 27, "Cụm Công cụ Nhị phân Chuyên sâu (Forensic Tool\\)", ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')
    ax.text(27.5, 24, "Get-ZimmermanTools (.NET 8/9) • SysinternalsSuite (C/C++)", ha='center', va='center', fontsize=7, color='#B45309')
    ax.text(27.5, 21.5, "Volatility 3.exe • MemProcFS vmm.dll • Wireshark tshark.exe", ha='center', va='center', fontsize=6.5, color='#64748B')

    box_e2 = patches.FancyBboxPatch((53, 20), 43, 10, boxstyle="round,pad=0.5", ec='#F59E0B', fc='#FFFFFF', lw=1)
    ax.add_patch(box_e2)
    ax.text(74.5, 27, "Kho Bằng chứng Trung tâm (E:\\Hunting-Forensics\\Evidence)", ha='center', va='center', fontsize=8, fontweight='bold', color='#0F172A')
    ax.text(74.5, 24, "Container Logic (.ad1, .txt) • Ảnh đĩa (.E01, .raw) • RAM (.dmp)", ha='center', va='center', fontsize=7, color='#B45309')
    ax.text(74.5, 21.5, "Gói tin (.pcap) • Thư mục giải nén extracted\\ (1.831 files)", ha='center', va='center', fontsize=6.5, color='#64748B')

    # Security Footnote
    rect_note = patches.FancyBboxPatch((4, 4), 92, 10, boxstyle="round,pad=0.5", ec='#CBD5E1', fc='#F1F5F9', lw=1)
    ax.add_patch(rect_note)
    ax.text(50, 11, "TIÊU CHUẨN AN TOÀN VÀ PHÁP CHỨNG (ISO/IEC 27037 & NIST SP 800-86 COMPLIANCE)", ha='center', va='center', fontsize=8, fontweight='bold', color='#334155')
    ax.text(50, 7, "• 100% On-Premise nội bộ: Không rò rỉ dữ liệu nhạy cảm ra ngoài • Băm 3 mã MD5, SHA-1, SHA-256 đối soát metadata gốc\n• Mọi tương tác đều ghi nhật ký Telemetry Event Stream thời gian thực • VETO Safety Rails chặn cứng lệnh shell thô sơ", ha='center', va='center', fontsize=7, color='#475569')

    # Arrows between tiers
    ax.annotate('', xy=(19.5, 76), xytext=(19.5, 70), arrowprops=dict(arrowstyle="->", color="#3B82F6", lw=1.5))
    ax.annotate('', xy=(50, 54), xytext=(50, 78), arrowprops=dict(arrowstyle="<-", color="#0284C7", lw=1.5, ls="--"))
    ax.text(51.5, 56, "Live Telemetry Webhook POST", fontsize=6.5, fontweight='bold', color='#0284C7')
    ax.annotate('', xy=(19.5, 58), xytext=(19.5, 52), arrowprops=dict(arrowstyle="->", color="#8B5CF6", lw=1.5))
    ax.annotate('', xy=(27.5, 38), xytext=(27.5, 32), arrowprops=dict(arrowstyle="->", color="#10B981", lw=1.5))
    ax.annotate('', xy=(74.5, 38), xytext=(74.5, 32), arrowprops=dict(arrowstyle="->", color="#10B981", lw=1.5))

    p1 = out_dir / "infra_architecture.png"
    plt.tight_layout()
    plt.savefig(str(p1), dpi=300)
    plt.close()
    print(f"Diagram 1 saved to {p1}")

    # -------------------------------------------------------------
    # DIAGRAM 2: SƠ ĐỒ HOẠT ĐỘNG & WORKFLOW ĐIỀU TRA TOÀN TRÌNH (INVESTIGATION WORKFLOW)
    # -------------------------------------------------------------
    fig, ax = plt.subplots(figsize=(12, 8.5), dpi=300)
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Title
    ax.text(50, 97, "SƠ ĐỒ QUY TRÌNH ĐIỀU TRA TOÀN TRÌNH THEO GIẢ THUYẾT (HYPOTHESIS-DRIVEN WORKFLOW)", 
            ha='center', va='center', fontsize=12.5, fontweight='bold', color='#0F172A')
    ax.text(50, 94, "Quy chuẩn 5 Giai đoạn Tự hành: Tiếp nhận ➔ Bóc tách ➔ Suy luận chuyên sâu ➔ Thẩm định VETO ➔ Báo cáo & Trực quan hóa", 
            ha='center', va='center', fontsize=8.5, fontstyle='italic', color='#475569')

    phases = [
        ("GIAI ĐOẠN 1: TIẾP NHẬN & XÁC MINH TOÀN VẸN (ISO/IEC 27037)", 
         "verify_evidence_integrity", 
         "1. Tiếp nhận mẫu bằng chứng (.ad1, .E01, .raw, .pcap)\n2. Tính đồng thời 3 mã băm MD5, SHA-1, SHA-256\n3. Đọc companion metadata (.txt) đối soát hash gốc\n4. Niêm phong chuỗi hành trình Chain of Custody",
         78, '#EFF6FF', '#3B82F6', '#1E40AF'),
        
        ("GIAI ĐOẠN 2: BÓC TÁCH CONTAINER & GIẢI MÃ CẤU TRÚC ĐĨA", 
         "ad1_extract & ad1_list", 
         "1. Nhận diện Magic Bytes: ADSEGMENTEDFILE (.ad1)\n2. Bóc tách cây thư mục logic ra đĩa vật lý (extracted/)\n3. Đếm số lượng files (ví dụ: 1.831 tệp tin FirstHack)\n4. Lập danh mục inventory tệp phục vụ điều tra sâu",
         60, '#F0FDF4', '#10B981', '#065F46'),

        ("GIAI ĐOẠN 3: SUY LUẬN THEO GIẢ THUYẾT & MỔ XẺ CHUYÊN SÂU (SANS FOR508)", 
         "Cụm 40+ FastMCP Tools", 
         "• Evidence of Execution: parse_prefetch, parse_amcache, parse_shimcache\n• Persistence Triage: autoruns_triage, sigcheck_file, evtx_logon\n• File System & Timelines: parse_mft (Timestomping), parse_shellbags, parse_srum\n• Linux & Memory: analyze_linux_logs (auth.log/bash_history), volatility_malfind",
         42, '#FAF5FF', '#8B5CF6', '#6B21A8'),

        ("GIAI ĐOẠN 4: CỔNG THẨM ĐỊNH ĐỐI NGHỊCH VETO LOOP (CHỐNG ẢO GIÁC)", 
         "Dual-Evidence Rule", 
         "1. Kiểm tra Bẫy nghi binh (Red Herring) từ attacker\n2. Áp dụng quy tắc đối chứng kép: Bắt buộc tối thiểu 2 nguồn chứng cứ độc lập\n3. Đánh giá độ tin cậy chứng cứ (>95%) trước khi kết luận\n4. Chặn đứng các suy diễn chủ quan không có bằng chứng số",
         24, '#FEF2F2', '#EF4444', '#991B1B'),

        ("GIAI ĐOẠN 5: XUẤT BÁO CÁO PHÁP CHỨNG & TRỰC QUAN HÓA (VISUALIZATION)", 
         "forensic-reporting & GUI", 
         "1. Xuất báo cáo DFIR chuẩn 8 phần (ISO 27037 & NIST SP 800-86)\n2. Bảng ánh xạ MITRE ATT&CK Kill Chain (T1078, T1548, T1059,...)\n3. Danh mục chỉ số xâm hại IOCs (Hashes, IPs, Domains, Scripts)\n4. ForBrain GUI (:5000) hiển thị Live Telemetry, Cây tiến trình, Timeline",
         6, '#FFFBEB', '#F59E0B', '#92400E')
    ]

    for title, tool_badge, desc, y_pos, bg_col, border_col, text_col in phases:
        rect = patches.FancyBboxPatch((5, y_pos), 90, 14, boxstyle="round,pad=0.6", ec=border_col, fc=bg_col, lw=1.5)
        ax.add_patch(rect)
        
        ax.text(7, y_pos + 10.5, title, fontsize=8.5, fontweight='bold', color=text_col)
        
        badge = patches.FancyBboxPatch((72, y_pos + 9.5), 21, 3.5, boxstyle="round,pad=0.3", ec=border_col, fc='#FFFFFF', lw=1)
        ax.add_patch(badge)
        ax.text(82.5, y_pos + 11.2, f"Tool: {tool_badge}", ha='center', va='center', fontsize=7, fontweight='bold', color=border_col)

        ax.text(7, y_pos + 5, desc, fontsize=7.2, color='#1E293B', va='center', linespacing=1.3)

    # Workflow arrows
    for y_arr in [78, 60, 42, 24]:
        ax.annotate('', xy=(50, y_arr - 2), xytext=(50, y_arr), 
                    arrowprops=dict(arrowstyle="->", color="#0F172A", lw=2))

    p2 = out_dir / "workflow_investigation.png"
    plt.tight_layout()
    plt.savefig(str(p2), dpi=300)
    plt.close()
    print(f"Diagram 2 saved to {p2}")

    return p1, p2

if __name__ == "__main__":
    generate_diagrams()
