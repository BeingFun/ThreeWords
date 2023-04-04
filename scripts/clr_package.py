import os

CUR_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(CUR_PATH)

zip_file = ROOT_PATH + r'\ThreeWords.zip'
if os.path.isfile(zip_file):
    # 如果是文件，则直接删除
    os.remove(zip_file)
    print(f"已删除文件：{zip_file}")

