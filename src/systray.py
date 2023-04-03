# import os
# import pystray
# from PIL import Image


# def init(root_paht):
#     # 定义托盘图标
#     icon_path = root_paht + "\\threewords\\res\\threewords.ico"
#     print(icon_path)
#     icon = Image.open(icon_path)

#     # 定义托盘菜单
#     menu = pystray.Menu(
#         pystray.MenuItem(
#             "Exit",
#             lambda: pystray.stop()
#         ),
#         pystray.MenuItem(
#             "About",
#             lambda: print("每日一句")
#         )
#     )
#     tray = pystray.Icon("ThreeWords", icon=icon, menu=menu)
#     return tray
