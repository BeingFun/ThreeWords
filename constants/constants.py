import os
import sys

FROZEN = getattr(sys, 'frozen', False)

# 获取当前文件所在目录的路径
if FROZEN:
    # 如果是可执行文件，则用 compass 获取可执行文件的目录
    _CUR_PATH = os.path.dirname(os.path.abspath(sys.executable))
else:
    # 否则，从 __file__ 中获取当前文件的路径，并取其所在目录作为当前目录
    _CUR_PATH = os.path.dirname(os.path.abspath(__file__))


class Constants:
    # 根目录
    ROOT_PATH = os.path.dirname(_CUR_PATH)

    # 文字风格 dict
    FONT_STYLE_MAP = {
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
    URL = 'https://v1.hitokoto.cn/'
    # 添加文字后的图片位置
    IMAGES_PATH = ROOT_PATH + r'\images'
    # 默认背景
    DEFAULT_BACKGROUD = IMAGES_PATH + r'\default'
    # Set the system desktop background
    SPI_SETDESKWALLPAPER = 20
    # 网页请求配置
    # 设置请求头，模拟浏览器行为
    HEADERS = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'application/json'}
    # 最大重试请求次数
    MAX_RETRIES = 3
    # 是否立即更新文本
    REFRESH_TEXT = False
