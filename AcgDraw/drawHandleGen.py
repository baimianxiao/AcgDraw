# -*- encoding:utf-8 -*-
from os import getcwd
from random import randint, choice
from PIL import Image
from os.path import dirname, abspath, join

from AcgDraw.drawHandle import get_mongolia

# 取根目录
dir = getcwd()  # 取根目录

# 图片资源
background_path = join(dir, "data", "Genshin", "image", "gacha", "background.png")
gacha_image_path = join(dir, "data", "Genshin", "image", "gacha")
char_image_path = join(dir, "data", "Genshin" "image", "char")