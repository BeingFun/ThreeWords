import ctypes
import os
import random
import shutil
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk

from src.hitokoto import Hitokoto
from src.constants.constants import Constants
from src.util.config_init import ConfigInit
from src.util.file_tools import FileTools
from src.util.http_tools import HttpTools


class ThreeWords:
    """
    获取一言数据库响应，并格式化为 Hitokoto 类
    """
    @staticmethod
    def get_text():
        response = HttpTools.response()
        # 将字典格式化为结构体，方便调用
        hitokoto = Hitokoto(**response)
        return hitokoto

    # This function adds data to an image
    @staticmethod
    def add_text(data: Hitokoto):
        text_setting = ConfigInit.config_init().text_setting
        screenwidth = tk.Tk().winfo_screenwidth()
        screenheight = tk.Tk().winfo_screenheight()
        origin_background = None
        # Get the image from the NEW_IMAGES_PATH directory
        for image_name in os.listdir(Constants.IMAGES_PATH):
            if "origin_background" in image_name:
                origin_background = image_name
        text_background = Constants.IMAGES_PATH + "\\" + "text_background." + origin_background.split(".")[1]
        origin_background = Constants.IMAGES_PATH + "\\" + origin_background
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
        FileTools.delete_file_or_folder(origin_background)

    # This function sets the background of the desktop to the first image in the NEW_IMAGES_PATH directory
    @staticmethod
    def set_backgroud():
        # get text image path
        # 如果没有cur_background名文件，则使用文件夹下按文件名排序的第一张图片
        text_background = os.listdir(Constants.IMAGES_PATH)[0]
        for image_name in os.listdir(Constants.IMAGES_PATH):
            if "text_background" in image_name:
                text_background = image_name
                break
        image_path = Constants.IMAGES_PATH + "\\" + text_background
        # Set the desktop background to the image path
        ctypes.windll.user32.SystemParametersInfoW(
            Constants.SPI_SETDESKWALLPAPER, 0, image_path, 3)

    @staticmethod
    def copy_images():
        image_setting = ConfigInit.config_init().image_setting
        # Select a random image from the original image set
        images = os.listdir(image_setting.background_images_path)
        random_image = images[random.randint(0, len(images) - 1)]
        # Copy the random image to the new image set folder
        src_path = image_setting.background_images_path + "\\" + random_image
        origin_image = "origin_background." + random_image.split(".")[1]
        dst_path = Constants.IMAGES_PATH + "\\" + origin_image
        shutil.copy2(src_path, dst_path)
