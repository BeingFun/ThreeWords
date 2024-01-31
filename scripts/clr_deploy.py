import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.constants.constants import Constants
from src.util.file_tools import FileTools
from clr_running import clr_pycache

print("#" * 60)
print("start clr deploy...")
zip_file = Constants.ROOT_PATH + r"\ThreeWords.zip"
FileTools.remove_s(zip_file)

clr_pycache(Constants.ROOT_PATH)

print("finish clr deploy...")
print("#" * 60)
