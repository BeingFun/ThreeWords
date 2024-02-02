# coding:utf-8
from PyQt6.QtCore import Qt
from qfluentwidgets import SwitchButton, TreeWidget, ComboBox, LineEdit, ColorDialog, PushButton
from PyQt6.QtWidgets import QFrame, QTreeWidgetItem, QHBoxLayout, QTreeWidgetItemIterator, QFontDialog

from util.config_init import ConfigInit
from util.file_tools import FileTools
from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from ..common.style_sheet import StyleSheet


class TextSettingInterface(GalleryInterface):
    """ Date time interface """

    def __init__(self, parent=None):
        t = Translator()
        super().__init__(
            title=t.text,
            subtitle='threewords.components.textsetting',
            parent=parent
        )
        self.setObjectName('textSettingInterface')
        self.parent_key = "TEXT_SETTING"

        # 加载配置文件
        textsetting = ConfigInit.config_init().text_setting

        # 开启文字自动更新
        switchButton = SwitchButton()
        switchButton.setChecked(True if textsetting.open_text_update else False)
        switchButton.checkedChanged.connect(self.openTextUpdate)
        self.addExampleCard(
            self.tr("开启文字定时更新"),
            switchButton,
            ''
        )

        # 文字风格
        self.frame = TreeFrame(self, True)
        self.frame.tree.itemChanged.connect(self.textStyle)
        self.addExampleCard(
            title=self.tr('文字风格选择(支持多选)'),
            widget=self.frame,
            sourcePath=''
        )

        # 显示文字出处
        switchButton = SwitchButton()
        switchButton.setChecked(True if textsetting.text_from else False)
        switchButton.checkedChanged.connect(self.textFrom)
        self.addExampleCard(
            title=self.tr('显示文字出处'),
            widget=switchButton,
            sourcePath=''
        )

        # 设置字体颜色
        buttonColor = PushButton(self.tr('选择颜色'))
        buttonColor.clicked.connect(self.showColorDialog)
        self.addExampleCard(
            self.tr('字体颜色'),
            buttonColor,
            ''
        )

        # 设置字体大小及类型
        buttonFont = PushButton(self.tr('选择字体及大小'))
        buttonFont.clicked.connect(self.showFontDialog)
        self.addExampleCard(
            self.tr('字体类型及大小'),
            buttonFont,
            ''
        )

        # 文字在屏幕中的位置
        comboBox = ComboBox()
        comboBox.setText(textsetting.text_position)
        comboBox.addItems([
            self.tr('居中'),
            self.tr('右下'),
            self.tr("左下"),
            self.tr('左上'),
            self.tr("右上"),
            self.tr("自定义位置")
        ])
        comboBox.setMinimumWidth(210)
        comboBox.currentTextChanged.connect(self.selectPos)
        self.addExampleCard(
            self.tr('文字在屏幕中的显示位置'),
            comboBox,
            ''
        )

        # 自定义位置
        self.textEdit = LineEdit()
        self.textEdit.setPlaceholderText("200,300")
        self.textEdit.editingFinished.connect(self.userPos)
        self.addExampleCard(
            self.tr('自定义文字在屏幕中的位置)'),
            self.textEdit,
            ''
        )
        self.textEdit.setHidden(True)

    def showColorDialog(self):
        w = ColorDialog(Qt.GlobalColor.cyan, self.tr('Choose color'), self.window())
        w.colorChanged.connect(lambda c: FileTools.dump_config(self.parent_key, "FONT_COLOR", c.name()))
        w.exec()

    def showFontDialog(self):
        font, ok = QFontDialog.getFont()
        if ok:
            FileTools.dump_config(self.parent_key, "FONT_SIZE", font.pointSize())
            FileTools.dump_config(self.parent_key, "FONT_FAMILY", font.family())
            FileTools.dump_config(self.parent_key, "FONT_ITALIC", font.italic())
            FileTools.dump_config(self.parent_key, "FONT_BOLD", font.bold())

    def openTextUpdate(self, value):
        key = "OPEN_TEXT_UPDATE"
        FileTools.dump_config(self.parent_key, key, value)

    def textStyle(self):
        it = QTreeWidgetItemIterator(self.frame.tree)
        key = "TEXT_STYLE"
        item_list = []
        while it.value():
            item_list.append(it.value())
            it += 1

        # 写入值
        value = ""
        if item_list[0].checkState(0) == Qt.CheckState.Checked:
            value = "All"
            for idx in range(1, len(item_list)):
                item_list[idx].setCheckState(0, Qt.CheckState.Checked)
        else:
            for idx in range(1, len(item_list)):
                if item_list[idx].checkState(0) == Qt.CheckState.Checked:
                    value = value + "&" + item_list[idx].text(0)
            value = value[1:]
        FileTools.dump_config(self.parent_key, key, value)

    def textFrom(self, value):
        key = "TEXT_FROM"
        FileTools.dump_config(self.parent_key, key, value)

    def selectPos(self, value):
        key = "TEXT_POSITION"
        if value == "自定义位置":
            self.textEdit.setHidden(False)
            return
        else:
            self.textEdit.setHidden(True)
        FileTools.dump_config(self.parent_key, key, value)

    def userPos(self):
        key = "TEXT_POSITION"
        a = self.textEdit.text()
        FileTools.dump_config(self.parent_key, key, a)


class Frame(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.hBoxLayout = QHBoxLayout(self)
        self.hBoxLayout.setContentsMargins(0, 8, 0, 0)

        self.setObjectName('frame')
        StyleSheet.VIEW_INTERFACE.apply(self)

    def addWidget(self, widget):
        self.hBoxLayout.addWidget(widget)


class TreeFrame(Frame):

    def __init__(self, parent=None, enableCheck=False):
        super().__init__(parent)
        self.tree = TreeWidget(self)
        self.addWidget(self.tree)

        item1 = QTreeWidgetItem([self.tr('All')])
        item2 = QTreeWidgetItem([self.tr('动画')])
        item3 = QTreeWidgetItem([self.tr('漫画')])
        item4 = QTreeWidgetItem([self.tr('游戏')])
        item5 = QTreeWidgetItem([self.tr('文学')])
        item6 = QTreeWidgetItem([self.tr('原创')])
        item7 = QTreeWidgetItem([self.tr('网络')])
        item8 = QTreeWidgetItem([self.tr('其他')])
        item9 = QTreeWidgetItem([self.tr('影视')])
        item10 = QTreeWidgetItem([self.tr('诗词')])
        item11 = QTreeWidgetItem([self.tr('网易云')])
        item12 = QTreeWidgetItem([self.tr('哲学')])
        item13 = QTreeWidgetItem([self.tr('抖机灵')])

        self.tree.addTopLevelItems(
            [item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12, item13])

        self.tree.expandAll()
        self.tree.setHeaderHidden(True)

        self.setFixedSize(300, 380)

        if enableCheck:
            it = QTreeWidgetItemIterator(self.tree)
            confing_text_style = ConfigInit.config_init().text_setting.text_style
            if confing_text_style == "All":
                while it.value():
                    it.value().setCheckState(0, Qt.CheckState.Checked)
                    it += 1
            else:
                confing_text_style_arr = confing_text_style.replace(" ", "").split("&")
                while it.value():
                    if it.value().text(0) in confing_text_style_arr:
                        it.value().setCheckState(0, Qt.CheckState.Checked)
                    else:
                        it.value().setCheckState(0, Qt.CheckState.Unchecked)
                    it += 1
