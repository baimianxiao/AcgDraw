# -*- coding: utf-8 -*-

from AcgDraw.image import *
# 原神图片处理
class ImageHandleGen:

    def __init__(self):
        self.font = ImageFont.truetype("data/genshin/zh-cn.ttf", size=20)
        self.background = Image.open("data/genshin/image/gacha/background.png", mode="r")

    # 十连抽图片合成处理
    async def char_ten_pulls(self, char_list: list):
        if char_list is None:
            return False
        else:
            char_list.reverse()
        main_image = self.background
        x = 0
        close_image = Image.open("data/genshin/image/gacha/ui_close.png")
        for char in char_list:
            if char["rarity"] == 3:
                light_offsets = 104
                y_offsets = 0
            elif char["rarity"] == 4:
                light_offsets = 5
                y_offsets = 0
            else:
                light_offsets = 0
                y_offsets = 0

            # 获取单次光效/背景/图标
            if char["type"] == "char":
                char_image = Image.open(join("data/genshin/image/char/char_min/", f"{char['name']}.png"))
                char_image = char_image.crop((2, 0, 147, 606))
                element_image = Image.open(join("data/genshin/image/gacha/", f"element_min/{char['element']}.png"))
                element_image = element_image.resize((72, 72), resample=Image.LANCZOS)
                char_x = 1592 - (x * 148)
                char_y = 238 + y_offsets
                element_x = 1628 - (x * 148)
                element_y = 670
            else:
                char_image = Image.open(join("data/genshin/image/char/weapons/", f"{char['name']}.png"))
                char_image = char_image.resize((306, 612), resample=Image.LANCZOS)
                char_image = char_image.crop((84, 0, 222, 550))
                element_image = Image.open(join("data/genshin/image/gacha/", f"weapons/{char['weapons_type']}.png"))
                element_image = element_image.resize((100, 100), resample=Image.LANCZOS)
                char_x = 1594 - (x * 148)
                char_y = 234
                element_x = 1614 - (x * 148)
                element_y = 663

            light_image = Image.open(
                join("data/genshin/image/gacha/frame/", str(char["rarity"]), f"{randint(0, 9)}.png"))
            back_image = Image.open("data/genshin/image/gacha/frame/back.png")
            stripe_image = Image.open("data/genshin/image/gacha/frame/stripe.png")
            rarity_image = Image.open(join("data/genshin/image/gacha/rarity", f"star_{char['rarity']}.png"))
            min_star_image = Image.open("data/genshin/image/gacha/frame/星星.png")

            # 合成图片
            main_image = await get_mongolia(main_image, back_image, 1587 - (x * 148), 233)
            if char["rarity"] == 5:
                main_image = await get_mongolia(main_image, stripe_image, 1590 - (x * 148), 278)
            main_image = await get_mongolia(main_image, char_image, char_x, char_y)
            main_image = await get_mongolia(main_image, light_image, 1485 - (x * 148) + light_offsets, 0)
            main_image = await get_mongolia(main_image, min_star_image, 1596 - (x * 148), 242)
            main_image = await get_mongolia(main_image, rarity_image, 1610 - (x * 148), 766)
            main_image = await get_mongolia(main_image, element_image, element_x, element_y)
            x = x + 1
        main_image = await get_mongolia(main_image, close_image, 1815, 20)
        #draw = ImageDraw.Draw(main_image)
        #draw.text( (1700, 800), "UID:114514", fill=(255, 255, 255), font=self.font)

        return main_image
