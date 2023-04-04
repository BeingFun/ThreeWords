import shutil
import os


def delete_file_or_folder(path):
    """
    删除文件或文件夹
    :param path: 文件或文件夹路径
    """
    if os.path.exists(path):
        if os.path.isfile(path):
            # 如果是文件，则直接删除
            os.remove(path)
            print(f"已删除文件：{path}")
        elif os.path.isdir(path):
            # 如果是文件夹，则递归删除其中所有内容后再删除文件夹本身
            if not os.listdir(path):
                # 如果文件夹为空，则直接删除
                os.rmdir(path)
                print(f"已删除空文件夹：{path}")
            else:
                # 如果文件夹不为空，则递归删除其中所有内容后再删除文件夹本身
                shutil.rmtree(path)
                print(f"已删除文件夹及其内容：{path}")
    else:
        print(f"已删除文件夹及其内容：{path}")