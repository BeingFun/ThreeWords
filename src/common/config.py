import os
import sys

FROZEN = getattr(sys, "frozen", False)

# 获取当前文件所在目录的路径
if FROZEN:
    # 如果是可执行文件，则用 compass 获取可执行文件的目录
    _CUR_PATH = os.path.dirname(os.path.abspath(sys.executable))
else:
    # 否则，从 __file__ 中获取当前文件的路径，并取其所在目录作为当前目录
    _CUR_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Config:
    # 根目录
    ROOT_PATH = os.path.dirname(_CUR_PATH)
    # 文字风格 dict
    FONT_STYLE_MAP = {
        "动画": "a",
        "漫画": "b",
        "游戏": "c",
        "文学": "d",
        "原创": "e",
        "网络": "f",
        "其他": "g",
        "影视": "h",
        "诗词": "i",
        "网易云": "j",
        "哲学": "k",
        "抖机灵": "l",
    }

    # 图片文件夹
    IMAGES_PATH = ROOT_PATH + r"\resources\images"
    # 默认背景文件夹
    DEFAULT_BACKGROUD = IMAGES_PATH + r"\default"
    # 必应壁纸文件夹
    BING_BACKGROUD = IMAGES_PATH + r"\bing images"
    # 当前使用壁纸文件夹
    CUR_USE_IMAGE = IMAGES_PATH + "\\cur use\\"
    # Set the system desktop background
    SPI_SETDESKWALLPAPER = 20

    # 网络资源相关配置
    # 设置请求头，模拟浏览器行为
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"
    }
    # 文字根节点
    HITOKOTO_URL = "https://v1.hitokoto.cn/"
    # 必应壁纸根节点
    BING_URL = "https://www.bing.com/HPImageArchive.aspx"
    # 最大重试请求次数
    MAX_RETRIES = 3
    # 检查更新
    GITHUB_API = "https://api.github.com/repos/BeingFun/ThreeWords"
    RELEASE_URL = "https://github.com/BeingFun/ThreeWords/releases/latest"
    LAST_UPDATE = "2023-04-03T16:05:58Z"

    # 实例变量
    REFRESH_TEXT = False
    REFRESH_IMAGE = False
    REFRESH_ALL = False
    # 图片资源
    ICON_PATH = ROOT_PATH + r"\\resources\\ico\\"
    # 图像无损格式
    IMAGE_LLF_LIST = ["png", "bmp", "tiff", "tif", "webp"]
    # 配置文件夹
    CONFIG_PATH = ROOT_PATH + r"\\config\\"
