import os
import subprocess

import tkinter as tk
import pystray
from PIL import Image
import pythoncom
import webbrowser

from constants.constants import Constants


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
                "开启图片刷新",
                self.__show_main  # TODO
            ),
            pystray.MenuItem(
                "开启文字刷新",
                self.__show_main  # TODO
            ),
            pystray.Menu.SEPARATOR,
            pystray.MenuItem(
                "立即刷新文字",
                self.__refresh_text
            ),
            pystray.MenuItem(
                "立即刷新图片",
                self.__refresh_text  # TODO
            ),
            pystray.MenuItem(
                "立即刷新全部",
                self.__refresh_text  # TODO
            ),
            pystray.MenuItem(
                "显示主窗口",
                self.__show_main  # TODO
            ),
            pystray.MenuItem(
                "设置",
                self.__show_setting  # TODO 设置菜单项 后续移动到设置主窗口中，风格参考 火绒
            ),
            pystray.MenuItem(
                "关于",
                self.__show_about  # TODO 关于菜单项 后续移动到设置主窗口中，风格参考 微软记事本
            ),
            pystray.MenuItem(
                "退出",
                self.tray.stop
            )
        )

        self.tray.menu = menu
        print("Systray init finish")

    def run(self):
        print("Start systray thread")
        pythoncom.CoInitialize()
        self.tray.run()

    def __show_about(self):
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
        label = tk.Label(root, text="这里是三言两语应用程序 By ZhangSanSan")
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

    def __show_setting(self):
        # 配置文件路径
        config_path = os.path.join(Constants.ROOT_PATH, 'config', 'config.ini')
        # 调用记事本打开配置文件
        subprocess.Popen(['notepad.exe', config_path])

    def __refresh_text(self):
        Constants.REFRESH_TEXT = True

    def __show_main(self):
        pass
