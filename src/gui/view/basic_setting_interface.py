# coding:utf-8
import requests
from PyQt6.QtCore import Qt
from qfluentwidgets import SpinBox, SwitchButton, PrimaryPushButton, PushButton, TeachingTip, TeachingTipTailPosition, \
    TeachingTipView, HyperlinkButton, FluentIcon

from src.util.config_init import ConfigInit
from .gallery_interface import GalleryInterface
from ..common.translator import Translator
from src.util.file_tools import FileTools
from src.common.config import Config
from ..common import resource

countNum = 0


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

        # 检查更新
        self.checkUpdateButton = PrimaryPushButton()
        self.checkUpdateButton.clicked.connect(self.checkUpdate)
        self.checkUpdateButton.setText("立即检查")
        self.addExampleCard(
            self.tr('检查更新'),
            self.checkUpdateButton,
            ''
        )

    def onValueChanged(self, value):
        key = "UPDATE_PERIOD"
        FileTools.dump_config(self.parent_key, key, value)

    def onCheckedChanged(self, value):
        key = "START_WITH_SYSTEM"
        FileTools.dump_config(self.parent_key, key, value)

    def checkUpdate(self):
        global countNum

        def count():
            global countNum
            countNum += 1
            button.setText("懒死了你🤧 x" + str(countNum))

        config = Config()
        proxy = {"http": None, "https": None}
        all_info = requests.get(config.GITHUB_API, proxies=proxy).json()
        cur_update = all_info['updated_at']
        pos = TeachingTipTailPosition.LEFT_BOTTOM
        if config.LAST_UPDATE < cur_update:
            view = TeachingTipView(
                icon=None,
                title="",
                content=self.tr("检测到新版本(PS:这世上就没比我阿尼亚更勤劳的人( •̀ ω •́ )y)"),
                image=Config.IMAGES_PATH + "/anya_wow.gif",
                isClosable=True,
                tailPosition=pos,
            )
            button = HyperlinkButton(Config.RELEASE_URL, "Goto GitHub更新 && 请阿尼亚🍗", self, FluentIcon.LINK)
        else:
            view = TeachingTipView(
                icon=None,
                title="",
                content=self.tr("未检查到新版本(PS:作者可能在摸鱼¯\(°_o)/¯)"),
                image=Config.IMAGES_PATH + "/anya.webp",
                isClosable=True,
                tailPosition=pos,
            )

            button = PushButton()
            button.setText("懒死了你🤧" if countNum == 0 else "懒死了你🤧 x" + str(countNum))
            button.clicked.connect(count)

        view.addWidget(button, align=Qt.AlignmentFlag.AlignRight)
        t = TeachingTip.make(view, self.checkUpdateButton, 20000, pos, self)
        view.closed.connect(t.close)
