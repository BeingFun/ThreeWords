import os
from constants.constants import Constants


new_image = Constants.ROOT_PATH + r'\images'
for filename in os.listdir(new_image):
    file_path = os.path.join(new_image, filename)
    try:
        if os.path.isfile(file_path):  # 如果是文件而不是文件夹
            os.remove(file_path)  # 删除文件
    except Exception as e:
        print(f"删除文件 {file_path} 时出错：{e}")
