# -*- encoding：utf-8 -*-

import asyncio
from datetime import datetime
from io import BytesIO
from PIL import Image

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import uvicorn
import image


@asynccontextmanager
async def lifespan(app: FastAPI):
    await auto_update()
    scheduler.start()
    yield
    scheduler.shutdown()


app = FastAPI(lifespan=lifespan)


async def auto_update():
    print("定时任务执行：当前时间:", datetime.now())

scheduler = AsyncIOScheduler()

# 添加定时任务，这里以每分钟执行一次为例
scheduler.add_job(
    func=auto_update,
    trigger=IntervalTrigger(minutes=1),
    id="periodic_task",
    replace_existing=True,
)


@app.get("/")
async def root():
    return {"message": "又一个AcgDraw的站点被发现了", "version": "1.0"}


@app.get("/Arknights")
async def arknights():
    im1 = Image.open("../test/1.png", mode="r")
    im2 = Image.open("../test/2.png", mode="r")
    pil_image = await image.get_mongolia(im1, im2)
    # 将PIL图片保存到BytesIO对象中
    img_byte_arr = BytesIO()
    pil_image.save(img_byte_arr, format="PNG")  # 根据实际情况选择合适的图片格式（如PNG、JPEG等）
    # 重置BytesIO对象指针到开始位置
    img_byte_arr.seek(0)
    # 使用流式传输返回图片
    return StreamingResponse(
        img_byte_arr,
        media_type="image/PNG",
    )


@app.get("/api-admin")
async def api_admin():
    return {"message": "管理员"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
