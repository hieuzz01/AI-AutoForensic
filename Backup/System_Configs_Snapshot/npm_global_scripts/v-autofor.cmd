@echo off
setlocal
title V-AutoFor - AI Digital Forensics Platform
echo ===================================================================
echo             V-AutoFor - AI DIGITAL FORENSICS PLATFORM
echo ===================================================================
echo   [1] V-AutoFor AI Chat (Dieu tra ^& Prompt):
echo       - May tai cho:        http://localhost:8787/#token=forensic
echo       - May trong mang LAN:  http://10.1.20.80:8787/#token=forensic
echo.
echo   [2] ForBrain Web Portal (Upload Evidence ^& Theo doi Processing):
echo       - May tai cho:        http://localhost:5000
echo       - May trong mang LAN:  http://10.1.20.80:5000
echo.
echo   [*] Thu muc Evidence:     E:\Hunting-Forensics\Evidence
echo   [*] MCP Tools:            ForBrain (AIFT), Eric Zimmerman, Sysinternals
echo   [*] AI Gateway:           9Router (127.0.0.1:20128)
echo ===================================================================
echo   Dang khoi dong song song ca 2 dich vu...
echo.

:: Khoi dong ForBrain Portal tren cong 5000 (chay ngam)
start /b "" "E:\Hunting-Forensics\Forensic Tool\Forensic AI\AIFT\.venv\Scripts\python.exe" "E:\Hunting-Forensics\Forensic Tool\Forensic AI\AIFT\aift.py"

:: Khoi dong V-AutoFor Web Server tren cong 8787
reasonix serve --page "C:\Users\Acer\AppData\Roaming\reasonix\web" --addr 0.0.0.0:8787 --dir "E:\Hunting-Forensics" --preset balanced --auth token --token forensic %*
