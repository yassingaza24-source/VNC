copy /Y "E:\Windows\System32\config\SOFTWARE" "E:\backup\SOFTWARE.bak"
copy /Y "E:\Windows\System32\config\SYSTEM" "E:\backup\SYSTEM.bak"

reg load HKLM\OFF_SOFTWARE "E:\Windows\System32\config\SOFTWARE"
reg load HKLM\OFF_SYSTEM "E:\Windows\System32\config\SYSTEM"

reg add "HKLM\OFF_SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v AutoAdminLogon /t REG_SZ /d 1 /f
reg add "HKLM\OFF_SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultUserName /t REG_SZ /d "<USER>" /f
reg add "HKLM\OFF_SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultPassword /t REG_SZ /d "<PASS>" /f
reg add "HKLM\OFF_SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v DefaultDomainName /t REG_SZ /d "<PCNAME>" /f
reg add "HKLM\OFF_SOFTWARE\Microsoft\Windows NT\CurrentVersion\Winlogon" /v ForceAutoLogon /t REG_SZ /d 1 /f

reg add "HKLM\OFF_SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" /v EnableLUA /t REG_DWORD /d 0 /f

reg add "HKLM\OFF_SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\DomainProfile" /v EnableFirewall /t REG_DWORD /d 0 /f
reg add "HKLM\OFF_SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\PublicProfile" /v EnableFirewall /t REG_DWORD /d 0 /f
reg add "HKLM\OFF_SYSTEM\CurrentControlSet\Services\SharedAccess\Parameters\FirewallPolicy\StandardProfile" /v EnableFirewall /t REG_DWORD /d 0 /f

reg unload HKLM\OFF_SOFTWARE
reg unload HKLM\OFF_SYSTEM
