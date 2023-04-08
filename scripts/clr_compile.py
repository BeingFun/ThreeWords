import os
import shutil
from constants.constants import ROOT_PATH
from src.util.file_tools import FileTools


CUR_PATH = os.path.dirname(os.path.abspath(__file__))

build_path = CUR_PATH + r'\threewords_build'
spec_path = CUR_PATH + r'\ThreeWords.spec'
bin_path = ROOT_PATH + r'\bin'
temp_path = ROOT_PATH + r'\temp'
logs_path = ROOT_PATH + r'\logs'
files_list = [build_path, spec_path,
              bin_path, temp_path, logs_path]

for path in files_list:
    FileTools.delete_file_or_folder(path)


# 遍历当前目录及其子目录
for root, dirs, files in os.walk(ROOT_PATH):
    # 检查是否存在 __pycache__ 文件夹
    if "__pycache__" in dirs:
        # 删除 __pycache__ 文件夹
        pycache_dir = os.path.join(root, "__pycache__")
        print(f"Removing {pycache_dir}")
        shutil.rmtree(pycache_dir)
