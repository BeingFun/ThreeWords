import os
import subprocess
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QMainWindow
from PyQt6.QtGui import QIcon, QAction
import sys

from src.constants.constants import Constants
from src.util.config_init import ConfigInit
from src.util.file_tools import FileTools
import aboutui


def tray_ui_config():
    if ConfigInit.config_init().text_setting.open_text_update:
        open_text_icon = Constants.ICON_PATH + "switch_on.ico"
        enable_update_text = True
    else:
        open_text_icon = Constants.ICON_PATH + "switch_off.ico"
        enable_update_text = False

    if ConfigInit.config_init().image_setting.open_image_update:
        open_image_icon = Constants.ICON_PATH + "switch_on.ico"
        enable_update_image = True
    else:
        open_image_icon = Constants.ICON_PATH + "switch_off.ico"
        enable_update_image = False
    return open_text_icon, enable_update_text, open_image_icon, enable_update_image


(
    open_text_icon,
    enable_update_text,
    open_image_icon,
    enable_update_image,
) = tray_ui_config()

switch_on_icon = Constants.ICON_PATH + "switch_on.ico"
switch_off_icon = Constants.ICON_PATH + "switch_off.ico"


class MyWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.InitTrayMenuUI()

    def InitTrayMenuUI(self):
        self.tray_icon = QSystemTrayIcon()
        tray_icon = QIcon(Constants.ICON_PATH + "threewords.ico")
        self.tray_icon.setIcon(tray_icon)
        self.cur_open_text_icon = open_text_icon
        self.cur_open_image_icon = open_image_icon
        self.createTrayMenu()
        self.tray_icon.show()

    def createTrayMenu(self):
        # 创建托盘图标菜单
        self.tray_menu = QMenu()
        # 创建菜单项
        self.open_text_update = QAction(QIcon(self.cur_open_text_icon), "开启文字更新")
        self.open_image_update = QAction(QIcon(self.cur_open_image_icon), "开启图像更新")
        self.update_text = QAction(QIcon(Constants.ICON_PATH + "text.ico"), "立即更新文字")
        self.update_image = QAction(QIcon(Constants.ICON_PATH + "image.ico"), "立即更新图像")
        self.update_all = QAction(
            QIcon(Constants.ICON_PATH + "select_all.ico"), "立即更新全部"
        )
        self.setting = QAction(QIcon(Constants.ICON_PATH + "setting.ico"), "设置")
        self.about = QAction(QIcon(Constants.ICON_PATH + "about.ico"), "关于")
        self.exit = QAction(QIcon(Constants.ICON_PATH + "quit.ico"), "退出")

        # enable menu item
        update_text_flag = ConfigInit.config_init().text_setting.open_text_update
        update_image_flag = ConfigInit.config_init().image_setting.open_image_update
        update_all_flag = update_image_flag and update_text_flag
        self.update_text.setEnabled(True if update_text_flag else False)
        self.update_image.setEnabled(True if update_image_flag else False)
        self.update_all.setEnabled(True if update_all_flag else False)

        # 将菜单项添加到菜单
        self.tray_menu.addAction(self.open_text_update)
        self.tray_menu.addAction(self.open_image_update)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.update_text)
        self.tray_menu.addAction(self.update_image)
        self.tray_menu.addAction(self.update_all)
        self.tray_menu.addSeparator()
        self.tray_menu.addAction(self.setting)
        self.tray_menu.addAction(self.about)
        self.tray_menu.addAction(self.exit)

        # 设置菜单项动作
        self.open_text_update.triggered.connect(self.refresh_text_icon)
        self.open_image_update.triggered.connect(self.refresh_image_icon)
        self.update_text.triggered.connect(self.refresh_text)
        self.update_image.triggered.connect(self.refresh_image)
        self.update_all.triggered.connect(self.refresh_all)
        self.setting.triggered.connect(self.open_setting)
        self.about.triggered.connect(self.show_about)
        self.exit.triggered.connect(self.quit)

        # 设置菜单UI
        style_file = Constants.ROOT_PATH + "/resources/qss/tray_menu.qss"
        with open(style_file, "r", encoding="utf-8") as f:
            style_sheet = f.read()
        self.tray_menu.setStyleSheet(style_sheet)
        # 将菜单添加到托盘
        self.tray_icon.setContextMenu(self.tray_menu)

    def refresh_text_icon(self):
        global enable_update_text, switch_on_icon, switch_off_icon
        if enable_update_text is True:
            enable_update_text = False
            self.cur_open_text_icon = switch_off_icon
            FileTools.dump_config("OPEN_TEXT_UPDATE", False)
        else:
            enable_update_text = True
            self.cur_open_text_icon = switch_on_icon
            FileTools.dump_config("OPEN_TEXT_UPDATE", True)
        self.createTrayMenu()

    def refresh_image_icon(self):
        global enable_update_image, switch_on_icon, switch_off_icon
        if enable_update_image is True:
            enable_update_image = False
            self.cur_open_image_icon = switch_off_icon
            FileTools.dump_config("OPEN_IMAGE_UPDATE", False)
        else:
            enable_update_image = True
            self.cur_open_image_icon = switch_on_icon
            FileTools.dump_config("OPEN_IMAGE_UPDATE", True)
        self.createTrayMenu()

    def refresh_text(self):
        Constants.REFRESH_TEXT = True

    def refresh_image(self):
        Constants.REFRESH_IMAGE = True

    def refresh_all(self):
        Constants.REFRESH_ALL = True

    def open_setting(self):
        # 配置文件路径
        config_path = os.path.join(Constants.ROOT_PATH, "config", "config.ini")
        # 调用记事本打开配置文件
        subprocess.Popen(["notepad.exe", config_path])

    def show_about(self):
        aboutwindow = aboutui.Ui_Form()
        aboutwindow.setupUi(self)
        self.show()

    def quit(self):
        self.setVisible(False)
        QApplication.quit()


class SystemTray:
    @staticmethod
    def run():
        app = QApplication(sys.argv)
        QApplication.setQuitOnLastWindowClosed(False)
        my = MyWindow()
        # my.show()
        sys.exit(app.exec())


if __name__ == "__main__":
    SystemTray.run()
