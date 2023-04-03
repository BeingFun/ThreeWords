import ctypes
import random
import shutil
import os
import sys
from PIL import Image, ImageDraw, ImageFont
import subprocess
import psutil
import datetime
import time
import configparser
import chardet
import winshell
import pystray
import win32gui
import win32con
import threading
import win32api
import tkinter as tk
import pystray
from datetime import datetime


# Set the system desktop background
SPI_SETDESKWALLPAPER = 20

# Whether to start with the system
START_WITH_SYSTEM = False

# Font color
COLOR = (250, 250, 250)

# 是否为可执行文件
FROZEN = getattr(sys, 'frozen', False)

# 获取当前文件所在目录的路径
if FROZEN:
    # 如果是可执行文件，则用 compass 获取可执行文件的目录
    CUR_PATH = os.path.dirname(os.path.abspath(sys.executable))
else:
    # 否则，从 __file__ 中获取当前文件的路径，并取其所在目录作为当前目录
    CUR_PATH = os.path.dirname(os.path.abspath(__file__))


ROOT_PATH = os.path.dirname(CUR_PATH)


# Location of the desktop background image folder
BACKGROUD_IMAGES_PATH = ROOT_PATH + "\\images\\origin_images"
NEW_IMAGES_PATH = ROOT_PATH + "\\images\\new_images"


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
    image_name = os.listdir(NEW_IMAGES_PATH)[0]
    image_file = NEW_IMAGES_PATH + "\\" + image_name
    image = Image.open(image_file)
    draw = ImageDraw.Draw(image)
    # Set font type and size
    font = ImageFont.truetype("simkai.ttf", 72)
    # Get text from dictionary
    text = dic_info["hitokoto"]
    color = (250, 250, 250)
    # Get size of text
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_size = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])
    # Calculate x and y coordinates for centering the text
    x = (image.width - text_size[0]) / 2
    y = (image.height - text_size[1]) / 2 - image.height * 0.10
    # Draw the text on the image
    draw.text((x, y), text, fill=color, font=font)
    # Save the image with the added text
    image.save(image_file)


# This function sets the background of the desktop to the first image in the NEW_IMAGES_PATH directory
def set_backgroud():
    # Get the path of the first image in the directory
    image_path = NEW_IMAGES_PATH + "\\" + os.listdir(NEW_IMAGES_PATH)[0]
    # Set the desktop background to the image path
    ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER, 0, image_path, 3)


def copy_images():
    # Select a random image from the original image set
    images = os.listdir(BACKGROUD_IMAGES_PATH)
    random_image = images[random.randint(0, len(images) - 1)]
    new_image = "new_image." + random_image.split(".")[1]
    # Copy the random image to the new image set folder
    src_path = BACKGROUD_IMAGES_PATH + "\\" + random_image
    dst_path = NEW_IMAGES_PATH + "\\" + new_image
    shutil.copy2(src_path, dst_path)


def is_first_or_zero():
    boot_time = psutil.boot_time()
    boot_time_dt = datetime.datetime.fromtimestamp(boot_time)
    today = datetime.datetime.today().date()
    first_flag = boot_time_dt.date == today
    now = datetime.datetime.now()
    zero_flag = now.hour == 0 and now.minute == 0 and now.second == 0
    return True if (first_flag or zero_flag) else False


# This function sets the start file for the ThreeWords program
def set_start_file():
    # Set the destination folder for the shortcut
    dst_folder = r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs\Startup'

    # Create a VBS script to run the ThreeWords program
    vbs_file = ROOT_PATH + "\\temp\\StartThreeWords.vbs"
    if FROZEN:
        vbs_run = "ThreeWords.exe"
    else:
        vbs_run = "python {} 2>null".format("ThreeWords.py")
    
    print(FROZEN)
    print(vbs_run)


    with open(vbs_file, "w") as f:
        f.write('Dim shell\n')
        f.write('Set shell = CreateObject("WScript.Shell")\n')
        f.write('shell.CurrentDirectory = "{}"\n'.format(CUR_PATH))
        f.write('shell.Run "{}", 0, True'.format(vbs_run))

    # Get the source file and shortcut path
    source_file = vbs_file
    shortcut_path = ROOT_PATH + "\\temp\\StartThreeWords.lnk"
    ico_path = ROOT_PATH + "\\resources\\threewords.ico"
    # Create a shortcut for the VBS script
    winshell.CreateShortcut(
        Path=shortcut_path,
        Target=source_file,
        Icon=(ico_path, 0),
        Description='Three Words shortcut'
    )

    # Copy the shortcut to the destination folder
    shutil.copy(shortcut_path, dst_folder)


def config_init():
    # Read the configuration file information
    config = configparser.ConfigParser(allow_no_value=False)
    config.optionxform = lambda option: option
    # Read the content of the file and use the chardet module to detect the encoding format
    configfile = ROOT_PATH + "\\config\\config.ini"
    with open(configfile, 'rb') as file:
        content = file.read()
        encoding = chardet.detect(content)['encoding']

    # Reopen the file using the detected encoding format and read the content
    with open(configfile, encoding=encoding) as file:
        config.read_file(file)

    # Get the configuration information from the file
    START_WITH_SYSTEM = config.get('BASIC_CONFIG', 'START_WITH_SYSTEM')
    BACKGROUD_IMAGES_PATH = config.get('BASIC_CONFIG', 'BACKGROUD_IMAGES_PATH')
    COLOR = config.get('BASIC_CONFIG', 'COLOR')
    TEXT_POSITION = config.get('BASIC_CONFIG', 'TEXT_POSITION')
    FIRST_USE = config.get('BASIC_CONFIG', 'FIRST_USE')

    # If it is the first time using the program and the user has set the program to start with the system,
    # set the start file and change the FIRST_USE value in the configuration file to False
    if FIRST_USE.lower() == 'true' and START_WITH_SYSTEM.lower() == 'true':
        set_start_file()
        with open(configfile, 'r', encoding=encoding) as file:
            content = file.read()
        content = content.replace('FIRST_USE = True', 'FIRST_USE = False')
        with open(configfile, 'w', encoding=encoding) as file:
            file.write(content)


def systray_init():
    print("start systray_init")
    # 获取图标文件的路径
    icon_path = os.path.join(ROOT_PATH, "resources", "threewords.ico")
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
    config_init()
    while True:
        dic_info = get_text()
        copy_images()
        add_text(dic_info)
        set_backgroud()
        time.sleep(3600)

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
    hwnd = MyWindowClass().create_window()
    win32gui.ShowWindow(hwnd, win32con.SW_HIDE)

    # 创建一个线程用于执行系统托盘
    systray_thread = threading.Thread(target=systray_init)
    # # 创建一个线程用于执行主任务
    threewords_thread = threading.Thread(target=threewords)
    threewords_thread.daemon = True

    systray_thread.start()
    threewords_thread.start()
    systray_thread.join()

    # 退出应用程序时关闭主窗口
    win32gui.PostMessage(hwnd, win32con.WM_CLOSE, 0, 0)
