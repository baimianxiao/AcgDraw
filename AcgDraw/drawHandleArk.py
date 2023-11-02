# -*- encoding:utf-8 -*-

from os.path import dirname, abspath, join
from random import randint, choice
from PIL import Image

from AcgDraw.drawHandle import json_read, get_mongolia

# 取根目录
dir = dirname(abspath(__file__))

# 图片资源
background_path = join(dir, "..", "data", "Arknights", "image", "gacha", "background.png")
gacha_image_path = join(dir, "..", "data", "Arknights", "image", "gacha")
char_image_path = join(dir, "..", "data", "Arknights", "image", "char")


# 单抽图片处理
def single_image_handle():
    im = Image.open(background_path, mode="r")
    pass


# 十连图片处理
def ten_image_handle(draw_list=None):
    if draw_list is None:
        draw_list = {}
        return False
    char_list = json_read(join(dir, "..", "data", "Arknights", "char_data_list.json"))
    main_image = Image.open(background_path, mode="r")
    x = 0
    for char in draw_list:
        x = x + 1
        # 获取单次光效/背景/图标
        star_image = Image.open(join(gacha_image_path, str(char_list[char]["星级"]) + "_star.png"))
        back_image = Image.open(join(gacha_image_path, str(char_list[char]["星级"]) + "_back.png"))
        light_image = Image.open(join(gacha_image_path, str(char_list[char]["星级"]) + "_light.png"))
        profession_image = Image.open(join(gacha_image_path, str(char_list[char]["职业"]) + ".png"))
        # 获取角色半身图并将其缩放
        char_image = Image.open(join(char_image_path, "半身像_" + str(char) + ".png"))
        char_image = char_image.resize((85, 254), resample=Image.LANCZOS, reducing_gap=3.0, box=(30, 0, 150, 360))
        # 合成图片
        main_image = get_mongolia(main_image, light_image, 18 + x * 84, 5)
        main_image = get_mongolia(main_image, back_image, 18 + x * 84, 5)
        main_image = get_mongolia(main_image, char_image, 18 + x * 84, 120)
        main_image = get_mongolia(main_image, star_image, 18 + x * 84, 5)
        main_image = get_mongolia(main_image, profession_image, 18 + x * 84, 0)
    return main_image


def hundred_image_handle():
    im = Image.open(background_path, mode="r")
    pass


def ten_draw(mode=None, group=None):
    if mode is None or mode == "default":
        simple_star_list = join(dir, "..", "data", "Arknights", "simple_star_list.json")
        char_list = []
        simple_star_list = json_read(simple_star_list)
        limit = 0
        for i in range(10):
            x = randint(0, 1000)
            if 0 <= x <= 20:
                char_list.append(choice(simple_star_list["6"]))
                limit = limit + 6
            elif 21 <= x <= 100:
                char_list.append(choice(simple_star_list["5"]))
                limit = limit + 5
            elif 101 <= x <= 200:
                char_list.append(choice(simple_star_list["4"]))
                limit = limit + 4
            else:
                char_list.append(choice(simple_star_list["3"]))
        if limit == 0:
            char_list[randint(0,9)] = choice(simple_star_list["4"])
        im = ten_image_handle(char_list)
        return im
    elif mode == "input":
        pass
    elif mode == "special":
        pass
    else:
        print("[warning]未知的抽卡模式")




if __name__ == "__main__":
    ten_draw()
