# -*- encoding：utf-8 -*-

from datetime import datetime
from os.path import join

from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from contextlib import asynccontextmanager
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
import uvicorn
from fastapi import Request

from AcgDraw import DrawHandleArk, DrawHandleGen, version
from AcgDraw.image import image_output, ImageHandleArk, ImageHandleGen
from AcgDraw.url_tool import generate_temp_image_url, clean_temp_folder, url_enable
from AcgDraw.util import work_dir


async def initialize_app(app: FastAPI):
    app.state.ark_draw = DrawHandleArk()
    app.state.ark_image = ImageHandleArk(join(work_dir, "data", "Arknights", "data_dict.json"),
                                         join(work_dir, "data", "Arknights", "image"))
    app.state.gen_draw = DrawHandleGen()
    app.state.gen_image = ImageHandleGen(join(work_dir, "data", "Arknights", "data_dict.json"),
                                         join(work_dir, "data", "Arknights", "image"))
    # 装载图片
    await app.state.ark_draw.data_reload()
    await app.state.ark_image.data_reload()
    await app.state.gen_draw.data_reload()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_app(app)
    await auto_update()
    scheduler.start()
    yield
    scheduler.shutdown()


api_app = FastAPI(lifespan=lifespan)
api_app.mount("/tmp", StaticFiles(directory="temp-images"), name="temp-images")


async def auto_update():
    print("定时任务执行：当前时间:", datetime.now())


async def result_get(draw_mode: str, game: str, result_list: list = None):
    result = {}
    if not result_list:
        result_list = ['json']
    print(result_list)
    if game == "arknights" and draw_mode == "ten":
        if "json" in result_list:
            result['json'] = await api_app.state.ark_draw.char_ten_pulls()
        if "image_url" in result_list:
            pil_image = await pil_image_get(draw_mode, game, result['json'])
            temp_image_url = generate_temp_image_url(pil_image)
            result["image_url"] = temp_image_url
        return result
    elif game == "genshin" and draw_mode == "ten":
        if "json" in result_list:
            result['json'] = await api_app.state.gen_draw.char_ten_pulls()
        if "image_url" in result_list:
            pil_image = await pil_image_get(draw_mode, game, result['json'])
            temp_image_url = generate_temp_image_url(pil_image)
            result["image_url"] = temp_image_url
        return result
    else:
        return None


async def pil_image_get(draw_mode: str, game: str, result):
    if result is None:
        return None
    if game == "arknights" and draw_mode == "ten":
        pil_image = await api_app.state.ark_image.char_ten_pulls(result)
        return pil_image
    elif game == "genshin" and draw_mode == "ten":
        pil_image = await api_app.state.gen_image.char_ten_pulls(result)
        return pil_image
    else:
        return None


scheduler = AsyncIOScheduler()

scheduler.add_job(
    func=auto_update,
    trigger=IntervalTrigger(days=1),
    id="auto_update",
    replace_existing=True,
)

scheduler.add_job(
    func=clean_temp_folder,
    trigger="interval",
    hours=1,
    id="auto_clean",
    replace_existing=True,
)


@api_app.get("/")
async def root():
    return {"message": "又一个AcgDraw的站点被发现了", "version": version, "API": "/api/draw/"}


@api_app.get("/api/draw/json")
async def get_draw_json(uid, game, mode):
    pass


@api_app.get("/api/draw/image")
async def get_draw_image(uid, game, mode, need):
    pass


@api_app.post("/api/draw/json")
async def post_draw_json(request: Request):
    try:
        data = await request.json()
        uid = str(data.get("uid"))
        game = str(data.get("game")).lower()
        draw_mode = str(data.get("draw_mode")).lower()
        result_list = list(data.get("result_list"))
    except Exception as e:
        response = {"code": 400, "msg": f"bad request: {e}", "data": None}
        return response

    result = await result_get(draw_mode, game, result_list)
    print(result)
    if result is None:
        response = {"code": 400, "msg": "bad request: wrong game or mode", "data": None}
        return response
    result_obj = {"uid": uid, "game": game, "mode": draw_mode, "result": result}
    response = {"code": 200, "msg": "success", "data": result_obj}
    return response


@api_app.post("/api/draw/image")
async def post_draw_image(request: Request):
    try:
        data = await request.json()
        uid = str(data.get("uid"))
        game = str(data.get("game")).lower()
        draw_mode = str(data.get("draw_mode")).lower()
    except Exception as e:
        response = {"code": 400, "msg": f"bad request: {e}", "data": None}
        return response
    result = await result_get(draw_mode, game)
    if result is None:
        response = {"code": 400, "msg": "bad request: wrong game or mode", "data": None}
    pil_image = await pil_image_get(draw_mode, game, result['json'])
    img_byte_arr = await image_output(pil_image)
    # 使用流式传输返回图片
    response = StreamingResponse(
        img_byte_arr,
        media_type="image/PNG",
    )
    response.headers["message"] = "success"
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@api_app.get("/api-admin")
async def api_admin():
    return {"message": "管理员"}


if __name__ == "__main__":
    uvicorn.run(api_app, host="0.0.0.0", port=8000)
