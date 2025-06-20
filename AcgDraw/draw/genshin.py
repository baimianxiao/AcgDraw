# -*- coding: utf-8 -*-

from . import DrawHandle
from random import randint, choice, random

# 原神抽卡数据处理类
class DrawHandleGen(DrawHandle):
    def __init__(self):
        super().__init__("genshin")

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
            # print(json.dumps(draw_result,indent=4)) #输出结果
            return draw_result
        elif mode == "input":
            pass
        elif mode == "special":
            pass
        else:
            print("[warning]未知的抽卡模式")
