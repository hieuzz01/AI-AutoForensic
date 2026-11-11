@echo off
setlocal
title V-AutoFor - 1-Click Restore Configs & Models
echo ===================================================================
echo     V-AutoFor - Restore All Configs, MCP & LLM to Drive C
echo ===================================================================
echo.
set "BACKUP_DIR=%~dp0"
set "REASONIX_TARGET=%APPDATA%\reasonix"
set "ROUTER_TARGET=%APPDATA%\9router"
set "NPM_TARGET=%APPDATA%\npm"
set "WORK_SKILLS=E:\Hunting-Forensics\.reasonix\skills"

echo [*] Restoring Reasonix Global Configs (config.toml, .env, models)...
if not exist "%REASONIX_TARGET%" mkdir "%REASONIX_TARGET%"
xcopy /E /I /Y /Q "%BACKUP_DIR%reasonix_global_AppData\*" "%REASONIX_TARGET%\"

echo [*] Restoring 9Router Database & LLM Engine Models...
if not exist "%ROUTER_TARGET%" mkdir "%ROUTER_TARGET%"
xcopy /E /I /Y /Q "%BACKUP_DIR%9router_global_AppData\*" "%ROUTER_TARGET%\"

echo [*] Restoring NPM Global CLI Commands (v-autofor, v-autofor-stop)...
if not exist "%NPM_TARGET%" mkdir "%NPM_TARGET%"
xcopy /E /I /Y /Q "%BACKUP_DIR%npm_global_scripts\*" "%NPM_TARGET%\"

echo [*] Restoring Workspace Forensic Skills (Knowledge Base)...
if not exist "%WORK_SKILLS%" mkdir "%WORK_SKILLS%"
xcopy /E /I /Y /Q "%BACKUP_DIR%skills\*" "%WORK_SKILLS%\"

echo.
echo ===================================================================
echo  [+] RESTORE THANH CONG! TOAN BO MCP, LLM ENGINE DA SAN SANG!
echo ===================================================================
pause
