import shutil
import os


class FileTools:
    # 安全删除文件
    @staticmethod
    def remove_s(file):
        if os.path.exists(file):
            os.remove(file)

    # 安全删除文件夹
    @staticmethod
    def rmdir_s(path):
        if not os.listdir(path):
            os.rmdir(path)
        else:
            shutil.rmtree(path)

    # 安全删除文件或文件夹
    @staticmethod
    def delete_file_or_folder(path):
        if os.path.exists(path):
            if os.path.isfile(path):
                # 如果是文件，则直接删除
                os.remove(path)
            elif os.path.isdir(path):
                FileTools.rmdir_s(path)

    # 安全创建文件
    @staticmethod
    def make_file_s(file):
        FileTools.remove_s(file)
        if not os.path.exists((os.path.dirname(file))):
            os.mkdir(os.path.dirname(file))
        open(file, "x").close()
