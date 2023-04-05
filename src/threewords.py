import ctypes
import datetime
import os
import random
import shutil
import subprocess
import threading
import time
import tkinter as tk
from datetime import datetime

import psutil
import pystray
import win32api
import win32con
import win32gui
from PIL import Image, ImageDraw, ImageFont

from constants.constants import ROOT_PATH, CustomConfig, Constants
from src.set_start_file import set_start_file


# This function is used to get the text from a nodejs script
def get_text():
    # Set response_false to True initially
    response_false = True
    # Create command to run nodejs script
    cmd = ROOT_PATH + "\\nodejs\\node.exe " + ROOT_PATH + \
        "\\js\\get_hitokoto_reponse.js"
    # Loop until response_false is False
    while (response_false):
        # Run the command and store the result in result variable
        result = subprocess.run(cmd,
                                shell=True, stdout=subprocess.PIPE)
        # Decode the result to utf-8
        result = result.stdout.decode('utf-8')
        # Check if uuid is present in the result
        if "uuid" in result:
            # Set response_false to False
            response_false = False
        else:
            # Sleep for 3 seconds
            time.sleep(3)

    # Remove the first two and last three characters from the result
    result = result[2:-3]
    # Split the result into an array
    arr = result.split(",\n")
    # Create an empty dictionary
    dic_info = {}
    # Iterate over the array
    for item in arr:
        # Split each item into an array
        item_arr = item.split(":")
        # Add the item to the dictionary with key as item_arr[0] and value as item_arr[1]
        dic_info[item_arr[0].replace(" ", "")] = item_arr[1].replace("'", "")

    # Return the dictionary
    return dic_info


# This function adds text to an image
def add_text(dic_info):
    # Get the image from the NEW_IMAGES_PATH directory
    image_name = os.listdir(Constants.NEW_IMAGES_PATH)[0]
    image_file = Constants.NEW_IMAGES_PATH + "\\" + image_name
    image = Image.open(image_file)
    draw = ImageDraw.Draw(image)
    # Set font type and size
    font = ImageFont.truetype(CustomConfig.FONT_SETTING.FONT_TYPE.lower(), CustomConfig.FONT_SETTING.FONT_SIZE)
    # Get text from dictionary
    text = dic_info["hitokoto"]
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


def is_first_or_zero():
    boot_time = psutil.boot_time()
    boot_time_dt = datetime.datetime.fromtimestamp(boot_time)
    today = datetime.datetime.today().date()
    first_flag = boot_time_dt.date == today
    now = datetime.datetime.now()
    zero_flag = now.hour == 0 and now.minute == 0 and now.second == 0
    return True if (first_flag or zero_flag) else False





def systray_init():
    print("start systray_init")
    # 获取图标文件的路径
    icon_path = os.path.join(ROOT_PATH, "resources", "ico", "threewords.ico")
    icon = Image.open(icon_path)

    # 定义托盘菜单
    tray = pystray.Icon("ThreeWords", icon=icon)
    menu = pystray.Menu(
        pystray.MenuItem(
            "Quit",
            lambda: tray.stop()
        ),
        pystray.MenuItem(
            "About",
            lambda: show_about()
        )
    )
    tray.menu = menu
    # tray.visible = True
    tray.run()


def show_about():
    # 创建一个顶层窗口
    popup = tk.Toplevel()
    popup.title("About")
    popup.geometry("350x100")

    # 计算窗口左上角坐标，使其居中显示
    screen_width = popup.winfo_screenwidth()
    screen_height = popup.winfo_screenheight()
    x = int((screen_width - popup.winfo_reqwidth()) / 2)
    y = int((screen_height - popup.winfo_reqheight()) / 2)
    popup.geometry("+{}+{}".format(x, y))

    # 在窗口中添加一个标签
    label = tk.Label(popup, text="这里是三言两语应用程序，希望你今日开心哈")
    label.pack(pady=20)

    # 运行窗口，直到用户关闭它
    popup.mainloop()


def threewords():
    import pythoncom
    pythoncom.CoInitialize()
    print("start threewords")

    if CustomConfig.BASIC_SETTING.START_WITH_SYSTEM:
        try:
            set_start_file()
        except:
            print("随系统开机自启设置失败")

    while True:
        dic_info = get_text()
        copy_images()
        add_text(dic_info)
        set_backgroud()
        time.sleep(CustomConfig.BASIC_SETTING.TEXT_UPDATE_INTERVAL)

# 定义窗口类


class MyWindowClass:
    def __init__(self):
        # 注册窗口类
        wc = win32gui.WNDCLASS()
        self.hinst = wc.hInstance = win32api.GetModuleHandle(None)
        wc.lpszClassName = "MyWindowClassName"
        wc.lpfnWndProc = self.wnd_proc
        self.classAtom = win32gui.RegisterClass(wc)

    def create_window(self):
        # 创建窗口
        style = win32con.WS_POPUP
        hwnd = win32gui.CreateWindowEx(
            0,                      # 扩展风格
            self.classAtom,         # 窗口类名
            "My Window Title",      # 窗口标题
            style,                  # 窗口样式
            0, 0, 640, 480,         # 窗口位置和大小
            None,                   # 父窗口句柄
            None,                   # 菜单句柄
            self.hinst,             # 应用程序实例句柄
            None                    # 创建参数
        )
        return hwnd

    def wnd_proc(self, hwnd, msg, wparam, lparam):
        if msg == win32con.WM_DESTROY:
            win32gui.PostQuitMessage(0)
        else:
            return win32gui.DefWindowProc(hwnd, msg, wparam, lparam)


if __name__ == "__main__":
    # 隐藏主窗口
    # hwnd = MyWindowClass().create_window()
    # win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

    # 创建一个线程用于执行系统托盘
    systray_thread = threading.Thread(target=systray_init)
    # # 创建一个线程用于执行主任务
    threewords_thread = threading.Thread(target=threewords)
    threewords_thread.daemon = True

    systray_thread.start()
    threewords_thread.start()
    systray_thread.join()

    # 退出应用程序时关闭主窗口
    # win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
