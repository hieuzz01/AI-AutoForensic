================================================================================
HUONG DAN SU DUNG BACKUP & RESTORE CAU HINH V-AUTOFOR & 9ROUTER
================================================================================

1. NGUYEN TAC LUU TRU TREN DRIVE C:
   - Reasonix Global Config:  %APPDATA%\reasonix\ (config.toml, .env, provider-keys.json)
   - 9Router Engine & DB:    %APPDATA%\9router\  (db\data.sqlite, model-catalog.json)
   - Global CLI Commands:     %APPDATA%\npm\      (v-autofor.cmd, v-autofor-stop.cmd)
   - Knowledge Base Skills:   E:\Hunting-Forensics\.reasonix\skills\

2. CACH RESTORE SANG MAY MOI (1-CLICK KHONG CAN CONFIG LAI):
   - Khi mang bo thu muc nay sang may moi hoac muon khoi phuc toan bo ve o C:
     Chi can CLICK DUP chuot vao file:
     👉 restore_all_configs_to_drive_C.cmd

   - Script se tu dong copy toan bo:
     [+] 4 MCP Servers (ForBrain AIFT, Eric Zimmerman, Sysinternals, Network/Memory)
     [+] Danh sach LLM Models & API Keys cua 9Router (data.sqlite)
     [+] Cac lenh chay toan cuc v-autofor, v-autofor-stop
     [+] 2 bo Skills chuyen gia dieu tra Forensic vao dung cho tren o C.

3. GOI ZIP DI DONG:
   - File V-AutoFor-Deploy-Kit.zip da chua tron ven bo snapshot tren va file restore.
   - Chi can giai nen va click "restore_all_configs_to_drive_C.cmd" la xong ngay lap tuc!
================================================================================
