import ctypes
import os
import random
import shutil
import threading
import time
import pythoncom

from PIL import Image, ImageDraw, ImageFont
import tkinter as tk

from src.gui.systray import Systray
from src.hitokoto import Hitokoto
from constants.constants import Constants
from src.startwithsys import WithSysInit
from src.util.config_init import ConfigInit
from src.util.http_tools import HttpTools


# 获取一言数据库响应，并格式化为Hitokoto类
def get_text():
    response = HttpTools.response()
    hitokoto = Hitokoto(**response)
    return hitokoto


# This function adds data to an image
def add_text(data: Hitokoto):
    text_setting = ConfigInit.config_init().text_setting
    # Get the image from the NEW_IMAGES_PATH directory
    image_name = os.listdir(Constants.NEW_IMAGES_PATH)[0]
    image_file = Constants.NEW_IMAGES_PATH + "\\" + image_name
    image = Image.open(image_file)
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
    image.save(image_file)


# This function sets the background of the desktop to the first image in the NEW_IMAGES_PATH directory
def set_backgroud():
    # Get the path of the first image in the directory
    image_path = Constants.NEW_IMAGES_PATH + "\\" + os.listdir(Constants.NEW_IMAGES_PATH)[0]
    # Set the desktop background to the image path
    ctypes.windll.user32.SystemParametersInfoW(
        Constants.SPI_SETDESKWALLPAPER, 0, image_path, 3)


def copy_images():
    image_setting = ConfigInit.config_init().image_setting
    # Select a random image from the original image set
    images = os.listdir(image_setting.background_images_path)
    random_image = images[random.randint(0, len(images) - 1)]
    new_image = "new_image." + random_image.split(".")[1]
    # Copy the random image to the new image set folder
    src_path = image_setting.background_images_path + "\\" + random_image
    dst_path = Constants.NEW_IMAGES_PATH + "\\" + new_image
    shutil.copy2(src_path, dst_path)


def threewords():
    print("Start threewords thread")
    pythoncom.CoInitialize()
    # 双层while循环是为了当接收到 REFRESH_TEXT 时，停止第二层循环的睡眠，从第一层循环重新开始
    while True:  # 第一层循环
        while True:  # 第二层循环
            data = get_text()
            copy_images()
            add_text(data)
            set_backgroud()
            for i in range(ConfigInit.config_init().base_setting.text_update_period):
                if Constants.REFRESH_TEXT:
                    Constants.REFRESH_TEXT = False
                    break
                time.sleep(1)


if __name__ == "__main__":
    # 初始化
    WithSysInit.init()

    # 系统托盘线程实例
    systray = Systray()
    # 创建一个线程用于执行系统托盘
    systray_thread = threading.Thread(target=systray.run, name="systray_thread")

    # 创建一个线程用于执行主任务
    threewords_thread = threading.Thread(target=threewords, name="threewords_thread")
    # 将 threewords_thread 设置为守护线程， 所有非守护线程结束，则 守护线程也将结束
    threewords_thread.daemon = True

    # 运行线程
    systray_thread.start()
    threewords_thread.start()

    # 主线程等待系统托盘线程
    # 如果 系统托盘线程结束--> 主线程结束 --> threewords_thread 线程结束 --> 程序结束
    systray_thread.join()
