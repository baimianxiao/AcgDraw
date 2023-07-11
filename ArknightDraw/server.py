# -*- encoding:utf-8 -*-
import os

from flask import Flask, send_file
import ArknightDraw.drawHandleArk
# import numpy as np
import io

app = Flask(__name__)


@app.route("/arknights/arknightsdraw", methods=['POST', 'GET'])
def arknights():
    img = ArknightDraw.drawHandleArk.ten_draw()
    file_object = io.BytesIO()
    img.save(file_object, 'PNG')
    file_object.seek(0)
    return send_file(file_object, mimetype='image/PNG')


@app.route('/', methods=['POST', 'GET'])
def arknights_draw():
    img = ArknightDraw.drawHandleArk.ten_draw()
    file_object = io.BytesIO()
    img.save(file_object, 'PNG')
    file_object.seek(0)
    return send_file(file_object, mimetype='image/PNG')


if __name__ == "__main__":
    app.run(debug=True)
    print("servers start")
