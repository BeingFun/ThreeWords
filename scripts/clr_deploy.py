import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.constants.constants import Constants
from src.util.file_tools import FileTools

print("#" * 60)
print("start clr deploy...")
zip_file = Constants.ROOT_PATH + r'\ThreeWords.zip'
FileTools.remove_s(zip_file)
print("finish clr deploy...")
print("#" * 60)
