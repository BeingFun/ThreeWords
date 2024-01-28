import os
import shutil
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.constants.constants import Constants
from src.util.file_tools import FileTools

print("#" * 60)
print("start clr compile...")

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
build_path = CUR_PATH + r'\threewords_build'
spec_path = CUR_PATH + r'\ThreeWords.spec'
bin_path = Constants.ROOT_PATH + r'\bin'
logs_path = Constants.ROOT_PATH + r'\Error.log'
files_list = [build_path, spec_path,
              bin_path, logs_path]

for path in files_list:
    FileTools.delete_file_or_folder(path)
    print(f"Removing {path}")

# 遍历当前目录及其子目录
for root, dirs, files in os.walk(Constants.ROOT_PATH):
    # 检查是否存在 __pycache__ 文件夹
    if "__pycache__" in dirs:
        # 删除 __pycache__ 文件夹
        pycache_dir = os.path.join(root, "__pycache__")
        print(f"Removing {pycache_dir}")
        shutil.rmtree(pycache_dir)

print("finish clr compile...")
print("#" * 60)
