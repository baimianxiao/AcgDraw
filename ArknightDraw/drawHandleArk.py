# -*- encoding:utf-8 -*-
import json
import os.path

from PIL import Image

# 图片资源地址
background_path = os.path.join("..", "data", "Arknights", "image", "gacha", "background.png")
image_path = os.path.join("..", "data", "Arknights", "image", "gacha")


# 单抽图片处理
def single_image_handle():
    im = Image.open(background_path, mode="r")
    pass


# 十连图片处理
def ten_image_handle(draw_list=None):
    if draw_list is None:
        draw_list = {}
        return False
    char_list = json_read(os.path.join("..","data", "Arknights", "char_data_list.json"))
    im = Image.open(background_path, mode="r")
    for char in draw_list:
        star_image = Image.open(os.path.join(image_path, str(char_list[char]["星级"])+"_star.png"))
        profession_image = Image.open(os.path.join(image_path, str(char_list[char]["职业"])+".png"))
    im.show()


def hundred_image_handle():
    im = Image.open(background_path, mode="r")
    pass


def ten_draw(mode=None, group=None):
    pass


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
    dic = ["香草"]
    ten_image_handle(dic)
