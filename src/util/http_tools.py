import json
import requests
from constants.constants import Constants, CustomConfig


class HttpTools:
    @staticmethod
    def response():
        for i in range(Constants.MAX_RETRIES):
            try:
                # 发送 GET 请求
                response = requests.get(url=CustomConfig.URL, headers=Constants.HEADERS, verify=False)
                response.raise_for_status()  # 如果响应状态码不是 200，会抛出异常
                break  # 如果请求成功，则跳出循环
            except requests.exceptions.RequestException as e:
                print(f'Retry {i+1}/{Constants.MAX_RETRIES}: {e}')

        response_text = response.text
        response_text = response_text.replace(r'"from"', r'"from_"')
        return json.loads(response_text)
