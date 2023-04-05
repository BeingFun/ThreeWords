import configparser
import chardet
import sys
import os

FROZEN = getattr(sys, 'frozen', False)

# 获取当前文件所在目录的路径
if FROZEN:
    # 如果是可执行文件，则用 compass 获取可执行文件的目录
    CUR_PATH = os.path.dirname(os.path.abspath(sys.executable))
else:
    # 否则，从 __file__ 中获取当前文件的路径，并取其所在目录作为当前目录
    CUR_PATH = os.path.dirname(os.path.abspath(__file__))

# 根目录
ROOT_PATH = os.path.dirname(CUR_PATH)


class ConfigInit:
    @staticmethod
    def config_init():
        # Read the configuration file information
        config = configparser.ConfigParser(allow_no_value=False)
        config.optionxform = lambda option: option
        # Read the content of the file and use the chardet module to detect the encoding format
        configfile = ROOT_PATH + "\\config\\config.ini"

        with open(configfile, 'rb') as file:
            content = file.read()
            encoding = chardet.detect(content)['encoding']

        # Reopen the file using the detected encoding format and read the content
        with open(configfile, encoding=encoding) as file:
            config.read_file(file)
        # custom_config = {}
        # for k, v in config.items():
        #     custom_config[k] = dict(v)
        # return custom_config
        return config

