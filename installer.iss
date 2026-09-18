[Setup]
AppId={{E0AF4A56-77CE-4C6E-88E7-2F52D7E7D3A1}
AppName=MessengerDesk
AppVersion=0.2.0
AppPublisher=MessengerDesk
DefaultDirName={autopf}\MessengerDesk
DefaultGroupName=MessengerDesk
OutputDir=installer
OutputBaseFilename=MessengerDesk-Setup
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=lowest
SetupIconFile=

[Files]
Source: "dist\MessengerDesk\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\MessengerDesk"; Filename: "{app}\MessengerDesk.exe"
Name: "{autodesktop}\MessengerDesk"; Filename: "{app}\MessengerDesk.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "ایجاد میانبر روی دسکتاپ"; GroupDescription: "میانبرها:"; Flags: unchecked

[Run]
Filename: "{app}\MessengerDesk.exe"; Description: "اجرای MessengerDesk"; Flags: nowait postinstall skipifsilent
