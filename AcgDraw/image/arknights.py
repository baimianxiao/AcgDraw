# -*-
from AcgDraw.image import *

# 方舟图片处理
class ImageHandleArk:

    def __init__(self):
        self.char_data_dict = {}
        self.image_path = join("data","arknights","image")
        self.gacha_image_path = join(self.image_path, "gacha")
        self.char_image_path = join(self.image_path, "char")
        self.background_image_path = join(self.gacha_image_path, "background.png")


    # 十连抽图片合成处理
    async def char_ten_pulls(self, char_list: list):
        if char_list is None:
            return False
        main_image = Image.open(self.background_image_path, mode="r")
        x = 0
        for char in char_list:
            x = x + 1
            # 获取单次光效/背景/图标
            light_image = Image.open(join(self.gacha_image_path, str(char['星级']) + "_light.png"))
            back_image = Image.open(join(self.gacha_image_path, str(char['星级']) + "_back.png"))
            profession_image = Image.open(join(self.gacha_image_path, str(char["职业"]) + ".png"))
            star_image = Image.open(join(self.gacha_image_path, str(char['星级']) + "_star.png"))

            # 获取角色半身图并将其缩放
            char_image = Image.open(join(self.char_image_path, "半身像_" + str(char['name']) + ".png"))
            char_image = char_image.resize((85, 254), resample=Image.LANCZOS, reducing_gap=3.0, box=(30, 0, 150, 360))
            # 合成图片
            main_image = await get_mongolia(main_image, light_image, 18 + x * 84, 5)
            main_image = await get_mongolia(main_image, back_image, 18 + x * 84, 5)
            main_image = await get_mongolia(main_image, char_image, 18 + x * 84, 120)
            main_image = await get_mongolia(main_image, star_image, 18 + x * 84, 5)
            main_image = await get_mongolia(main_image, profession_image, 18 + x * 84, 0)
        return main_image

