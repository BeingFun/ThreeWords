import os
from constants.constants import ROOT_PATH
from src.util.file_tool import FileTool


CUR_PATH = os.path.dirname(os.path.abspath(__file__))

build_path = CUR_PATH + r'\threewords_build'
spec_path = CUR_PATH + r'\ThreeWords.spec'
bin_path = ROOT_PATH + r'\bin'
temp_path = ROOT_PATH + r'\temp'
logs_path = ROOT_PATH + r'\logs'
files_list = [build_path, spec_path,
              bin_path, temp_path, logs_path]

for path in files_list:
    FileTool.delete_file_or_folder(path)
