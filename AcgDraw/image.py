# -*- coding: utf-8 -*-
import asyncio
from os import getcwd
from os.path import join

from PIL import Image

# 取根目录
dir = getcwd()  # 取根目录

# 图片资源
background_path = join(dir, "data", "Arknights", "image", "gacha", "background.png")
gacha_image_path = join(dir, "data", "Arknights", "image", "gacha")
char_image_path = join(dir, "data", "Arknights", "image", "char")


# 透明通道合成
async def get_mongolia(im1: Image.Image, im2: Image.Image, width=0, height=0):
    # 参数校验
    if width < 0 or height < 0:
        raise ValueError("width and height must be non-negative.")

    try:
        # 转换为RGBA模式以确保透明度处理正确
        im1 = im1.convert('RGBA')
        im2 = im2.convert('RGBA')

        # 检查并处理边界条件
        im1_size = im1.size
        im2_size = im2.size
        if width > im1_size[0] or height > im1_size[1] or width > im2_size[0] or height > im2_size[1]:
            raise ValueError("width or height exceeds image dimensions.")

        # 蒙层与图片的融合，将im2贴到im1上
        crop_size = (min(im1_size[0] - width, im2_size[0]), min(im1_size[1] - height, im2_size[1]))
        im1_crop = im1.crop((width, height, crop_size[0] + width, crop_size[1] + height))
        im2_crop = im2.crop((0, 0, crop_size[0], crop_size[1]))

        mongolia = Image.alpha_composite(im1_crop, im2_crop)

        # 在原图im1的指定位置粘贴处理后的图片mongolia
        im1.paste(mongolia, (width, height), mongolia)

        return im1
    except Exception as e:
        # 异常处理
        raise RuntimeError("Image processing failed.") from e


class ImageHandleArk:
    def __init__(self):
        pass

    async def ten_pulls(self):
        pass
