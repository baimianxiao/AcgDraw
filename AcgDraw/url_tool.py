# -*- encoding：utf-8 -*-

import time
from os import getcwd
from os.path import join
import tempfile
import os

from AcgDraw.util import config,Logger

work_dir = getcwd()
log = Logger(f"{work_dir}/log.txt")

try:

    url_enable = bool(config["url"]["enable"])
    domain = str(config["url"]["domain"])
    port = int(config["global"]["port"])
except Exception as e:
    url_enable = False
    domain = ""
    port = 11451
    print(f"配置文件读取失败，已禁用 URL 功能。错误信息: {str(e)}")

if url_enable and domain == "":
    domain = "http://localhost"
    print(f"url模式启用，但未指定域名，使用默认域名: {domain}")


def generate_temp_image_url(pil_image):
    if pil_image is None:
        return None
    # 创建专用临时目录
    temp_dir = os.path.join(work_dir, "temp-images")
    os.makedirs(temp_dir, exist_ok=True)

    # 创建临时文件（保留文件引用）
    temp_file = tempfile.NamedTemporaryFile(
        dir=temp_dir,
        delete=False,
        suffix=".png"
    )
    pil_image.save(temp_file, format="PNG")
    temp_file.close()

    # 生成访问URL
    return f"{domain}:{port}/tmp/{os.path.basename(temp_file.name)}"

def clean_temp_folder():
    """清理超过1小时的临时文件"""
    temp_dir = os.path.join(work_dir, "temp-images")
    now = time.time()

    for f in os.listdir(temp_dir):
        file_path = os.path.join(temp_dir, f)
        if os.stat(file_path).st_mtime < now - 3600:
            os.unlink(file_path)