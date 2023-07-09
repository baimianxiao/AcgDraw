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
    char_list = json_read(os.path.join("..","data", "Arknights", "char_data_list.json"))
    im = Image.open(background_path, mode="r")
    for char in draw_list:
        star_image = Image.open(os.path.join(gacha_image_path, str(char_list[char]["星级"]) + "_star.png"))
        back_image = Image.open(os.path.join(gacha_image_path, str(char_list[char]["星级"]) + "_back.png"))
        profession_image = Image.open(os.path.join(gacha_image_path, str(char_list[char]["职业"]) + ".png"))
        char_image = Image.open(os.path.join(char_image_path,"半身像_"+str(char)+".png"))
        im.paste(back_image,(0,0))
        im.paste(char_image, (0, 0))
        # im.paste(profession_image, (0, 0))
        # im.paste(star_image, (30, 0))
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
    dic = ["陈"]
    ten_image_handle(dic)
