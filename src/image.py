import ctypes
import os
import time
import shutil
import requests
import json

from src.constants.constants import Constants
from src.util.config_init import ConfigInit
from src.util.file_tools import FileTools

# 由于微软必应壁纸8张，所以循环从-1到7循环
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
        for i in range(Constants.MAX_RETRIES):
            try:
                global bing_image_idx
                FileTools.make_folder_s(Constants.BING_BACKGROUD)
                idx = bing_image_idx
                url = Constants.BING_URL + "?format=js&idx={}&n={}".format(idx, num)
                response = requests.get(url, headers=Constants.HEADERS)
                response.raise_for_status()  # 如果响应状态码不是 200，会抛出异常
                response.encoding = 'utf8'
                jsonData = json.loads(response.text)
                image_url = jsonData['images'][0]['url']
                # 获取图像与信息
                image_response = requests.get("https://s.cn.bing.net/" + image_url, headers=Constants.HEADERS)
                image_response.raise_for_status()  # 如果响应状态码不是 200，会抛出异常
                image_content = image_response.content
                image_desc = str(jsonData['images'][0]['copyright']).split("(©")[0]
                # image_title = str(jsonData['images'][0]['title'])
                image_date = jsonData['images'][0]['fullstartdate']
                image_path = Constants.BING_BACKGROUD + fr"\{image_date}_{image_desc}.jpg"
                with open(image_path, "w"):
                    pass
                with open(image_path, "wb") as file:
                    file.write(image_content)
                bing_image_idx += 1
                if bing_image_idx == 8:
                    bing_image_idx = -1
                break
            except Exception as e:
                print(f'Retry {i + 1}/{Constants.MAX_RETRIES}: {e}')
                time.sleep(60)
                if i == Constants.MAX_RETRIES - 1:
                    raise e

    @staticmethod
    def get_image():
        global dir_image_idx
        image_setting = ConfigInit.config_init().image_setting
        if image_setting.background_from == "bing":
            ThreeImages.get_bing_images()
            image_setting.background_from = Constants.BING_BACKGROUD
        images = os.listdir(image_setting.background_from)
        image = images[dir_image_idx]
        dir_image_idx += 1
        if dir_image_idx == len(images):
            dir_image_idx = 0
        # Copy the random image to the new image set folder
        src_path = image_setting.background_from + "\\" + image
        FileTools.make_folder_s(Constants.CUR_IMAGE)
        origin_image = "cur_use." + image.split(".")[1]
        dst_path = Constants.IMAGES_PATH + r"\\cur use\\" + origin_image
        shutil.copy2(src_path, dst_path)

    @staticmethod
    def set_backgroud():
        # get text image path
        # 如果没有cur_background名文件，则使用文件夹下按文件名排序的第一张图片
        text_background = None
        for image_name in os.listdir(Constants.CUR_IMAGE):
            if "text_background" in image_name:
                text_background = image_name
                break
        image_path = Constants.CUR_IMAGE + "\\" + text_background
        # Set the desktop background to the image path
        ctypes.windll.user32.SystemParametersInfoW(
            Constants.SPI_SETDESKWALLPAPER, 0, image_path, 3)
