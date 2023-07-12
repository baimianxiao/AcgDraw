# -*- encoding:utf-8 -*-
"""

"""
import os
import time
import ArknightDraw
from gevent import pywsgi


# 判断目录是否存在，并且在不存在时创建目录
def mkdir(path):
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path.encode("utf-8"))
        return True
    else:
        return False


# 初始化目录
create_dir_list = [
    "./static/image",
    "./templates",
    "./data/",
    "./conf"
]

print("Arknights-Draw")
input("按任意键继续")
if not os.path.exists("./data/lock.lock"):
    print("服务器未部署，开始部署")
    for create_dir in create_dir_list:
        mkdir(create_dir)
    try:
        ArknightDraw.updateArk.UpdateHandleArk("./data/Arknights/", "./conf/Arknights/").start_update()
        with open("./data/lock.lock", 'w', encoding='utf-8') as f:
            f.write("")
        ArknightDraw.server.server_start()
    except:
        print("部署发生错误，请重试")
        input("按任意键继续")
else:
    print("服务器已部署\n1.启动服务器\n2.启动更新")
    x = input("请选择操作:")
    if int(x) == 1:
        ArknightDraw.server.server_start()
    elif int(x) == 2:
        ArknightDraw.updateArk.UpdateHandleArk("./data/Arknights/", "./conf/Arknights/").start_update()
        ArknightDraw.server.server_start()
