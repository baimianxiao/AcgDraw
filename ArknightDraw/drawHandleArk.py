# -*- encoding:utf-8 -*-
import json
import os.path

from PIL import Image

# 图片资源地址
background_path = os.path.join("..", "data", "Arknights", "image", "gacha", "background.png")
gacha_image_path = os.path.join("..", "data", "Arknights", "image", "gacha")
char_image_path = os.path.join("..", "data", "Arknights", "image", "char")


# 单抽图片处理
def single_image_handle():
    im = Image.open(background_path, mode="r")
    pass


# 十连图片处理
def ten_image_handle(draw_list=None):
    if draw_list is None:
        draw_list = {}
        return False
    char_list = json_read(os.path.join("..", "data", "Arknights", "char_data_list.json"))
    im = Image.open(background_path, mode="r")
    x = 0
    for char in draw_list:
        x = x + 1
        # 获取单次光效/背景/图标
        star_image = Image.open(os.path.join(gacha_image_path, str(char_list[char]["星级"]) + "_star.png"))
        back_image = Image.open(os.path.join(gacha_image_path, str(char_list[char]["星级"]) + "_back.png"))
        light_image = Image.open(os.path.join(gacha_image_path, str(char_list[char]["星级"]) + "_light.png"))
        profession_image = Image.open(os.path.join(gacha_image_path, str(char_list[char]["职业"]) + ".png"))
        # 获取角色半身图并将其缩放
        char_image = Image.open(os.path.join(char_image_path, "半身像_" + str(char) + ".png"))
        char_image = char_image.resize((85, 254), resample=Image.LANCZOS, reducing_gap=3.0, box=(30, 0, 150, 360))
        # 合成图片
        im = get_mongolia(im, light_image, 18 + x * 84, 0)
        im = get_mongolia(im, back_image, 18 + x * 84, 5)
        im = get_mongolia(im, char_image, 18 + x * 84, 120)
        im = get_mongolia(im, star_image, 18 + x * 84, 0)
        im = get_mongolia(im, profession_image, 18 + x * 84, 0)
    return im


def hundred_image_handle():
    im = Image.open(background_path, mode="r")
    pass


def ten_draw(mode=None, group=None):
    pass

# 透明通道合成
def get_mongolia(im1, im2, width=0, height=0):
    # 蒙层与图片的融合， 将im2贴到im1上
    im1_size = im1.size
    im2_size = im2.size
    crop_size = (min(im1_size[0] - width, im2_size[0]), min(im1_size[1] - height, im2_size[1]))
    im1_crop = im1.crop((width, height, crop_size[0] + width, crop_size[1] + height))
    im2_crop = im2.crop((0, 0, crop_size[0], crop_size[1]))
    mongolia = Image.alpha_composite(im1_crop, im2_crop)
    im1.paste(mongolia, (width, height), mongolia)
    return im1


def json_write(path, data) -> bool:
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(json.dumps(data, ensure_ascii=False, indent=2))
        return True
    except:
        return False


def json_read(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read()
        return json.loads(data)
    except:
        return False


if __name__ == "__main__":
    dic = ["白面鸮", "香草","白面鸮","白面鸮", "白面鸮", "白面鸮", "白面鸮", "白面鸮", "白面鸮", "白面鸮"]
    im=ten_image_handle(dic)
    im.show()
