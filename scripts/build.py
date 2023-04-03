import sys
import os
from pathlib import Path
from PyInstaller.__main__ import run

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(CUR_PATH)

if __name__ == '__main__':
    threewords_path = ROOT_PATH + "\\src\\threewords.py"
    performable_path = ROOT_PATH + "\\bin"
    icon_file_path = ROOT_PATH + "\\resources\\threewords.ico"
    work_path = CUR_PATH + "\\threewords_build"
    print()
    # 设置编译参数和选项
    options = [
        '--onefile',  # 打包成单个可执行文件
        '--noconsole',  # 不显示控制台窗口
        '--clean',  # 清理临时文件
        '--name={}'.format("ThreeWords"),  # 指定生成的可执行文件名称
        '--distpath={}'.format(performable_path),  # 指定生成的可执行文件路径
        '--icon={}'.format(icon_file_path),  # 指定生成的可执行文件图标
        '--specpath={}'.format(CUR_PATH),  # 指定 .spec 文件的输出路径
        '--workpath={}'.format(work_path)  # 指定build 文件夹路径
    ]

    print(options)
    # 运行 PyInstaller
    try:
        run([
            str(threewords_path),
            *options,
        ])
    except Exception as e:
        print(e)
        sys.exit(1)
