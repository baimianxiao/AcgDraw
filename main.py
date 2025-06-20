# -*- encoding:utf-8 -*-
"""

"""
import logging
import os
import sys
from datetime import datetime
from os.path import  join

import uvicorn

import AcgDraw
from AcgDraw import api
from AcgDraw.util import json_read,work_dir

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

try:
    host = json_read(join(work_dir, "conf", "config.json"))["global"]["host"]
    port = int(json_read(join(work_dir, "conf", "config.json"))["global"]["port"])
except TypeError:
    print("配置文件错误:使用默认的host和post")
    host = "127.0.0.1"
    port = 11451

# 初始化目录
create_dir_list = [
    "./static/image",
    "./data/",
    "./conf"
]


def log_output(log_type: str, message: str) -> None:
    print("{}[{}]{}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S"), log_type, message))


log_output("INFO", "Arknights-Draw")
app = api.api_app

# 测试模式
debug_mode=1
debug=False
if debug and debug_mode==1:
    uvicorn.run(app, host=host, port=port, log_level=logging.INFO,reload=False)
elif debug and debug_mode==2:
    AcgDraw.update.UpdateHandleArk("./data/Arknights/", "./conf/Arknights/").start_update()
    uvicorn.run(app, host=host, port=port, log_level=logging.INFO,reload=False)

# 自动运行
elif len(sys.argv) > 1:
    if sys.argv[1] == "init":
        log_output("INFO", "服务器未部署，开始部署")
        for create_dir in create_dir_list:
            mkdir(create_dir)
        try:
            AcgDraw.update.UpdateHandleArk("./data/Arknights/", "./conf/Arknights/").start_update()
            with open("./data/lock.lock", 'w', encoding='utf-8') as f:
                f.write("")
        except:
            log_output("Error", "部署发生错误，请重试")
            exit(1)
        exit(0)
    elif sys.argv[1] == "update":
        AcgDraw.update.UpdateHandleArk("./data/Arknights/", "./conf/Arknights/").start_update()
        uvicorn.run(app, host=host, port=port, log_level=logging.INFO)
    elif sys.argv[1] == "start":
        uvicorn.run(app, host=host, port=port, log_level=logging.INFO)
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
            AcgDraw.update.UpdateHandleArk("./data/Arknights/", "./conf/Arknights/").start_update()
            with open("./data/lock.lock", 'w', encoding='utf-8') as f:
                f.write("")
            uvicorn.run(app, host=host, port=port, log_level=logging.INFO)
        except:
            log_output("Error", "部署发生错误，请重试")
            input("按任意键继续")
    else:
        log_output("INFO", "服务器已部署 1.启动服务器 2.启动更新")
        x = input("请选择操作(default：1.启动服务器):")
        if int(x) == 1:
            uvicorn.run(app, host=host, port=port, log_level=logging.INFO)

        elif int(x) == 2:
            AcgDraw.update.UpdateHandleArk("./data/Arknights/", "./conf/Arknights/").start_update()
            uvicorn.run(app, host=host, port=port, log_level=logging.INFO)

        else:
            uvicorn.run(app, host=host, port=port, log_level=logging.INFO)

