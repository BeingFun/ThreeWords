import sys
import os

from PyInstaller.__main__ import run
from src.constants.constants import Constants


CUR_PATH = os.path.dirname(os.path.abspath(__file__))

if __name__ == '__main__':
    version = "release"
    threewords_path = Constants.ROOT_PATH + r'\src\\main.py'
    performable_path = Constants.ROOT_PATH + r'\bin'
    icon_file_path = Constants.ROOT_PATH + r'\resources\\ico\\threewords.ico'
    work_path = CUR_PATH + r'\threewords_build'

    # 设置编译参数和选项
    options = [
        '--onefile',  # 打包成单个可执行文件
        # '--noconsole',  # 不显示控制台窗口
        '--clean',  # 清理临时文件
        '--name={}'.format("ThreeWords"),  # 指定生成的可执行文件名称
        '--distpath={}'.format(performable_path),  # 指定生成的可执行文件路径
        '--icon={}'.format(icon_file_path),  # 指定生成的可执行文件图标
        '--specpath={}'.format(CUR_PATH),  # 指定 .spec 文件的输出路径
        '--workpath={}'.format(work_path)  # 指定build 文件夹路径
    ]

    if "release" == version:
        options.append("--noconsole")  # 不显示控制台窗口

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
