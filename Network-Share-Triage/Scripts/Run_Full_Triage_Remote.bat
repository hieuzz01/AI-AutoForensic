@echo off
setlocal enabledelayedexpansion
title V-AutoFor - Remote Live Forensic Triage (RFC 3227 Order of Volatility)

::================================================================================
:: V-AUTOFOR REMOTE LIVE TRIAGE SCRIPT
:: Muc tieu: Thu thap toan ven chung cu truc tiep qua Network Share khong can cai dat
:: Thu tu bay mau (RFC 3227): RAM -> Network PCAP -> Live State -> Artifacts -> Hash
::================================================================================

:: Lay dia chi may chu chia se tu tham so hoac mac dinh IP may chu V-AutoFor
set "FORENSIC_SERVER=%~1"
if "%FORENSIC_SERVER%"=="" (
    set "FORENSIC_SERVER=\\10.1.20.80"
)

set "TOOLS_DIR=%FORENSIC_SERVER%\ForensicTools"
set "EVIDENCE_BASE=%FORENSIC_SERVER%\Evidence"
set "HOST_EVIDENCE=%EVIDENCE_BASE%\%COMPUTERNAME%_%DATE:~-4,4%%DATE:~-7,2%%DATE:~-10,2%"

echo ===================================================================
echo      V-AUTOFOR AGENTLESS REMOTE TRIAGE - HOST: %COMPUTERNAME%
echo ===================================================================
echo [*] May chu Forensic:  %FORENSIC_SERVER%
echo [*] Thu muc Tools:     %TOOLS_DIR%
echo [*] Thu muc Evidence:  %HOST_EVIDENCE%
echo.

:: Tao thu muc tren may chu luu tru chung cu
mkdir "%HOST_EVIDENCE%" 2>nul
mkdir "%HOST_EVIDENCE%\LiveState" 2>nul

echo [1/5] THU THAP BO NHO RAM (WinPmem Mini)...
if exist "%TOOLS_DIR%\1_RAM\winpmem_mini_x64.exe" (
    "%TOOLS_DIR%\1_RAM\winpmem_mini_x64.exe" -o "%HOST_EVIDENCE%\ram_dump.raw"
    echo   [+] RAM dump xong: %HOST_EVIDENCE%\ram_dump.raw
) else (
    echo   [-] Khong tim thay winpmem_mini_x64.exe, bo qua RAM dump.
)

echo.
echo [2/5] BAT LUU LUONG MANG TRUC TIEP (RawCap / Pktmon trong 30 giay)...
if exist "%TOOLS_DIR%\2_Network\RawCap.exe" (
    start "" /b "%TOOLS_DIR%\2_Network\RawCap.exe" 0 "%HOST_EVIDENCE%\network_capture.pcap"
    timeout /t 30 /nobreak >nul
    taskkill /F /IM RawCap.exe >nul 2>&1
    echo   [+] PCAP capture xong: %HOST_EVIDENCE%\network_capture.pcap
) else (
    echo   [*] Thu bat bang Windows Pktmon...
    pktmon start --etw -m real-time >nul 2>&1
    timeout /t 30 /nobreak >nul
    pktmon stop >nul 2>&1
    pktmon pcapng pktmon.etl -o "%HOST_EVIDENCE%\network_capture.pcapng" >nul 2>&1
    del /f /q pktmon.etl >nul 2>&1
    echo   [+] Pktmon capture xong.
)

echo.
echo [3/5] THU THAP TRANG THAI DANG CHAY (Live State & Persistence)...
"%TOOLS_DIR%\3_LiveState\tcpvcon64.exe" -a -c -n /accepteula > "%HOST_EVIDENCE%\LiveState\active_connections.csv" 2>nul
"%TOOLS_DIR%\3_LiveState\pslist64.exe" -t /accepteula > "%HOST_EVIDENCE%\LiveState\process_tree.txt" 2>nul
"%TOOLS_DIR%\3_LiveState\autorunsc64.exe" -a * -c /accepteula > "%HOST_EVIDENCE%\LiveState\persistence_autoruns.csv" 2>nul
"%TOOLS_DIR%\3_LiveState\handle64.exe" -a /accepteula > "%HOST_EVIDENCE%\LiveState\open_handles.txt" 2>nul
netstat -ano > "%HOST_EVIDENCE%\LiveState\netstat_raw.txt" 2>nul
ipconfig /all > "%HOST_EVIDENCE%\LiveState\ipconfig.txt" 2>nul
echo   [+] Live State da duoc luu tai: %HOST_EVIDENCE%\LiveState\

echo.
echo [4/5] BUNG TOAN BO ARTIFACTS HE THONG (CyLR: EventLog, Registry, MFT, Prefetch)...
if exist "%TOOLS_DIR%\4_Artifacts\CyLR.exe" (
    "%TOOLS_DIR%\4_Artifacts\CyLR.exe" -o "%HOST_EVIDENCE%" -u
    echo   [+] CyLR da hoan thanh trich xuat artifacts!
) else (
    echo   [-] Khong tim thay CyLR.exe!
)

echo.
echo [5/5] BAM TOAN VEN CHUNG CU SO (Chain of Custody SHA-256)...
echo Date acquired: %DATE% %TIME% > "%HOST_EVIDENCE%\Chain_of_Custody.txt"
echo Hostname: %COMPUTERNAME% >> "%HOST_EVIDENCE%\Chain_of_Custody.txt"
echo IP Configuration: >> "%HOST_EVIDENCE%\Chain_of_Custody.txt"
ipconfig | findstr /i "IPv4" >> "%HOST_EVIDENCE%\Chain_of_Custody.txt"
echo. >> "%HOST_EVIDENCE%\Chain_of_Custody.txt"
echo [SHA-256 HASHES] >> "%HOST_EVIDENCE%\Chain_of_Custody.txt"

powershell -NoProfile -Command "Get-ChildItem -Path '%HOST_EVIDENCE%' -File | ForEach-Object { $h = Get-FileHash -Path $_.FullName -Algorithm SHA256; Write-Host ('  ' + $_.Name + ' -> ' + $h.Hash); Add-Content -Path '%HOST_EVIDENCE%\Chain_of_Custody.txt' -Value ($_.Name + ' : ' + $h.Hash) }"

echo.
echo ===================================================================
echo  [+] HOAN THANH THU THAP CHUNG CU CHO V-AUTOFOR THANH CONG!
echo  Toan bo file da duoc day ve server tai: %HOST_EVIDENCE%
echo ===================================================================
