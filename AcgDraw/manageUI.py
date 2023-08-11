# -*- encoding:utf-8 -*-
from tkinter import *


# 程序主窗口
class MainWindows(Tk):
    def __init__(self):
        super().__init__()
        self.title("AcgDraw管理面板")
        self.geometry("640x320")
        self.iconbitmap("../static/image/logo.ico")

    # 查询版本函数
    def query_version(self):

        pass


if __name__ == "__main__":
    app = MainWindows()
    app.mainloop()
