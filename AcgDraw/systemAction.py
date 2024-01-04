# -*- encoding:utf-8 -*-

import sqlite3
from datetime import datetime
from json import dumps, loads


def json_write(path, data) -> bool:
    try:
        with open(path, 'w', encoding='utf-8') as f:
            f.write(dumps(data, ensure_ascii=False, indent=2))
        return True
    except:
        return False


def json_read(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read()
        return loads(data)
    except:
        return False


# 日志输出
def log_output(type: str, message: str) -> None:
    if type == "INFO":
        print_type = 0
        font_color = 37
        back_color = 40
    elif type == "WARNING":
        print_type = 0
        font_color = 30
        back_color = 43
    elif type == "ERROR":
        print_type = 1
        font_color = 30
        back_color = 41
    else:
        print_type = 0
        font_color = 37
        back_color = 40
    print("\033[{};{};{}m{}[{}]{}\033[0m".format(print_type, font_color, back_color,
                                                 datetime.now().strftime("%Y-%m-%d %H:%M:%S"), type, message))


class UserDataHandle:
    def __init__(self, sqlite_path: str):
        self.conn = sqlite3.connect(sqlite_path)
        self.cur = self.conn.cursor()
        print("已链接数据库")

    # 更新用户数据
    def user_data_insert(self, Name, QQ, Ex, Level, Hcy, Time):
        if self.user_data_select(QQ) is None:
            self.cur.execute(f"INSERT INTO USERDATA (Name,QQ,Ex,Level,Hcy,Time) \
                      VALUES ('{Name}','{QQ}',{Ex},{Level},{Hcy},'{Time}' )")
            self.conn.commit()
            return True
        else:
            return False

    # 检索用户数据
    def user_data_select(self, QQ):
        cursor = self.cur.execute(f"SELECT * from USERDATA WHERE QQ='{QQ}'")
        self.conn.commit()
        result = cursor.fetchall()
        if not result:
            return None
        return result

    # 更新用户数据
    def user_data_update(self, QQ, Ex, Level, Hcy, Time, Name=""):
        if self.user_data_select(QQ) is not None:
            if Name == "":
                self.cur.execute(
                    f"UPDATE USERDATA set  Ex={Ex},Level={Level},Hcy={Hcy},Time= '{Time}' where QQ='{QQ}'")
                self.conn.commit()
                return True
            else:
                self.cur.execute(
                    f"UPDATE USERDATA set Name='{Name}', Ex={Ex},Level={Level},Hcy={Hcy},Time= '{Time}' where QQ='{QQ}'")
                self.conn.commit()
                return True
        else:
            return False

    def user_data_delete(self, QQ):
        try:
            self.cur.execute(f"DELETE from USERDATA where QQ='{QQ}';")
            self.conn.commit()
            return True
        except:
            return False


if __name__ == "__main__":
    log_output("INFO", "这是一个测试段落")
    log_output("WARNING", "这是一个测试段落")
    log_output("ERROR", "这是一个测试段落")
    log_output("ABC", "这是一个测试段落")
