import ctypes
import os
import random
import shutil
from PIL import Image, ImageDraw, ImageFont
import tkinter as tk

from src.hitokoto import Hitokoto
from constants.constants import Constants
from src.util.config_init import ConfigInit
from src.util.file_tools import FileTools
from src.util.http_tools import HttpTools


class ThreeWords:
    # 获取一言数据库响应，并格式化为Hitokoto类
    @staticmethod
    def get_text():
        response = HttpTools.response()
        hitokoto = Hitokoto(**response)
        return hitokoto

    # This function adds data to an image
    @staticmethod
    def add_text(data: Hitokoto):
        text_setting = ConfigInit.config_init().text_setting
        # Get the image from the NEW_IMAGES_PATH directory
        for image_name in os.listdir(Constants.IMAGES_PATH):
            if "origin_background" in image_name:
                origin_background = image_name
        text_background = Constants.IMAGES_PATH + "\\" + "text_background." + origin_background.split(".")[1]
        origin_background = Constants.IMAGES_PATH + "\\" + origin_background
        image = Image.open(origin_background)
        draw = ImageDraw.Draw(image)
        # Set font type and size
        font = ImageFont.truetype(text_setting.font_type.lower(), text_setting.font_size)
        text = data.hitokoto
        if text_setting.text_position == (-1, -1):
            # Get size of text
            text_bbox = draw.textbbox((0, 0), text, font=font)
            text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])
            # Calculate x and y coordinates for centering the text
            x = (image.width - text_size[0]) / 2
            y = (image.height - text_size[1]) / 2 - image.height * 0.10
        else:
            x = text_setting.text_position[0]
            y = text_setting.text_position[1]
        # Draw the text on the image
        draw.text((x, y), text, fill=text_setting.font_color, font=font)

        if text_setting.text_from:
            # 计算 出处 位置
            # y 距离顶边距离
            # x 距离左边距离
            # text_size[1] 高度
            # text_size[0] 宽度
            # todo 用户配置非 -1，-1 case 处理
            from_y = y + text_size[1] * 2
            screenwidth = tk.Tk().winfo_screenwidth()
            from_x = x + text_size[0] + screenwidth * 10 / text_size[0]
            from_font = ImageFont.truetype(text_setting.font_type.lower(),
                                           int(text_setting.font_size * 0.7))
            draw.text((from_x, from_y), "——「{}」".format(data.from_), fill=text_setting.font_color,
                      font=from_font)

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
