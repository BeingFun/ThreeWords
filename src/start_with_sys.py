import winreg
from constants.constants import ROOT_PATH


# 设置要添加到注册表中的键值对
def start_with_sys():
    start_path = ROOT_PATH + r'\bin\ThreeWords.exe'
    start_path = r'"{}"'.format(start_path) + r' --hidden'
    key = winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                         r'SOFTWARE\Microsoft\Windows\CurrentVersion\Run', 0, winreg.KEY_ALL_ACCESS)
    winreg.SetValueEx(key, "ThreeWords", 0, winreg.REG_SZ, start_path)
    winreg.CloseKey(key)
