# -*- coding: utf-8 -*-

from os.path import join
from PIL import Image
from io import BytesIO

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


class ImageHandleArk:

    def __init__(self, char_data_path: str, image_path: str):
        self.char_data_path = char_data_path
        self.char_data_dict = {}
        self.image_path = image_path
        self.gacha_image_path = join(self.image_path, "gacha")
        self.char_image_path = join(self.image_path, "char")
        self.background_image_path = join(self.gacha_image_path, "background.png")

    # 装载数据
    async def data_reload(self):
        self.char_data_dict = await json_read_async(self.char_data_path)

    # 十连抽图片合成处理
    async def char_ten_pulls(self, char_list: list):
        if char_list is None:
            return False
        main_image = Image.open(self.background_image_path, mode="r")
        x = 0
        for char in char_list:
            x = x + 1
            # 获取单次光效/背景/图标
            star_image = Image.open(join(self.gacha_image_path, str(self.char_data_dict[char]["星级"]) + "_star.png"))
            back_image = Image.open(join(self.gacha_image_path, str(self.char_data_dict[char]["星级"]) + "_back.png"))
            light_image = Image.open(join(self.gacha_image_path, str(self.char_data_dict[char]["星级"]) + "_light.png"))
            profession_image = Image.open(join(self.gacha_image_path, str(self.char_data_dict[char]["职业"]) + ".png"))
            # 获取角色半身图并将其缩放
            char_image = Image.open(join(self.char_image_path, "半身像_" + str(char) + ".png"))
            char_image = char_image.resize((85, 254), resample=Image.LANCZOS, reducing_gap=3.0, box=(30, 0, 150, 360))
            # 合成图片
            main_image = await get_mongolia(main_image, light_image, 18 + x * 84, 5)
            main_image = await get_mongolia(main_image, back_image, 18 + x * 84, 5)
            main_image = await get_mongolia(main_image, char_image, 18 + x * 84, 120)
            main_image = await get_mongolia(main_image, star_image, 18 + x * 84, 5)
            main_image = await get_mongolia(main_image, profession_image, 18 + x * 84, 0)
        return main_image
