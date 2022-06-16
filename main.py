# -*- encoding:utf-8 -*-
"""

"""
import os
import time
import ArknightDraw


def mkdir(path):
    is_exists = os.path.exists(path)
    if not is_exists:
        os.makedirs(path.encode("utf-8"))
        return True
    else:
        return False


mkdir("/static/image")

server = ArknightDraw.server.app
server.run()
