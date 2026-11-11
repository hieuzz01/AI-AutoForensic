@echo off
setlocal
echo ===================================================================
echo             STOPPING ALL V-AUTOFOR ^& FORBRAIN SERVICES
echo ===================================================================

:: 1. Dung cac tien trinh dang mo Listening Port 8787 va 5000
powershell -NoProfile -Command "Get-NetTCPConnection -LocalPort 8787, 5000 -ErrorAction SilentlyContinue | Select-Object -ExpandProperty OwningProcess -Unique | ForEach-Object { Write-Host '  [-] Dung process dang chiem port:' $_; Stop-Process -Id $_ -Force -ErrorAction SilentlyContinue }"

:: 2. Quet va dung bat ky tien trinh aift.py hoac reasonix nao con sot lai trong bo nho
powershell -NoProfile -Command "Get-CimInstance Win32_Process -ErrorAction SilentlyContinue | Where-Object { $_.CommandLine -like '*aift.py*' -or $_.Name -eq 'reasonix.exe' } | ForEach-Object { Write-Host '  [-] Dung tien trinh:' $_.ProcessId '(' $_.Name ')'; Stop-Process -Id $_.ProcessId -Force -ErrorAction SilentlyContinue }"

taskkill /F /IM reasonix.exe >nul 2>&1

echo.
echo   [+] DA DUNG TOAN BO CAC DICH VU (Port 8787 ^& Port 5000) HOAN TOAN SACH SE!
echo ===================================================================
