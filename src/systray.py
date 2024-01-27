import os
import subprocess
import tkinter as tk
import pystray
from PIL import Image
import webbrowser

from src.constants.constants import Constants
from src.util.config_init import ConfigInit
from src.util.dump_config import dump_config

dic = {
    "text_refresh": ["√    开启文字刷新", "      开启文字刷新"],
    "image_refresh": ["√    开启图像刷新", "      开启图像刷新"]
}
if ConfigInit.config_init().text_setting.open_text_update:
    text_refresh = dic["text_refresh"][0]
    enabled_update_text = True
else:
    text_refresh = dic["text_refresh"][1]
    enabled_update_text = False

if ConfigInit.config_init().image_setting.open_background_update:
    image_refresh = dic["image_refresh"][0]
    enabled_update_image = True
else:
    image_refresh = dic["image_refresh"][1]
    enabled_update_image = False


def refresh_image():
    Constants.REFRESH_IMAGE = True


def refresh_all():
    Constants.REFRESH_ALL = True


def show_about():
    # 创建窗口
    root = tk.Tk()
    root.title("About")
    # root.iconbitmap
    root.geometry("350x100")

    # 计算窗口左上角坐标，使其居中显示
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = int((screen_width - root.winfo_reqwidth()) / 2)
    y = int((screen_height - root.winfo_reqheight()) / 2)
    root.geometry("+{}+{}".format(x, y))

    # 在窗口中添加一个标签
    label = tk.Label(root, text="这里是三言两语应用程序 By Zhang33")
    label.pack(pady=20)

    # 左键点击
    def click(event, link):
        webbrowser.open_new(link)

    def handlerAdaptor(func, **kwds):
        '''事件处理函数的适配器'''
        return lambda event, fun=func, kwds=kwds: fun(event, **kwds)

    # 鼠标指向 光标样式
    def show_hand_cursor(event):
        text.config(cursor='arrow')

    # 鼠标离开 光标样式
    def show_xterm_cursor(event):
        text.config(cursor='xterm')

    text_name = ["GitHub", "致谢"]
    text_url = ["https://github.com/BeingFun/ThreeWords", "https://hitokoto.cn/"]

    text = tk.Text(root, font=('微软雅黑', 8))
    text.pack(pady=10)
    text.tag_config("link", foreground='blue', underline=True)

    for i in range(0, len(text_name)):
        text.tag_config(i, foreground='blue', underline=True)
        text.insert(tk.INSERT, text_name[i] + "\t", i)
        text.tag_bind(i, "<Button-1>", handlerAdaptor(click, link=text_url[i]))
        text.tag_bind(i, '<Enter>', show_hand_cursor)
        text.tag_bind(i, '<Leave>', show_xterm_cursor)

    # 运行窗口，直到用户关闭它
    root.focus()
    root.mainloop()


def show_setting():
    # 配置文件路径
    config_path = os.path.join(Constants.ROOT_PATH, 'config', 'config.ini')
    # 调用记事本打开配置文件
    subprocess.Popen(['notepad.exe', config_path])


class Systray:
    def __init__(self):
        print("Systray init")
        # 获取图标文件的路径
        icon_path = os.path.join(
            Constants.ROOT_PATH, "resources", "ico", "threewords.ico")
        icon = Image.open(icon_path)

        # 定义托盘菜单
        self.tray = pystray.Icon("ThreeWords", icon=icon)
        menu = pystray.Menu(
            pystray.MenuItem(
                text=lambda text: text_refresh, action=self.open_text_refresh
            ),
            pystray.MenuItem(
                text=lambda text: image_refresh, action=self.open_image_refresh
            ),

            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "      立即刷新文字",
                enabled=lambda enabled: enabled_update_text,
                action=self.refresh_text
            ),
            pystray.MenuItem(
                "      立即刷新图片",
                enabled=lambda enabled: enabled_update_image,
                action=refresh_image,
            ),
            pystray.MenuItem(
                text="      立即刷新全部",
                action=refresh_all,
                visible=False
            ),
            pystray.MenuItem(
                "      显示主窗口",
                self.show_main,
                visible=False
                # 参考 traffic monitor
            ),
            pystray.MenuItem(
                text="      设置",
                action=show_setting
            ),
            pystray.MenuItem(
                "      关于",
                show_about
            ),
            pystray.MenuItem(
                "      退出",
                self.tray.stop
            )
        )

        self.tray.menu = menu
        print("Systray init finish")

    def refresh_text(self):
        Constants.REFRESH_TEXT = True

    def open_text_refresh(self):
        global dic, text_refresh, enabled_update_text
        for item in dic["text_refresh"]:
            if text_refresh != item:
                text_refresh = item
                break

        if text_refresh == dic["text_refresh"][0]:
            dump_config("OPEN_TEXT_UPDATE", True)
            enabled_update_text = True
        else:
            dump_config("OPEN_TEXT_UPDATE", False)
            enabled_update_text = False
        self.tray.update_menu()

    def open_image_refresh(self):
        global dic, image_refresh, enabled_update_image
        for item in dic["image_refresh"]:
            if image_refresh != item:
                image_refresh = item
                break

        if image_refresh == dic["image_refresh"][0]:
            dump_config("OPEN_BACKGROUND_UPDATE", True)
            enabled_update_image = True
        else:
            dump_config("OPEN_BACKGROUND_UPDATE", False)
            enabled_update_image = False
        self.tray.update_menu()

    def run(self):
        print("Start systray thread")
        self.tray.run()

    def show_main(self):
        pass
