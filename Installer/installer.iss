﻿; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "Maid Fiddler"
#define MyAppVersion "1.0.0.0-pre3"
#define MyAppURL "https://github.com/denikson/COM3D2.MaidFiddler"
#define MyAppExeName "maid_fiddler_qt.exe"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{B1019C7B-E19F-4584-B2A1-3EB7B5FD5874}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={userpf}\MaidFiddlerGUI
DefaultGroupName={#MyAppName}
InfoBeforeFile=README.txt
OutputBaseFilename=MaidFiddlerSetup
Compression=lzma2/ultra64
SolidCompression=yes
ArchitecturesAllowed=x64
ArchitecturesInstallIn64BitMode=x64
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[Files]
Source: "bin\app\maid_fiddler_qt.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "bin\app\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "bin\plugin\*"; DestDir: "{code:GetInstallLocation}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Code]
var
  HelperDirPage: TInputDirWizardPage;

procedure InitializeWizard;
var 
  COM3D2Location : String;
begin
  HelperDirPage := CreateInputDirPage(wpSelectDir, 
   'Select COM3D2 directory',
   'Where is COM3D2 located?',
   'Please give the location of COM3D2 (NOT SYBARIS):', False, '');
   HelperDirPage.Add('');

   if RegQueryStringValue(HKEY_CURRENT_USER, 'Software\KISS\カスタムオーダーメイド3D2', 'InstallPath', COM3D2Location) then
   begin
     HelperDirPage.Values[0] := COM3D2Location;
   end; 
end;

function NextButtonClick(CurPageID: Integer) : Boolean;
begin
  if (CurPageID = HelperDirPage.ID) and (not DirExists(HelperDirPage.Values[0] + '\Sybaris')) then
  begin
    MsgBox('No Sybaris folder found in the given COM3D2 directory!'#13#10'Check that you have Sybaris 2 installed in the given directory.', mbError, MB_OK);
    Result := False;
  end
  else
    Result := True;
end;

function GetInstallLocation(Param : String) : String;
begin
  Result := HelperDirPage.Values[0]
end;