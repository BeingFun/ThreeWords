import json

from src.constants.constants import Constants


class ImageSetting:
    def __init__(self, open_image_update, background_from):
        self.open_image_update = open_image_update
        self.background_from = background_from


class TextSetting:
    def __init__(self, open_text_update, font_color, font_size, font_family, font_italic, font_bold, text_style,
                 text_form,
                 text_position):
        self.open_text_update = open_text_update
        self.font_color = font_color
        self.font_size = font_size
        self.font_family = font_family
        self.font_italic = font_italic
        self.font_bold = font_bold
        self.text_style = text_style
        self.text_from = text_form
        self.text_position = text_position


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
        config_path = Constants.ROOT_PATH + r"\config\config.json"
        with open(config_path, "r", encoding="utf-8") as load_file:
            config_dict = json.load(load_file)

        # BASIC_SETTING
        start_with_sys = (config_dict["BASIC_SETTING"]["START_WITH_SYSTEM"]) == "True"
        update_period = int(config_dict["BASIC_SETTING"]["UPDATE_PERIOD"])
        base_setting = BasicSetting(
            start_with_sys=start_with_sys,
            update_period=update_period
        )

        # IMAGE_SETTING
        open_image_update = (config_dict['IMAGE_SETTING']['OPEN_IMAGE_UPDATE']) == "True"
        background_from = config_dict['IMAGE_SETTING']['BACKGROUND_IMAGES_FROM']
        image_setting = ImageSetting(open_image_update, background_from)

        # TEXT_SETTING
        open_text_update = (config_dict["TEXT_SETTING"]["OPEN_TEXT_UPDATE"]) == "True"
        font_color = config_dict['TEXT_SETTING']['FONT_COLOR']
        position = config_dict['TEXT_SETTING']['TEXT_POSITION']
        text_style = config_dict['TEXT_SETTING']['TEXT_STYLE']
        text_from = config_dict["TEXT_SETTING"]['TEXT_FROM']
        text_setting = TextSetting(
            open_text_update=open_text_update,
            font_color=font_color,
            font_size=int(config_dict['TEXT_SETTING']['FONT_SIZE']),
            font_family=config_dict['TEXT_SETTING']['FONT_FAMILY'],
            font_italic=config_dict["TEXT_SETTING"]["FONT_ITALIC"],
            font_bold=config_dict["TEXT_SETTING"]["FONT_BOLD"],
            text_position=position,
            text_style=text_style,
            text_form=text_from)

        setting = Setting(base_setting=base_setting, image_setting=image_setting, text_setting=text_setting)
        return setting
