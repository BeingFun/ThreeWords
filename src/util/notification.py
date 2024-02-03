from plyer import notification
from src.common.config import Config


class Notification:
    @staticmethod
    def send_notification(message: str):
        app_icon = Config.ROOT_PATH + r'\resources\ico\logo.ico'
        notification.notify(
            title='Some Error',
            message=message,
            app_name='ThreeWords',
            app_icon=app_icon,
        )
