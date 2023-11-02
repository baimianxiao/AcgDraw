# -*- encoding:utf-8 -*-

from random import randint, choice
from PIL import Image
from os.path import dirname, abspath, join

from AcgDraw.drawHandle import json_read, get_mongolia

# 取根目录
dir = dirname(abspath(__file__))

# 图片资源
background_path = join(dir, "..", "data", "Genshin", "image", "gacha", "background.png")
gacha_image_path = join(dir, "..", "data", "Genshin", "image", "gacha")
char_image_path = join(dir, "..", "data", "Genshin" "image", "char")