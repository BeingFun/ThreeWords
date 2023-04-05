import os
import shutil
import zipfile
from src.util.file_tool import FileTool
from constants.constants import ROOT_PATH


if __name__ == '__main__':
    # 创建package_folder
    package_folder = "ThreeWords"
    need_copy_folder = ['bin', 'config', 'js',
                        "nodejs", 'resources']
    need_copy_file = ['README.md', 'changelog.md']
    new_folder = ['temp', 'logs', 'images']
    need_clean_folder = [package_folder, 'temp', 'logs']

    # 切换到根目录
    os.chdir(ROOT_PATH)
    # 检查文件夹是否存在
    for folder in need_clean_folder:
        FileTool.delete_file_or_folder(folder)
        os.mkdir(folder)

    # TODO 需要检查need_copy_file need_copy_folder 文件文件夹是否存在
    # 将bin、config文件夹中所有内容拷贝到threewords中
    for folder in need_copy_folder:
        src = os.path.join('.', folder)
        dst = os.path.join(package_folder, folder)
        shutil.copytree(src, dst)

    for folder in new_folder:
        src = os.path.join('.', folder)
        dst = os.path.join(package_folder, folder)
        shutil.copytree(src, dst)

    # 将 Threewords 文件夹压缩为 Threewords.zip
    with zipfile.ZipFile(package_folder + '.zip', 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # 遍历文件夹中的所有文件和子文件夹
        for root, dirs, files in os.walk(package_folder):
            for file in files:
                # 构造文件的完整路径
                file_path = os.path.join(root, file)
                # 将文件添加到 ZIP 文件中
                zip_file.write(file_path)

    # zipfile模块打包会忽略空文件，单独打包
    with zipfile.ZipFile(package_folder + '.zip', 'a', zipfile.ZIP_DEFLATED) as zip_file:
        for folder in new_folder:
            if folder == "images":
                zip_file.write(package_folder + r'/' + folder + '/' + 'new_images/')
            else:
                zip_file.write(package_folder + r'/' + folder + '/')

    # 打包完成之后清理文件夹
    shutil.rmtree(package_folder)
