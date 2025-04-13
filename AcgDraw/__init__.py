# -*- encoding:utf-8 -*-

import AcgDraw.update
from AcgDraw.draw import *
from AcgDraw.image import *
from AcgDraw.url_tool import *

# 抽卡随机生成器
from AcgDraw.draw.arknights import DrawHandleArk
from AcgDraw.draw.genshin import DrawHandleGen

# 抽卡图片合成器
from AcgDraw.image.arknights import ImageHandleArk
from AcgDraw.image.genshin import ImageHandleGen


__all__ = [
    "DrawHandleArk",
    "DrawHandleGen",
    "ImageHandleArk",
    "ImageHandleGen",
    "api",
    "util",
    "url_tool",
    "version"
]

version = "v3.1.3"

__init_dict__ = {
    "path_list":{
        "arknights":[],
        "genshin":[]
    }
}
__default_init_config__:{

}
__default_global_config__ = {
    "global": {
        "host": "127.0.0.1",
        "port": "11451"
    },
    "apiArk": {
        "route": "/ArknightsDraw"
    },
    "apiGen": {
        "route": "/GenshinDraw"
    },
    "autoTask": {
        "autoUpdate": {
            "globalMode": 1,
            "globalCycle": "week",
            "globalTime": "1:00"
        }
    },
    "url": {
        "enable": False,
        "domain": ""
    }
}

def initialize():
    pass

def initialize_config(config_path: str, config_path_list: list):
    pass

def initialize_data(data_path: str,data_path_list: list):
    if data_path_list is None:
        pass


def update_app():
    pass
