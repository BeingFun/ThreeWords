import os
import sys

import shutil
import winshell
from constants.constants import Constants
from src.util.file_tools import FileTools
from src.util.func_tools import FuncTools


# 是否为可执行文件
FROZEN = getattr(sys, 'frozen', False)

# 获取当前文件所在目录的路径
if FROZEN:
    # 如果是可执行文件，则用 compass 获取可执行文件的目录
    CUR_PATH = os.path.dirname(os.path.abspath(sys.executable))
else:
    # 否则，从 __file__ 中获取当前文件的路径，并取其所在目录作为当前目录
    CUR_PATH = os.path.dirname(os.path.abspath(__file__))


@FuncTools.run_as_admin
def set_start_file():
    # Set the destination folder for the shortcut
    dst_folder = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup'
    dst_file = dst_folder + r'\ThreeWords.lnk'
    # 如果启动项已经存在则返回
    if os.path.exists(dst_file):
        return
    # Create a VBS script to run the ThreeWords program
    vbs_file = Constants.ROOT_PATH + r'\temp\StartThreeWords.vbs'
    FileTools.make_file_s(vbs_file)
    if Constants.FROZEN:
        vbs_run = "ThreeWords.exe"
    else:
        vbs_run = "python {} 2>null".format("ThreeWords.py")

    with open(vbs_file, "w") as f:
        f.write('Dim shell\n')
        f.write('Set shell = CreateObject("WScript.Shell")\n')
        f.write('shell.CurrentDirectory = "{}"\n'.format(CUR_PATH))
        f.write('shell.Run "{}", 0, True'.format(vbs_run))

    # Get the source file and shortcut path
    source_file = vbs_file
    shortcut_path = Constants.ROOT_PATH + r'\temp\StartThreeWords.lnk'
    ico_path = Constants.ROOT_PATH + r'\resources\ico\threewords.ico'
    # Create a shortcut for the VBS script
    winshell.CreateShortcut(
        Path=shortcut_path,
        Target=source_file,
        Icon=(ico_path, 0),
        Description='Three Words shortcut'
    )

    # Copy the shortcut to the destination folder
    shutil.copy(shortcut_path, dst_file)
