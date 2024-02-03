import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.common.config import Config
from src.util.file_tools import FileTools
from clr_running import clr_pycache


print("#" * 60)
print("start clr compile...")

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
build_path = CUR_PATH + r'\threewords_build'
spec_path = CUR_PATH + r'\ThreeWords.spec'
bin_path = Config.ROOT_PATH + r'\bin'
logs_path = Config.ROOT_PATH + r'\Error.log'
files_list = [build_path, spec_path,
              bin_path, logs_path]

for path in files_list:
    FileTools.delete_file_or_folder(path)
    print(f"Removing {path}")

clr_pycache(Config.ROOT_PATH)

print("finish clr compile...")
print("#" * 60)
