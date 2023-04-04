
import os
import sys

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(CUR_PATH)

sys.path.append(ROOT_PATH + r'/src/util')
from file_tool import delete_file_or_folder

build_path = CUR_PATH + r'\threewords_build'
spec_path = CUR_PATH + r'\ThreeWords.spec'
bin_path = ROOT_PATH + r'\bin'
temp_path = ROOT_PATH + r'\temp'
logs_path = ROOT_PATH + r'\logs'
files_list = [build_path, spec_path,
              bin_path, temp_path, logs_path]

for path in files_list:
    delete_file_or_folder(path)
