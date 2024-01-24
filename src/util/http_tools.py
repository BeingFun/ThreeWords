import json
import time

import requests
from constants.constants import Constants
from src.util.config_init import ConfigInit


class HttpTools:
    @staticmethod
    def response():
        url = ConfigInit.config_init().text_setting.text_url
        for i in range(Constants.MAX_RETRIES):
            try:
                # 发送 GET 请求
                response = requests.get(url=url, headers=Constants.HEADERS, verify=False)
                response.raise_for_status()  # 如果响应状态码不是 200，会抛出异常
                break  # 如果请求成功，则跳出循环
            except Exception as e:
                print(f'Retry {i + 1}/{Constants.MAX_RETRIES}: {e}')
                time.sleep(60)
                if i == Constants.MAX_RETRIES - 1:
                    raise e
        response_text = response.text.replace(r'"from"', r'"from_"')
        return json.loads(response_text)
