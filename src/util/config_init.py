import configparser
import chardet

from src.constants.constants import Constants


class ImageSetting:
    def __init__(self, open_image_update, background_from):
        self.open_image_update = open_image_update
        self.background_from = background_from


class TextSetting:
    def __init__(self, open_text_update, font_color, font_size, font_type, text_style, text_form,
                 text_position, text_url):
        self.open_text_update = open_text_update
        self.font_color = font_color
        self.font_size = font_size
        self.font_type = font_type
        self.text_style = text_style
        self.text_from = text_form
        self.text_position = text_position
        self.text_url = text_url


class BasicSetting:
    def __init__(self, start_with_sys, update_period):
        self.start_with_sys = start_with_sys
        self.update_period = update_period


class Setting:
    def __init__(self, base_setting: BasicSetting, image_setting: ImageSetting, text_setting: TextSetting):
        self.base_setting = base_setting
        self.image_setting = image_setting
        self.text_setting = text_setting


class ConfigInit:
    @staticmethod
    def config_init() -> Setting:
        # Read the configuration file information
        config = configparser.ConfigParser(allow_no_value=False)
        configfile = Constants.ROOT_PATH + "\\config\\config.ini"
        with open(configfile, "rb") as file:
            content = file.read()
            encoding = chardet.detect(content)["encoding"]

        # Reopen the file using the detected encoding format and read the content
        with open(configfile, encoding=encoding) as file:
            config.read_file(file)

        dict_config = dict(config)
        # BASIC_SETTING
        start_with_sys = dict_config["BASIC_SETTING"].getboolean("START_WITH_SYSTEM")
        update_period = dict_config["BASIC_SETTING"].getint("UPDATE_PERIOD")
        base_setting = BasicSetting(
            start_with_sys=start_with_sys,
            update_period=update_period
        )

        # IMAGE_SETTING
        open_image_update = dict_config['IMAGE_SETTING'].getboolean('OPEN_IMAGE_UPDATE')
        background_from = dict_config['IMAGE_SETTING'].get('BACKGROUND_IMAGES_FROM')
        if background_from.lower() == 'default':
            background_from = Constants.DEFAULT_BACKGROUD
        elif background_from.lower() == "bing":
            background_from = "bing"
        image_setting = ImageSetting(open_image_update, background_from)

        # TEXT_SETTING
        open_text_update = dict_config["TEXT_SETTING"].getboolean("OPEN_TEXT_UPDATE")
        font_color = tuple(
            map(int, dict_config['TEXT_SETTING'].get('FONT_COLOR').strip('()').replace(' ', '').split(',')))
        position = tuple(
            map(int, dict_config['TEXT_SETTING'].get('TEXT_POSITION').strip('()').replace(' ', '').split(',')))
        text_style = str(dict_config['TEXT_SETTING'].get('TEXT_STYLE'))
        if text_style.lower() == 'default':
            text_style = ''
        else:
            text_style_arr = text_style.replace(' ', '').split('or')
            text_style = r'?'
            for i in range(len(text_style_arr)):
                if (text_style_arr[i] not in Constants.FONT_STYLE_MAP):
                    raise TypeError("文字风格 {} 不支持，请检查设置".format(text_style_arr[i]))
                if (i != len(text_style_arr) - 1):
                    text_style = text_style + r'c={}&'.format(Constants.FONT_STYLE_MAP[text_style_arr[i]])
                else:
                    text_style = text_style + r'c={}'.format(Constants.FONT_STYLE_MAP[text_style_arr[i]])
        text_from = dict_config["TEXT_SETTING"].getboolean('TEXT_FROM')
        # 最终的 url 拼接
        text_url = Constants.HITOKOTO_URL + text_style
        text_setting = TextSetting(
            open_text_update=open_text_update,
            font_color=font_color,
            font_size=dict_config['TEXT_SETTING'].getint('FONT_SIZE'),
            font_type=dict_config['TEXT_SETTING'].get('FONT_TYPE'),
            text_position=position,
            text_style=text_style,
            text_form=text_from,
            text_url=text_url)

        setting = Setting(base_setting=base_setting, image_setting=image_setting, text_setting=text_setting)
        return setting
