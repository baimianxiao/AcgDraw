# -*- encoding:utf-8 -*-
from PIL import Image

# 图片资源地址
background_path = "../data/Arknights/image/gacha/background.png"
star_image_path = {
    6: "../data/Arknights/image/gacha/6_star.png",
    5: "../data/Arknights/image/gacha/5_star.png",
    4: "../data/Arknights/image/gacha/4_star.png",
    3: "../data/Arknights/image/gacha/3_star.png"
}
# 干员职业图标
profession_image_path = {
    "先锋": "../data/Arknights/image/gacha/先锋.png",
    "医疗": "../data/Arknights/image/gacha/医疗.png",
    "术士": "../data/Arknights/image/gacha/术士.png",
    "特种": "../data/Arknights/image/gacha/特种.png",
    "狙击": "../data/Arknights/image/gacha/狙击.png",
    "辅助": "../data/Arknights/image/gacha/辅助.png",
    "近卫": "../data/Arknights/image/gacha/近卫.png",
    "重装": "../data/Arknights/image/gacha/重装.png"
}

# 干员背景光效
back_image_path = {
    6: "../data/Arknights/image/gacha/6_back.png",
    5: "../data/Arknights/image/gacha/5_back.png",
    4: "../data/Arknights/image/gacha/4_back.png",
    3: "../data/Arknights/image/gacha/3_back.png"
}


# 单抽图片处理
def single_image_handle():
    im = Image.open(background_path, mode="r")
    pass


# 十连图片处理
def ten_image_handle(draw_list=None):
    if draw_list is None:
        draw_list = {}
        return False
    im = Image.open(background_path, mode="r")
    for char in draw_list:
        star_image = Image.open()
        profession_image = Image.open()

    im.show()


def hundred_image_handle():
    im = Image.open(background_path, mode="r")
    pass


def ten_draw(mode=None, group=None):
    pass


if __name__ == "__main__":
    ten_image_handle()
