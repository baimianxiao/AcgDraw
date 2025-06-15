# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from AcgDraw.util import json_read_async, data_dir, join



class DrawHandle(ABC):

    def __init__(self, name: str = "default"):
        self.game_name = name
        self.data_dict_path = join(data_dir, self.game_name, "data_dict.json")
        self.rarity_dict_path = join(data_dir, self.game_name, "rarity_dict.json")
        self.data_dict = None
        self.rarity_dict = None

    async def data_reload(self):
        self.data_dict = await json_read_async(self.data_dict_path)
        self.rarity_dict = await json_read_async(self.rarity_dict_path)

    # 对抽卡的结果进行初始化，使其转化为image.py能识别的dict
    def preprocess_result(self, name):
        if name in self.data_dict["char_data_dict"].keys():
            data = self.data_dict["char_data_dict"][name]
            data["name"] = name
            data["type"] = "char"
            return data
        elif name in self.data_dict["weapons_data_dict"].keys():
            data = self.data_dict["weapons_data_dict"][name]
            data["name"] = name
            data["type"] = "weapons"
            return self.data_dict["weapons_data_dict"][name]

    @abstractmethod
    async def char_once_pull(self, mode=None, group=None):
        pass

    @abstractmethod
    async def char_ten_pulls(self, mode=None):
        pass



from .arknights import DrawHandleArk
from .genshin import DrawHandleGen

__all__ = [
    "DrawHandle",
    "DrawHandleArk",
    "DrawHandleGen"
]
