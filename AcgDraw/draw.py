# -*- coding: utf-8 -*-

from random import randint, choice
from AcgDraw.systemAction import json_read


# 明日方舟抽卡数据处理类
class DrawHandleArk:
    def __init__(self, char_star_path):
        self.char_star_path = char_star_path
        self.char_star_dict = {}

    async def data_reload(self, mode=None):
        self.char_star_dict = await json_read(self.char_star_path)
        pass

    async def char_once_draw(self, mode=None, group=None):
        pass

    async def char_ten_draw(self, mode=None, group=None):
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
