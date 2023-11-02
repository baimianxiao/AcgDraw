# -*- encoding:utf-8 -*-

from json import dumps, loads
from PIL import Image


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
            f.write(dumps(data, ensure_ascii=False, indent=2))
        return True
    except:
        return False


def json_read(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read()
        return loads(data)
    except:
        return False
