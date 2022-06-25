# -*- encoding:utf-8 -*-
"""

"""
import os
import time
import ArknightDraw


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
    "./data/image"
]
for create_dir in create_dir_list:
    mkdir(create_dir)

if not os.path.exists("./data/lock.lock"):
    pass
server = ArknightDraw.server.app
server.run()
