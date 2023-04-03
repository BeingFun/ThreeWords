Dim shell
Set shell = CreateObject("WScript.Shell")
shell.CurrentDirectory = "D:\ThreeWords\ThreeWords\bin"
shell.Run "ThreeWords.exe", 0, True