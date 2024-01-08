import threading
import time
import pythoncom

from src.gui.systray import Systray
from constants.constants import Constants
from src.startwithsys import WithSysInit
from src.threewords import ThreeWords
from src.util.config_init import ConfigInit


def threewords():
    print("Start threewords thread")
    pythoncom.CoInitialize()
    # 双层while循环是为了当接收到 REFRESH_TEXT 时，停止第二层循环的睡眠，从第一层循环重新开始
    while True:  # 第一层循环
        while True:  # 第二层循环
            data = ThreeWords.get_text()
            ThreeWords.copy_images()
            ThreeWords.add_text(data)
            ThreeWords.set_backgroud()
            for i in range(ConfigInit.config_init().base_setting.text_update_period):
                if Constants.REFRESH_TEXT:
                    Constants.REFRESH_TEXT = False
                    break
                time.sleep(1)


def main_thread():
    """
    主线程用于启动两个子线程，并检查子线程状态
    如果任意一子线程异常，退出主程序
    :return:
    """
    # 初始化
    WithSysInit.init()
    # 系统托盘线程实例
    systray = Systray()
    # 创建一个线程用于执行系统托盘
    systray_thread = threading.Thread(target=systray.run, name="systray_thread")

    # 创建一个线程用于执行主任务
    threewords_thread = threading.Thread(target=threewords, name="threewords_thread")
    # 将 threewords_thread 设置为守护线程， 所有非守护线程结束，则 守护线程也将结束
    threewords_thread.daemon = True

    # 设置为守护线程并运行
    systray_thread.daemon = True
    threewords_thread.daemon = True
    systray_thread.start()
    threewords_thread.start()

    # 添加到线程列表
    task_list = [systray_thread, threewords_thread]
    while True:
        for task in task_list:
            if not task.is_alive():
                print(f"{task.name} is not alive, main thread quit.")
                return 1
            time.sleep(1)


if __name__ == "__main__":
    main_thread()
