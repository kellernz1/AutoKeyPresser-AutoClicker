Option Explicit

Dim shell, fileSystem, scriptFolder, pythonScript, command

Set shell = CreateObject("WScript.Shell")
Set fileSystem = CreateObject("Scripting.FileSystemObject")

scriptFolder = fileSystem.GetParentFolderName(WScript.ScriptFullName)
pythonScript = fileSystem.BuildPath(scriptFolder, "tecla_automatica.py")
command = "pyw.exe """ & pythonScript & """"

shell.CurrentDirectory = scriptFolder
shell.Run command, 0, False
