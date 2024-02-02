# coding:utf-8
from qfluentwidgets import SpinBox, SwitchButton

from util.config_init import ConfigInit
from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from src.util.file_tools import FileTools


class BasicSettingInterface(GalleryInterface):
    """ Basic setting interface """

    def __init__(self, parent=None):
        translator = Translator()
        super().__init__(
            title=translator.basic,
            subtitle='threewords.components.basicsetting',
            parent=parent
        )
        self.setObjectName('BasicSettingInterface')
        self.parent_key = "BASIC_SETTING"

        # 加载配置文件
        bascisetting = ConfigInit.config_init().base_setting

        # 开机自启
        switchButton = SwitchButton(self.tr("开机随系统启动"))
        switchButton.setChecked(True if bascisetting.start_with_sys else False)
        switchButton.checkedChanged.connect(self.onCheckedChanged)
        self.addExampleCard(
            self.tr('开机随系统启动'),
            switchButton,
            ''
        )

        # 文字/背景更新周期
        spinbox = SpinBox()
        spinbox.setMinimum(1)
        spinbox.setMaximum(9999)
        spinbox.setValue(bascisetting.update_period)
        spinbox.valueChanged.connect(self.onValueChanged)
        self.addExampleCard(
            self.tr('文字/背景更新周期(单位: 分钟)'),
            spinbox,
            ''
        )

    def onValueChanged(self, value):
        key = "UPDATE_PERIOD"
        FileTools.dump_config(self.parent_key, key, value)

    def onCheckedChanged(self, value):
        key = "START_WITH_SYSTEM"
        FileTools.dump_config(self.parent_key, key, value)
