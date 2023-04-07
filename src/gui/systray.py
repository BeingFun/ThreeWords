import os
import subprocess

import tkinter as tk
import pystray
from PIL import Image
import pythoncom


from constants.constants import ROOT_PATH


class Systray:
    def __init__(self):
        print("Systray init")
        # 获取图标文件的路径
        icon_path = os.path.join(
            ROOT_PATH, "resources", "ico", "threewords.ico")
        icon = Image.open(icon_path)

        # 定义托盘菜单
        self.tray = pystray.Icon("ThreeWords", icon=icon)
        menu = pystray.Menu(
            pystray.MenuItem(
                "显示主窗口",
                self.__show_main  # TODO
            ),
            pystray.MenuItem(
                "刷新文字",
                self.__refresh_text  # TODO
            ),
            pystray.MenuItem(
                "设置",
                self.__show_setting
            ),
            pystray.MenuItem(
                "关于",
                self.__show_about  # TODO 关于菜单项 后续移动到设置主窗口中，风格参考微软记事本
            ),
            pystray.MenuItem(
                "退出",
                self.tray.stop
            )
        )
        self.tray.menu = menu
        print("Systray init finish")

    def run(self):
        print("start systray thread")
        pythoncom.CoInitialize()
        self.tray.run()

    def __show_about(self):
        # 创建窗口
        windows = tk.Tk()
        windows.title("About")
        windows.geometry("350x100")

        # 计算窗口左上角坐标，使其居中显示
        screen_width = windows.winfo_screenwidth()
        screen_height = windows.winfo_screenheight()
        x = int((screen_width - windows.winfo_reqwidth()) / 2)
        y = int((screen_height - windows.winfo_reqheight()) / 2)
        windows.geometry("+{}+{}".format(x, y))

        # 在窗口中添加一个标签
        label = tk.Label(windows, text="这里是三言两语应用程序 By ZhangSanSan")
        label.pack(pady=20)

        # 运行窗口，直到用户关闭它
        windows.mainloop()

    def __show_setting(self):
        # 配置文件路径
        config_path = os.path.join(ROOT_PATH, 'config', 'config.ini')
        # 调用记事本打开配置文件
        subprocess.Popen(['notepad.exe', config_path])

    def __refresh_text(self):
        # 涉及线程通信
        pass

    def __show_main(self):
        pass
