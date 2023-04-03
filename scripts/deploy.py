import os
import shutil
import zipfile


CUR_PATH = os.path.dirname(os.path.abspath(__file__))
ROOT_PATH = os.path.dirname(CUR_PATH)

if __name__ == '__main__':
    folder_name = "ThreeWords"
    os.chdir(ROOT_PATH)
    # 检查文件夹是否存在
    if os.path.exists(folder_name):
        # 如果文件夹存在，则删除其中所有文件和子文件夹
        for root, dirs, files in os.walk(folder_name, topdown=False):
            for file in files:
                file_path = os.path.join(root, file)
                os.remove(file_path)
            for dir in dirs:
                dir_path = os.path.join(root, dir)
                os.rmdir(dir_path)
    else:
        # 如果文件夹不存在，则创建它
        os.mkdir(folder_name)

    need_copy_folder = ['bin', 'config', 'js', 'logs',
                        "nodejs", 'resources', 'temp', 'images']
    need_copy_file = ['README.md', 'changelog.md']
    # 将bin、config文件夹中所有内容拷贝到threewords中
    for folder in need_copy_folder:
        src = os.path.join('.', folder)
        dst = os.path.join(folder_name, folder)
        shutil.copytree(src, dst)

    for file in need_copy_file:
        shutil.copy(file, folder_name)

    # 将 Threewords 文件夹压缩为 Threewords.zip
    with zipfile.ZipFile(folder_name + '.zip', 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # 遍历文件夹中的所有文件和子文件夹
        for root, dirs, files in os.walk(folder_name):
            for file in files:
                # 构造文件的完整路径
                file_path = os.path.join(root, file)
                # 将文件添加到 ZIP 文件中
                zip_file.write(file_path)
