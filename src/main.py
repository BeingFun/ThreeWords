import time

from src.excepthread import ExcThread
from src.gui.systray import Systray
from constants.constants import Constants
from src.startwithsys import WithSysInit
from src.threewords import ThreeWords
from src.util.config_init import ConfigInit
from src.util.log import Log


def threewords():
    print("Start threewords thread")
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


def start_child_thread():
    """
    feature:将所有子线程添加到线程列表中
    :return:
    """
    # 初始化
    WithSysInit.init()
    # 系统托盘线程实例
    systray = Systray()

    thread_task_list = []
    systray_thread = ExcThread(target=systray.run, name="systray_thread")
    systray_thread.start()

    threewords_thread = ExcThread(target=threewords, name="threewords_thread")
    threewords_thread.start()

    thread_task_list.append(threewords_thread)
    thread_task_list.append(systray_thread)
    return thread_task_list


if __name__ == "__main__":
    """
    feature: 轮询各个子线程的状态，如果有子线程失败就结束主线程 
    从而有一个子线程异常时，主线程结束，导致所有子线程(已经全部设置为守护线程)退出
    """
    thread_list = start_child_thread()
    while True:
        false_flag = False
        for task in thread_list:
            if not task.is_alive():
                log_content = (str(task.exception) + "split_symb" + task.exc_traceback)
                Log.save_log(content=log_content)
                # 当更新失败时，以静默模式退出程序，不打扰用户
                # raise task.exception
                false_flag = True
        if false_flag:
            break
        time.sleep(10)
