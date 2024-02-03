import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common.config import Config
from src.util.file_tools import FileTools
from clr_running import clr_pycache

print("#" * 60)
print("start clr deploy...")
zip_file = Config.ROOT_PATH + r"\ThreeWords.zip"
FileTools.remove_s(zip_file)
clr_pycache(Config.ROOT_PATH)

# 删除用户依赖的文件
FileTools.delete_file_or_folder(Config.CONFIG_PATH + "font_dict.json")
FileTools.delete_file_or_folder(Config.CONFIG_PATH + "window_config.json")

print("finish clr deploy...")
print("#" * 60)
