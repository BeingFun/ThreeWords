import os
import shutil
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.constants.constants import Constants

image_path = Constants.ROOT_PATH + r'\images'

def clr_pycache(folder_path):
    # 遍历当前目录及其子目录
    for root, dirs, files in os.walk(folder_path):
        # 检查是否存在 __pycache__ 文件夹
        if "__pycache__" in dirs:
            # 删除 __pycache__ 文件夹
            pycache_dir = os.path.join(root, "__pycache__")
            print(f"Removing {pycache_dir}")
            shutil.rmtree(pycache_dir)


print("#" * 60)
print("start clr compile...")
for filename in os.listdir(image_path):
    file_path = os.path.join(image_path, filename)
    try:
        if filename == "bing images" or filename == "cur use":
            shutil.rmtree(file_path)
    except Exception as e:
        print(f"删除文件夹 {file_path} 时出错：{e}")

clr_pycache(Constants.ROOT_PATH)
print("finish clr compile...")
print("#" * 60)
