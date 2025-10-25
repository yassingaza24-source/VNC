rem 1) Sauvegarde (copie avant tout)
copy /Y "E:\Windows\System32\config\SOFTWARE" "E:\backup\SOFTWARE.bak"

rem 2) Charger la ruche SOFTWARE dans HKLM\OFF_SOFTWARE
reg load HKLM\OFF_SOFTWARE "E:\Windows\System32\config\SOFTWARE"

rem 3) Créer/écrire les valeurs (remplace USER / PASS / PCNAME)
reg add "HKLM\OFF_SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon /t REG_SZ /d 1 /f
reg add "HKLM\OFF_SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUserName /t REG_SZ /d "<USER>" /f
reg add "HKLM\OFF_SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword /t REG_SZ /d "<PASS>" /f
reg add "HKLM\OFF_SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultDomainName /t REG_SZ /d "<PCNAME>" /f

rem (optionnel)
reg add "HKLM\OFF_SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v ForceAutoLogon /t REG_SZ /d 1 /f

rem 4) Décharger la ruche
reg unload HKLM\OFF_SOFTWARE
