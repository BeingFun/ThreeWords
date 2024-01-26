import time

from src.constants.constants import Constants
from src.excepthread import ExcThread
from src.gui.systray import Systray
from src.startwithsys import WithSysInit
from src.threewords import ThreeWords
from src.util.config_init import ConfigInit
from src.util.log import Log
from src.util.notification import Notification


def threewords():
    print("Start threewords thread")
    # 当接收到 REFRESH_TEXT 时，停止第二层循环的睡眠，从第一层循环重新开始
    while True:  # 第二层循环
        data = ThreeWords.get_text()
        ThreeWords.copy_images()
        ThreeWords.add_text(data)
        ThreeWords.set_backgroud()
        print("threewords thread sleep {}s\n".format(ConfigInit.config_init().base_setting.text_update_period))
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
    thread_task_list = []
    # 初始化
    WithSysInit.init()
    # 系统托盘线程实例
    systray = Systray()
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
    exit_flag = False
    while True:
        for task in thread_list:
            if not task.is_alive():
                if task.exit_code == 0:
                    exit_flag = True
                    break
                log_content = (str(task.exception) + "split_symb" + task.exc_traceback)
                Log.save_log(content=log_content)
                # 当文字更新失败时，仅通知用户，重新拉起失败线程
                # raise task.exception
                Notification.send_notification(str(task.exception))
                thread_list.remove(task)
                new_thread = ExcThread(target=task.target, name=task.name)
                new_thread.start()
                thread_list.append(new_thread)
        if exit_flag:
            break
