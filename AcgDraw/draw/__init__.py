# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from random import randint, choice, random
from AcgDraw.util import json_read_async,data_dir,join

class DrawHandle(ABC):

    def __init__(self):
        self.data_dict_path = join(data_dir,"Arknights","data_dict.json")
        self.rarity_dict_path = join(data_dir,"Arknights","rarity_dict.json")
        self.char_dict = {}
        self.rarity_dict = {}

    async def data_reload(self):
        self.char_dict = await json_read_async(self.char_data_path)
        self.rarity_dict = await json_read_async(self.rarity_dict_path)


