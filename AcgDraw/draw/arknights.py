#-*- encoding:utf-8 -*-

from AcgDraw.draw import *
from random import randint, choice

# 明日方舟抽卡数据处理类
class DrawHandleArk(DrawHandle):

    def __init__(self):
        super().__init__("arknights")


    async def char_once_pull(self, mode=None, group=None):
        pass

    async def char_ten_pulls(self, mode=None):
        if mode is None or mode == "default":
            draw_result = []
            limit = 0
            for i in range(10):
                x = randint(0, 1000)
                if 0 <= x <= 20:
                    draw_result.append(self.preprocess_result(choice(self.rarity_dict["char_list"]["6"])))
                    limit = limit + 6
                elif 21 <= x <= 100:
                    draw_result.append(self.preprocess_result(choice(self.rarity_dict["char_list"]["5"])))
                    limit = limit + 5
                elif 101 <= x <= 200:
                    draw_result.append(self.preprocess_result(choice(self.rarity_dict["char_list"]["4"])))
                    limit = limit + 4
                else:
                    draw_result.append(self.preprocess_result(choice(self.rarity_dict["char_list"]["3"])))
            if limit == 0:
                for i in range(randint(0, 9)):
                    draw_result[randint(0, 9)] = self.preprocess_result(choice(self.rarity_dict["char_list"]["4"]))
            print(draw_result)
            return draw_result
        elif mode == "input":
            pass
        elif mode == "special":
            pass
        else:
            print("[warning]未知的抽卡模式")



