import os
import sys
from collections import namedtuple

from src.config_init import ConfigInit

FROZEN = getattr(sys, 'frozen', False)

# 获取当前文件所在目录的路径
if FROZEN:
    # 如果是可执行文件，则用 compass 获取可执行文件的目录
    _CUR_PATH = os.path.dirname(os.path.abspath(sys.executable))
else:
    # 否则，从 __file__ 中获取当前文件的路径，并取其所在目录作为当前目录
    _CUR_PATH = os.path.dirname(os.path.abspath(__file__))

# 根目录
ROOT_PATH = os.path.dirname(_CUR_PATH)

# 文字风格 dict
_FONT_STYLE_MAP = {
    "动画": 'a',
    "漫画": 'b',
    "游戏": 'c',
    "文学": 'd',
    "原创": 'e',
    "来自网络": 'f',
    "其他": 'g',
    "影视": 'h',
    "诗词": 'i',
    "网易云": 'j',
    "哲学": 'k',
    "抖机灵": 'l'
}

# 域名
# _ 仅本文访问
_URL = 'https://v1.hitokoto.cn/'


class Constants:
    # 工程根目录
    ROOT_PATH = ROOT_PATH
    # 是否是 release 版本
    VERSION = "release"
    # 是否为可执行文件
    FROZEN = FROZEN
    # 默认背景
    DEFAULT_BACKGROUD = ROOT_PATH + r'\resources\default'
    # 添加文字后的图片位置
    NEW_IMAGES_PATH = ROOT_PATH + r'\images'
    # Set the system desktop background
    SPI_SETDESKWALLPAPER = 20
    # 网页请求配置
    # 设置请求头，模拟浏览器行为
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'application/json'}
    # 最大重试请求次数
    MAX_RETRIES = 3


class CustomConfig:
    # __ 私有变量
    __custom_config = ConfigInit.config_init()

    __BASIC_SETTING = namedtuple('BASIC_SETTING', ['START_WITH_SYSTEM', 'TEXT_UPDATE_INTERVAL'])
    __IMAGE_SETTING = namedtuple('IMAGE_SETTING', ['BACKGROUND_IMAGES_PATH'])
    __FONT_SETTING = namedtuple('FONT_SETTING', ['FONT_COLOR', 'FONT_SIZE', 'FONT_TYPE', 'TEXT_POSITION', 'FONT_STYLE'])

    # BASIC_SETTING
    __start_with_sys = __custom_config["BASIC_SETTING"].getboolean('START_WITH_SYSTEM')
    __text_update_interval = __custom_config["BASIC_SETTING"].getint('TEXT_UPDATE_INTERVAL')
    BASIC_SETTING = __BASIC_SETTING(__start_with_sys, __text_update_interval)

    # IMAGE_SETTING
    __image_path = __custom_config['IMAGE_SETTING'].get('BACKGROUND_IMAGES_PATH')
    if __image_path == 'Default':
        IMAGE_SETTING = __IMAGE_SETTING(Constants.DEFAULT_BACKGROUD)
    else:
        IMAGE_SETTING = __IMAGE_SETTING(__image_path)
    # FONT_SETTING
    __color = tuple(map(int, __custom_config['FONT_SETTING'].get('FONT_COLOR').strip('()').replace(' ', '').split(',')))
    __position = tuple(map(int, __custom_config['FONT_SETTING'].get('TEXT_POSITION').strip('()').replace(' ', '').split(',')))
    __style = __custom_config['FONT_SETTING'].get('FONT_STYLE')
    if __style == 'Default':
        __style = ''
    elif __style not in _FONT_STYLE_MAP:
        raise TypeError("文字风格 {} 不支持，请检查设置".format(__style))
    else:
        __style = r'?c=' + _FONT_STYLE_MAP[__style]
    FONT_SETTING = __FONT_SETTING(__color,
                                  __custom_config['FONT_SETTING'].getint('FONT_SIZE'),
                                  __custom_config['FONT_SETTING'].get('FONT_TYPE'),
                                  __position,
                                  __style)
    # 最终的 url 拼接
    URL = _URL + FONT_SETTING.FONT_STYLE
