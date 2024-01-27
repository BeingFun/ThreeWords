import time

from src.constants.constants import Constants
from src.image import ThreeImages
from src.text import ThreeWords
from src.util.config_init import ConfigInit
from src.util.excepthread import ExcThread
from src.systray import Systray
from src.util.startwithsys import WithSysInit
from src.util.log import Log
from src.util.notification import Notification


def three():
    print("Start threewords thread")
    # 当接收到 REFRESH_TEXT 时，停止第二层循环的睡眠，从第一层循环重新开始
    break_flag = False
    data = None
    ThreeImages.get_image()
    while True:  # 第二层循环
        print("threewords thread sleep {} minutes\n".format(ConfigInit.config_init().base_setting.update_period))
        if break_flag:
            break_flag = False
        else:
            if ConfigInit.config_init().image_setting.open_background_update:
                ThreeImages.get_image()
            if ConfigInit.config_init().text_setting.open_text_update:
                data = ThreeWords.get_text()
            else:
                data = None
            ThreeWords.add_text(data)
            ThreeImages.set_backgroud()

        for i in range(ConfigInit.config_init().base_setting.update_period * 60):
            if Constants.REFRESH_TEXT:
                data = ThreeWords.get_text()
                ThreeWords.add_text(data)
                ThreeImages.set_backgroud()
                break_flag = True
                Constants.REFRESH_TEXT = False
                break
            elif Constants.REFRESH_IMAGE:
                ThreeImages.get_image()
                if ConfigInit.config_init().text_setting.open_text_update is False:
                    data = None
                ThreeWords.add_text(data)
                ThreeImages.set_backgroud()
                Constants.REFRESH_IMAGE = False
                break_flag = True
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
    # 系统托盘线程
    systray = Systray()
    systray_thread = ExcThread(target=systray.run, name="systray_thread")
    systray_thread.start()

    # Threewords 线程
    threewords_thread = ExcThread(target=three, name="threewords_thread")
    threewords_thread.start()

    thread_task_list.append(threewords_thread)
    thread_task_list.append(systray_thread)
    return thread_task_list


if __name__ == "__main__":
    """
    feature: 轮询各个子线程的状态
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
        time.sleep(1)
