import json
import time
import requests
from PIL import Image, ImageDraw, ImageFont
from win32api import GetMonitorInfo, MonitorFromPoint

from src.util.hitokoto import Hitokoto
from src.common.config import Config
from src.util.config_init import ConfigInit


class ThreeWords:
    """
    获取一言数据库响应，并格式化为 Hitokoto 类
    """

    @staticmethod
    def get_text():
        text_style = ConfigInit.config_init().text_setting.text_style
        if text_style == 'All':
            text_style = ''
        else:
            text_style_arr = text_style.replace(' ', '').split('&')
            text_style = r'?'
            for i in range(len(text_style_arr)):
                if (text_style_arr[i] not in Config.FONT_STYLE_MAP):
                    raise TypeError("文字风格 {} 不支持，请检查设置".format(text_style_arr[i]))
                if (i != len(text_style_arr) - 1):
                    text_style = text_style + r'c={}&'.format(Config.FONT_STYLE_MAP[text_style_arr[i]])
                else:
                    text_style = text_style + r'c={}'.format(Config.FONT_STYLE_MAP[text_style_arr[i]])

        text_url = Config.HITOKOTO_URL + text_style

        response = None
        for i in range(Config.MAX_RETRIES):
            try:
                # 发送 GET 请求
                # 不使用系统代理
                proxy = {"http": None, "https": None}
                response = requests.get(url=text_url, headers=Config.HEADERS, proxies=proxy)
                response.raise_for_status()  # 如果响应状态码不是 200，会抛出异常
                break  # 如果请求成功，则跳出循环
            except Exception as e:
                print(f'Retry {i + 1}/{Config.MAX_RETRIES}: {e}')
                if i == Config.MAX_RETRIES - 1:
                    raise e
                time.sleep(60)
        response_text = response.text.replace(r'"from"', r'"from_"')
        response = json.loads(response_text)
        # 将字典格式化为结构体，方便调用
        return Hitokoto(**response)

    # This function adds data to an image
    @staticmethod
    def add_text(data: Hitokoto):
        text_setting = ConfigInit.config_init().text_setting
        monitor_info = GetMonitorInfo(MonitorFromPoint((0, 0)))
        __, __, screenwidth, screenheight = monitor_info.get("Monitor")
        # 获取当前要添加文字的图片
        origin_background = Config.CUR_USE_IMAGE + "\\cur_use.png"
        image = Image.open(origin_background)
        image = image.resize((screenwidth, screenheight), resample=Image.LANCZOS)
        # 添加好文字的图片路径
        text_background = Config.CUR_USE_IMAGE + "\\" + "text_background." + origin_background.split(".")[1]
        if data is None:
            image.save(text_background)
            return

        draw = ImageDraw.Draw(image)
        text_font = ImageFont.truetype(text_setting.font_dict[text_setting.font_family], text_setting.font_size,
                                       layout_engine=ImageFont.Layout.RAQM)
        from_font = ImageFont.truetype(text_setting.font_dict[text_setting.font_family],
                                       int(text_setting.font_size * 0.7))

        # 获取 工作区间 大小
        __, __, work_width, work_height = monitor_info.get("Work")
        from_bbox = draw.textbbox((0, 0), "——「{}」".format(data.from_), font=from_font)
        from_width, from_height = (from_bbox[2] - from_bbox[0], from_bbox[3] - from_bbox[1])
        text_bbox = draw.textbbox((0, 0), data.hitokoto, font=text_font)
        text_width, text_height = (text_bbox[2] - text_bbox[0], text_bbox[3] - text_bbox[1])
        line_space = 0
        x = work_width
        y = work_height
        match text_setting.text_position:
            case "居中":
                anchor = "mm"
                if text_setting.text_from:
                    # 绘制 from 文字
                    if x / 2 + text_width / 2 + from_width > x * 0.9:
                        x = int(x * 0.9 - from_width)
                    else:
                        x = x / 2 + text_width / 2
                    y = int(y / 2 + text_height / 2)
                    xy = (x, y)
                    draw.text(xy, "——「{}」".format(data.from_), fill=text_setting.font_color, font=from_font,
                              anchor="lt")
                xy = (work_width / 2, work_height / 2)
                draw.text(xy, data.hitokoto, fill=text_setting.font_color, font=text_font,
                          anchor=anchor)
            case "左侧顶部":
                if text_setting.text_from:
                    x = text_width
                    y = text_height
                    xy = (x, y)
                    draw.text(xy, "——「{}」".format(data.from_), fill=text_setting.font_color, font=from_font,
                              anchor="lt")
                xy = (0, 0)
                draw.text(xy, data.hitokoto, fill=text_setting.font_color, font=text_font,
                          anchor="lt")
            case "左侧中部":
                if text_setting.text_from:
                    x = text_width
                    y = int(y / 2 + text_height / 2)
                    xy = (x, y)
                    draw.text(xy, "——「{}」".format(data.from_), fill=text_setting.font_color, font=from_font,
                              anchor="lt")
                xy = (0, work_height / 2)
                draw.text(xy, data.hitokoto, fill=text_setting.font_color, font=text_font,
                          anchor="lm")
            case "左侧底部":
                anchor = "ld"
                if text_setting.text_from:
                    # 绘制 from 文字
                    x = text_width
                    y = y - from_height
                    xy = (x, y)
                    draw.text(xy, "——「{}」".format(data.from_), fill=text_setting.font_color, font=from_font,
                              anchor="lt")
                    # 计算句子坐标
                    y = y - text_height - from_height
                    anchor = "lt"
                xy = (0, y)
                draw.text(xy, data.hitokoto, fill=text_setting.font_color, font=text_font,
                          anchor=anchor)
            case "中间顶部":
                if text_setting.text_from:
                    x = int(x / 2 + text_width / 2)
                    y = text_height
                    xy = (x, y)
                    draw.text(xy, "——「{}」".format(data.from_), fill=text_setting.font_color, font=from_font,
                              anchor="lt")
                xy = (work_width / 2, 0)
                draw.text(xy, data.hitokoto, fill=text_setting.font_color, font=text_font,
                          anchor="mt")
            case "中间底部":
                if text_setting.text_from:
                    y = y - from_height
                    if x / 2 + text_width / 2 + from_width > x * 0.9:
                        x = int(x * 0.9 - from_width)
                    else:
                        x = x / 2 + text_width / 2
                    xy = (x, y)
                    draw.text(xy, "——「{}」".format(data.from_), fill=text_setting.font_color, font=from_font,
                              anchor="lt")
                    # 计算句子坐标
                    y = work_height - text_height - from_height
                xy = (work_width / 2, y)
                draw.text(xy, data.hitokoto, fill=text_setting.font_color, font=text_font,
                          anchor="md")
            case "右侧顶部":
                anchor = "ra"
                if text_setting.text_from:
                    x = x - from_width
                    y = text_height
                    xy = (x, y)
                    draw.text(xy, "——「{}」".format(data.from_), fill=text_setting.font_color, font=from_font,
                              anchor="lt")
                    # 计算句子坐标
                    x = work_width - text_width - from_width
                    anchor = "lt"

                xy = (x, 0)
                draw.text(xy, data.hitokoto, fill=text_setting.font_color, font=text_font,
                          anchor=anchor)
            case "右侧中部":
                anchor = "rm"
                if text_setting.text_from:
                    x = x - from_width
                    y = work_height / 2 + text_height / 2
                    xy = (x, y)
                    draw.text(xy, "——「{}」".format(data.from_), fill=text_setting.font_color, font=from_font,
                              anchor="lt")
                    # 计算句子坐标
                    x = work_width - from_width - text_width
                    anchor = "ld"

                xy = (x, work_height / 2)
                draw.text(xy, data.hitokoto, fill=text_setting.font_color, font=text_font,
                          anchor=anchor)
            case "右侧底部":
                anchor = "rd"
                if text_setting.text_from:
                    # 绘制 from 文字
                    xy = (x, y)
                    draw.text(xy, "——「{}」".format(data.from_), fill=text_setting.font_color, font=from_font,
                              anchor="rd")
                    # 计算句子坐标
                    y = work_height - from_height - text_height - line_space
                    x = work_width - from_width - text_width
                    anchor = "lt"

                xy = (x, y)
                draw.text(xy, data.hitokoto, fill=text_setting.font_color, font=text_font,
                          anchor=anchor)
            case _:
                # 自定义位置,描点为水平左侧
                split_symb = "," if "," in text_setting.text_position else "，"
                x = int(text_setting.text_position.replace(" ", "").split(split_symb)[0])
                y = int(text_setting.text_position.replace(" ", "").split(split_symb)[1])
                xy = (x, y)
                draw.text(xy, data.hitokoto, fill=text_setting.font_color, font=text_font)
                if text_setting.text_from:
                    x = x + text_width
                    y = y + text_height
                    draw.text(xy, "——「{}」".format(data.from_), fill=text_setting.font_color, font=from_font,
                              anchor="lt")

        image.save(text_background)
