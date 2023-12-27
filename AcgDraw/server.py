# -*- encoding:utf-8 -*-
import os
from datetime import datetime

from flask import Flask, send_file
from flask_apscheduler import APScheduler
from io import BytesIO
from gevent import pywsgi
import AcgDraw.drawHandleArk


class Config(object):
    SCHEDULER_API_ENABLED = True


app = Flask(__name__)

scheduler = APScheduler()

app.config.from_object(Config())
scheduler.init_app(app)
scheduler.start()


# 方舟抽卡API地址
@app.route("/arknightsdraw", methods=['POST', 'GET'])
def arknights():
    img = AcgDraw.drawHandleArk.ten_draw()
    file_object = BytesIO()
    img.save(file_object, 'PNG')
    file_object.seek(0)
    return send_file(file_object, mimetype='image/PNG')


# 原神抽卡API地址

@app.route('/', methods=['POST', 'GET'])
def arknights_draw():
    img = AcgDraw.drawHandleArk.ten_draw()
    file_object = BytesIO()
    img.save(file_object, 'PNG')
    file_object.seek(0)
    return send_file(file_object, mimetype='image/PNG')


@scheduler.task('interval', id='do_job_1', seconds=5, misfire_grace_time=900)
def job1():
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    print(now)


def server_start(mode="", host="127.0.0.1", port=11451):
    if mode == "debug":
        app.run(debug=True)
        print("测试环境")
    else:
        try:
            print("图片服务器已启动：http://" + host + ":" + str(port))
            server = pywsgi.WSGIServer((host, port), app)
            server.serve_forever()
        except OSError:
            print("端口被占用，请修改端口")
            input("回车关闭")


if __name__ == "__main__":
    server_start()
