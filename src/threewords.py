import ctypes
import os
import random
import shutil
import threading
import time
import pythoncom

from PIL import Image, ImageDraw, ImageFont

from src.gui.systray import Systray
from src.hitokoto import Hitokoto
from src.set_start_file import set_start_file
from constants.constants import CustomConfig, Constants
from src.util.http_tools import HttpTools


# 获取一言数据库响应，并格式化为Hitokoto类
def get_text():
    response = HttpTools.response()
    hitokoto = Hitokoto(**response)
    return hitokoto


# This function adds data to an image
def add_text(data: Hitokoto):
    # Get the image from the NEW_IMAGES_PATH directory
    image_name = os.listdir(Constants.NEW_IMAGES_PATH)[0]
    image_file = Constants.NEW_IMAGES_PATH + "\\" + image_name
    image = Image.open(image_file)
    draw = ImageDraw.Draw(image)
    # Set font type and size
    font = ImageFont.truetype(CustomConfig.FONT_SETTING.FONT_TYPE.lower(), CustomConfig.FONT_SETTING.FONT_SIZE)
    text = data.hitokoto
    if CustomConfig.FONT_SETTING.TEXT_POSITION == (-1, -1):
        # Get size of text
        text_bbox = draw.textbbox((0, 0), text, font=font)
        text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])
        # Calculate x and y coordinates for centering the text
        x = (image.width - text_size[0]) / 2
        y = (image.height - text_size[1]) / 2 - image.height * 0.10
    else:
        x = CustomConfig.FONT_SETTING.TEXT_POSITION[0]
        y = CustomConfig.FONT_SETTING.TEXT_POSITION[1]
    # Draw the text on the image
    draw.text((x, y), text, fill=CustomConfig.FONT_SETTING.FONT_COLOR, font=font)
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
    # Select a random image from the original image set
    images = os.listdir(CustomConfig.IMAGE_SETTING.BACKGROUND_IMAGES_PATH)
    random_image = images[random.randint(0, len(images) - 1)]
    new_image = "new_image." + random_image.split(".")[1]
    # Copy the random image to the new image set folder
    src_path = CustomConfig.IMAGE_SETTING.BACKGROUND_IMAGES_PATH + "\\" + random_image
    dst_path = Constants.NEW_IMAGES_PATH + "\\" + new_image
    shutil.copy2(src_path, dst_path)


def threewords():
    pythoncom.CoInitialize()
    print("start threewords")

    if CustomConfig.BASIC_SETTING.START_WITH_SYSTEM:
        try:
            set_start_file()
        except PermissionError():
            print("获取管理员权限失败，随系统开机自启设置失败")

    while True:
        data = get_text()
        copy_images()
        add_text(data)
        set_backgroud()
        time.sleep(CustomConfig.BASIC_SETTING.TEXT_UPDATE_INTERVAL)


if __name__ == "__main__":
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

    # 等待系统托盘线程
    # 如果 系统托盘线程结束--> 主线程结束 --> threewords_thread 线程结束 --> 程序结束
    systray_thread.join()
