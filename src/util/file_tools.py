import json
import shutil
import os

from src.constants.constants import Constants


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

    # 安全创建文件夹
    @staticmethod
    def make_folder_s(folder):
        if os.path.exists(folder):
            shutil.rmtree(folder)
        os.mkdir(folder)

    # 清空文件夹
    @staticmethod
    def empty_folder_s(folder_path):
        file_path = None
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            shutil.rmtree(file_path)
        except FileNotFoundError:
            print(f"文件夹 {folder_path} 不存在！")

    @staticmethod
    def dump_config(parent_key: str, key: str, value):
        config_path = Constants.ROOT_PATH + r"\config\config.json"
        with open(config_path, "r", encoding="utf-8") as load_file:
            config_dict = json.load(load_file)
        config_dict[parent_key][key] = str(value)
        with open(config_path, "w", encoding="utf-8") as dump_file:
            json.dump(config_dict, dump_file, ensure_ascii=False)
