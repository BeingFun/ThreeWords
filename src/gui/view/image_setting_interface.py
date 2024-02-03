# coding:utf-8
from PyQt6.QtWidgets import QFileDialog
from qfluentwidgets import (PushButton, SwitchButton, ComboBox)

from src.util.config_init import ConfigInit
from src.util.file_tools import FileTools
from ..common.translator import Translator
from .gallery_interface import GalleryInterface


class ImageSettingInterface(GalleryInterface):
    """ Dialog interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.image,
            subtitle='threewords.components.imagesetting',
            parent=parent
        )
        self.setObjectName('dialogInterface')
        self.parent_key = "IMAGE_SETTING"

        # 加载配置文件
        imagesetting = ConfigInit.config_init().image_setting

        # 开启图像背景更新
        switchButton = SwitchButton()
        switchButton.setChecked(True if imagesetting.open_image_update else False)
        switchButton.checkedChanged.connect(self.openImageUpdate)
        self.addExampleCard(
            self.tr('开启背景图像定时更新'),
            switchButton,
            ''
        )

        # 自定义位置
        self.folerButton = PushButton(self.tr('选择文件夹'))

        # 设置背景图像来源
        comboBox = ComboBox()
        items_list = ['软件自带', '必应每日壁纸', '自定义背景图像文件夹']
        for item in items_list:
            comboBox.addItem(self.tr(item))

        # 设置默认值
        comboBox.setText(imagesetting.background_from)
        comboBox.setCurrentIndex(items_list.index(imagesetting.background_from))
        comboBox.currentTextChanged.connect(self.imageFrom)
        comboBox.setMinimumWidth(210)
        self.addExampleCard(
            self.tr('背景图像来源'),
            comboBox,
            ''
        )

        self.folerButton.clicked.connect(self.showFileDialog)
        self.addExampleCard(
            self.tr('自定义背景图像文件夹'),
            self.folerButton,
            ''
        )
        self.folerButton.setHidden(True)

    def showFileDialog(self):
        path = QFileDialog.getExistingDirectory()
        FileTools.dump_config(self.parent_key, "BACKGROUND_IMAGES_FROM", path)

    def openImageUpdate(self, value):
        FileTools.dump_config(self.parent_key, "OPEN_IMAGE_UPDATE", value)

    def imageFrom(self, value):
        if value == "自定义背景图像文件夹":
            self.folerButton.setHidden(False)
            return
        else:
            self.folerButton.setHidden(True)
        FileTools.dump_config(self.parent_key, "BACKGROUND_IMAGES_FROM", value)
