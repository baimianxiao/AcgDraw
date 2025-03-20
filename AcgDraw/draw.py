# -*- coding: utf-8 -*-
import asyncio
from random import randint, choice, random
from AcgDraw.util import json_read_async


# 明日方舟抽卡数据处理类
class DrawHandleArk:
    def __init__(self, char_star_path):
        self.char_star_path = char_star_path
        self.char_star_dict = {}

    async def data_reload(self):
        self.char_star_dict = await json_read_async(self.char_star_path)
        pass

    async def char_once_pull(self, mode=None, group=None):
        pass

    async def char_ten_pulls(self, mode=None):
        if mode is None or mode == "default":
            draw_result = []
            limit = 0
            for i in range(10):
                x = randint(0, 1000)
                if 0 <= x <= 20:
                    draw_result.append(choice(self.char_star_dict["6"]))
                    limit = limit + 6
                elif 21 <= x <= 100:
                    draw_result.append(choice(self.char_star_dict["5"]))
                    limit = limit + 5
                elif 101 <= x <= 200:
                    draw_result.append(choice(self.char_star_dict["4"]))
                    limit = limit + 4
                else:
                    draw_result.append(choice(self.char_star_dict["3"]))
            if limit == 0:
                draw_result[randint(0, 9)] = choice(self.char_star_dict["4"])
            return draw_result
        elif mode == "input":
            pass
        elif mode == "special":
            pass
        else:
            print("[warning]未知的抽卡模式")


# 原神抽卡数据处理类
class DrawHandleGen:
    def __init__(self):
        self.data_dict_path = "data/Genshin/data_dict.json"
        self.rarity_dict_path = "data/Genshin/rarity_dict.json"
        self.data_dict = {}
        self.rarity_dict = {}

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

    async def char_once_pull(self, mode=None, group=None):
        pass

    async def char_ten_pulls(self, mode=None):
        if mode is None or mode == "default":
            draw_5_num = 0
            draw_4_num = 0
            draw_3_num = 10
            draw_weights = {'5': 100, '4': 80, '3': 0}
            remaining_weights = randint(100, 150)
            for i in range(10):
                if random() <= (0.006 + remaining_weights * 0.0001 * i):
                    draw_5_num += 1
                    draw_3_num -= 1
                    remaining_weights -= draw_weights['5']
                elif random() <= (0.0255 + remaining_weights * 0.0001 * i):
                    draw_4_num += 1
                    draw_3_num -= 1
                    remaining_weights -= draw_weights['4']
                else:
                    remaining_weights -= draw_weights['3']
            if draw_4_num == 0:
                draw_3_num -= 1
                draw_4_num += 1
            # print(str(draw_5_num) + "\n" + str(draw_4_num) + "\n" + str(draw_3_num))
            draw_result = [self.preprocess_result(choice(self.rarity_dict["global_list"]["5"])) for _ in
                           range(draw_5_num)] + \
                          [self.preprocess_result(choice(self.rarity_dict["global_list"]["4"])) for _ in
                           range(draw_4_num)] + \
                          [self.preprocess_result(choice(self.rarity_dict["weapons_list"]["3"])) for _ in
                           range(draw_3_num)]
            # (json.dumps(draw_result,indent=4)) #输出结果
            return draw_result
        elif mode == "input":
            pass
        elif mode == "special":
            pass
        else:
            print("[warning]未知的抽卡模式")


if __name__ == "__main__":
    draw_handle = DrawHandleGen()
    asyncio.run(draw_handle.data_reload())
    asyncio.run(draw_handle.char_ten_pulls())
