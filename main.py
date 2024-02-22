# -*- encoding:utf-8 -*-
"""

"""
import os
import sys
from datetime import datetime
from os.path import abspath, dirname, join
import AcgDraw
from AcgDraw.systemAction import json_read, json_write

# 取根目录
dir = os.getcwd()  # 取根目录


# 判断目录是否存在，并且在不存在时创建目录
def mkdir(path):
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path.encode("utf-8"))
        return True
    else:
        return False


# 写入json


host = json_read(join(dir, "conf", "global.json"))["host"]
port = int(json_read(join(dir, "conf", "global.json"))["port"])

# 初始化目录
create_dir_list = [
    "./static/image",
    "./templates",
    "./data/",
    "./conf"
]


def log_output(type: str, message: str) -> None:
    print("{}[{}]{}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), type, message))


log_output("INFO", "Arknights-Draw")

# 自动运行
if len(sys.argv) > 1:
    if sys.argv[1] == "init":
        log_output("INFO", "服务器未部署，开始部署")
        for create_dir in create_dir_list:
            mkdir(create_dir)
        try:
            AcgDraw.updateArk.UpdateHandleArk("./data/Arknights/", "./conf/Arknights/").start_update()
            with open("./data/lock.lock", 'w', encoding='utf-8') as f:
                f.write("")
        except:
            log_output("Error", "部署发生错误，请重试")
            exit(1)
        exit(0)
    elif sys.argv[1] == "update":
        AcgDraw.updateArk.UpdateHandleArk("./data/Arknights/", "./conf/Arknights/").start_update()
        AcgDraw.server.server_start(host=host, port=port)
    elif sys.argv[1] == "start":
        AcgDraw.server.server_start(host=host, port=port)
    else:
        log_output("Error", "参数错误")
        exit(1)
# 交互式
else:
    input("按任意键继续")
    if not os.path.exists("./data/lock.lock"):
        log_output("INFO", "服务器未部署，开始部署")
        for create_dir in create_dir_list:
            mkdir(create_dir)
        try:
            AcgDraw.updateArk.UpdateHandleArk("./data/Arknights/", "./conf/Arknights/").start_update()
            with open("./data/lock.lock", 'w', encoding='utf-8') as f:
                f.write("")
            AcgDraw.server.server_start(host=host, port=port)
        except:
            log_output("Error", "部署发生错误，请重试")
            input("按任意键继续")
    else:
        log_output("INFO", "服务器已部署 1.启动服务器 2.启动更新")
        x = input("请选择操作:")
        if int(x) == 1:
            AcgDraw.server.server_start(host=host, port=port)
        elif int(x) == 2:
            AcgDraw.updateArk.UpdateHandleArk("./data/Arknights/", "./conf/Arknights/").start_update()
            AcgDraw.server.server_start(host=host, port=port)
