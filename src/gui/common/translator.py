# coding: utf-8
from PyQt6.QtCore import QObject


class Translator(QObject):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.basic = self.tr('基础设置')
        self.text = self.tr("文字设置")
        self.image = self.tr("背景图像设置")
