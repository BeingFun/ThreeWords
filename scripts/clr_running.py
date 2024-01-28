import os
import shutil
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.constants.constants import Constants

image_path = Constants.ROOT_PATH + r'\images'

print("#" * 60)
print("start clr compile...")
for filename in os.listdir(image_path):
    file_path = os.path.join(image_path, filename)
    try:
        if filename == "bing images" or filename == "cur use":
            shutil.rmtree(file_path)
    except Exception as e:
        print(f"删除文件夹 {file_path} 时出错：{e}")

print("finish clr compile...")
print("#" * 60)
