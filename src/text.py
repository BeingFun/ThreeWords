import json
import os
import time
import requests
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk

from src.image import ThreeImages
from src.util.hitokoto import Hitokoto
from src.constants.constants import Constants
from src.util.config_init import ConfigInit


class ThreeWords:
    """
    获取一言数据库响应，并格式化为 Hitokoto 类
    """

    @staticmethod
    def get_text():
        url = ConfigInit.config_init().text_setting.text_url
        response = None
        for i in range(Constants.MAX_RETRIES):
            try:
                # 发送 GET 请求
                response = requests.get(url=url, headers=Constants.HEADERS, verify=False)
                response.raise_for_status()  # 如果响应状态码不是 200，会抛出异常
                break  # 如果请求成功，则跳出循环
            except Exception as e:
                print(f'Retry {i + 1}/{Constants.MAX_RETRIES}: {e}')
                time.sleep(60)
                if i == Constants.MAX_RETRIES - 1:
                    raise e
        response_text = response.text.replace(r'"from"', r'"from_"')
        response = json.loads(response_text)
        # 将字典格式化为结构体，方便调用
        return Hitokoto(**response)

    # This function adds data to an image
    @staticmethod
    def add_text(data: Hitokoto):
        text_setting = ConfigInit.config_init().text_setting
        screenwidth = tk.Tk().winfo_screenwidth()
        screenheight = tk.Tk().winfo_screenheight()
        origin_background = None
        # Get the image from the NEW_IMAGES_PATH directory
        for image_name in os.listdir(Constants.CUR_IMAGE):
            if "cur_use" in image_name:
                origin_background = image_name
        text_background = Constants.CUR_IMAGE + "\\" + "text_background." + origin_background.split(".")[1]
        origin_background = Constants.CUR_IMAGE + "\\" + origin_background
        image = Image.open(origin_background)
        # 根据屏幕分辨率重采样图像大小,使字体在不同分辨率图像下保持一致,也一定程度上提升了图像质量
        image = image.resize((screenwidth, screenheight), resample=Image.LANCZOS)
        draw = ImageDraw.Draw(image)

        # 显示文字
        text_font = ImageFont.truetype(text_setting.font_type.lower(), text_setting.font_size)
        text = data.hitokoto
        text_bbox = draw.textbbox((0, 0), text, font=text_font)
        # text_size[1] 高度
        # text_size[0] 宽度
        text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])
        if text_setting.text_position == (-1, -1):
            # Calculate x and y coordinates for centering the text
            x = (image.width - text_size[0]) / 2
            y = (image.height - text_size[1]) / 2 - image.height * 0.10
        else:
            x = text_setting.text_position[0]
            y = text_setting.text_position[1]
        draw.text((x, y), text, fill=text_setting.font_color, font=text_font)

        # 显示文字出处
        if text_setting.text_from:
            from_font = ImageFont.truetype(text_setting.font_type.lower(), int(text_setting.font_size * 0.7))
            from_bbox = draw.textbbox((0, 0), "——「{}」".format(data.from_), font=from_font)
            from_size = (from_bbox[2] - from_bbox[0], from_bbox[3] - from_bbox[1])

            from_y = y + text_size[1] * 2
            from_x = x + text_size[0]
            # 如果文字出处的文字太长,则始终距右侧 10% 宽度距离显示
            if from_x + from_size[0] > screenwidth * 0.9:
                from_x = screenwidth * 0.9 - from_size[0]
            draw.text((from_x, from_y), "——「{}」".format(data.from_), fill=text_setting.font_color, font=from_font)

        # Save the image with the added text
        image.save(text_background)

