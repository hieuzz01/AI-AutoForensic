@echo off
setlocal
title V-AutoFor - Configure SMB Network Shares for Remote Triage
echo ===================================================================
echo     V-AUTOFOR - SETUP NETWORK SHARES CHO REMOTE TRIAGE
echo ===================================================================
echo.
echo Script nay can quyen Administrator de tao thu muc chia se SMB tren mang.
echo.

:: 1. Share thu muc Tools (Read-Only)
echo [*] Dang chia se thu muc Tools: E:\Hunting-Forensics\Network-Share-Triage as [ForensicTools]...
net share ForensicTools /delete >nul 2>&1
net share ForensicTools="E:\Hunting-Forensics\Network-Share-Triage" /GRANT:Everyone,READ /REMARK:"V-AutoFor Portable Triage Tools (Read-Only)"

:: 2. Share thu muc Evidence (Writeable de may nan nhan day du lieu ve)
echo [*] Dang chia se thu muc Evidence: E:\Hunting-Forensics\Evidence as [Evidence]...
net share Evidence /delete >nul 2>&1
net share Evidence="E:\Hunting-Forensics\Evidence" /GRANT:Everyone,CHANGE /REMARK:"V-AutoFor Evidence Dropzone (Writeable)"

:: 3. Lay dia chi IP hien tai
for /f "tokens=4" %%a in ('route print ^| findstr 0.0.0.0 ^| findstr /v "0.0.0.0.*0.0.0.0"') do (
    set "MY_IP=%%a"
)

echo.
echo ===================================================================
echo  [+] CAU HINH CHIA SE MANG THANH CONG!
echo ===================================================================
echo  1. Thu muc Tools (Chi doc):     \\%MY_IP%\ForensicTools
echo  2. Thu muc Evidence (Ghi file): \\%MY_IP%\Evidence
echo.
echo  LENH KICH HOAT THU THAP TREN MAY NAN NHAN (Chay qua CMD/WinRM):
echo  "\\%MY_IP%\ForensicTools\Scripts\Run_Full_Triage_Remote.bat \\%MY_IP%"
echo ===================================================================
pause
