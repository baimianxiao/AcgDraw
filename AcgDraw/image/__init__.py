# -*- coding: utf-8 -*-

from os.path import join
from PIL import Image,ImageFont,ImageDraw
from io import BytesIO
from random import randint
from AcgDraw.util import json_read_async


# 透明通道合成
async def get_mongolia(im1: Image.Image, im2: Image.Image, width=0, height=0):
    # 参数校验
    if width < 0 or height < 0:
        raise ValueError("width 和 height 必须为非负数。")

    try:
        # 转换为RGBA模式以确保透明度处理正确
        im1 = im1.convert('RGBA')
        im2 = im2.convert('RGBA')

        # 检查并处理边界条件
        im1_size = im1.size
        im2_size = im2.size

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
        raise RuntimeError("图像处理失败。") from e


# 输出图片
async def image_output(pil_image):
    # 将PIL图片保存到BytesIO对象中
    img_byte_arr = BytesIO()
    pil_image.save(img_byte_arr, format="PNG")
    # 重置BytesIO对象指针到开始位置
    img_byte_arr.seek(0)
    return img_byte_arr