import ctypes
import os
import time
import requests
import json
from PIL import Image
from win32api import GetMonitorInfo, MonitorFromPoint

from src.common.config import Config
from src.util.config_init import ConfigInit
from src.util.file_tools import FileTools

# 由于微软必应壁纸api 提供8张可查询图片,所以循环从 -1 到 7 循环
bing_image_idx = 0
dir_image_idx = 0


class ThreeImages:
    @staticmethod
    def get_bing_images(idx: int = 0, num: int = 1):
        """
        必应官方接口可接受的参数:
            format(非必须):    返回数据形式 js:json;xml:xml,默认js
            idx(非必须):       请求图片截至天数; -1:明天| 0:今天| 1昨天| 2前天,可选范围 [-1,7]
            n(必须):           返回数量,可选范围 [1,8]
            mkt(非必须):       地区; zh-CN:中国 ...
        """
        for i in range(Config.MAX_RETRIES):
            try:
                global bing_image_idx
                FileTools.make_folder_s(Config.BING_BACKGROUD)
                idx = bing_image_idx
                url = Config.BING_URL + "?format=js&idx={}&n={}".format(idx, num)
                response = requests.get(url, headers=Config.HEADERS, proxies={})
                response.raise_for_status()  # 如果响应状态码不是 200，会抛出异常
                response.encoding = 'utf8'
                jsonData = json.loads(response.text)
                image_url = jsonData['images'][0]['url']
                # 获取图像与信息
                image_response = requests.get("https://s.cn.bing.net/" + image_url, headers=Config.HEADERS,
                                              proxies={})
                image_response.raise_for_status()  # 如果响应状态码不是 200，会抛出异常
                image_content = image_response.content
                image_desc = str(jsonData['images'][0]['copyright']).split("(©")[0]
                image_date = jsonData['images'][0]['fullstartdate']
                image_path = Config.BING_BACKGROUD + fr"\{image_date}_{image_desc}.jpg"
                with open(image_path, "w"):
                    pass
                with open(image_path, "wb") as file:
                    file.write(image_content)
                bing_image_idx += 1
                if bing_image_idx == 8:
                    bing_image_idx = -1
                break
            except Exception as e:
                print(f'Retry {i + 1}/{Config.MAX_RETRIES}: {e}')
                time.sleep(60)
                if i == Config.MAX_RETRIES - 1:
                    raise e

    @staticmethod
    def get_image():
        global dir_image_idx
        image_setting = ConfigInit.config_init().image_setting
        if image_setting.background_from == "必应每日壁纸":
            ThreeImages.get_bing_images()
            image_setting.background_from = Config.BING_BACKGROUD
        elif image_setting.background_from == "软件自带":
            image_setting.background_from = Config.DEFAULT_BACKGROUD
        images = os.listdir(image_setting.background_from)
        if dir_image_idx >= len(images):
            dir_image_idx = 0
        image_name = images[dir_image_idx]
        dir_image_idx += 1
        # 图片大小调整、格式转换
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        __, __, screenwidth, screenheight = monitor_info.get("Monitor")
        image = Image.open(image_setting.background_from + "\\" + image_name)
        if image.size[0] != screenwidth or image.size != screenheight:
            image.resize((screenwidth, screenheight), resample=Image.LANCZOS)
        if image_name.split(".")[1].lower() not in Config.IMAGE_LLF_LIST:
            image.convert("RGBA")
        if not os.path.exists(Config.CUR_USE_IMAGE):
            os.makedirs(Config.CUR_USE_IMAGE)
        image.save(Config.CUR_USE_IMAGE + "\\cur_use.png")

    @staticmethod
    def set_background():
        image_path = Config.CUR_USE_IMAGE + "\\text_background.png"
        ctypes.windll.user32.SystemParametersInfoW(
            Config.SPI_SETDESKWALLPAPER, 0, image_path, 3)
