# -*- encoding:utf-8 -*-

import thinker


class MainWindows():
    def __int__(self):
        pass


class Add:
    def __init__(self, num1):
        self.num1 = num1

    def print(self, num2):
        print(num2 + self.num1)


add_1 = Add(1)
add_1.print(2)
add_1.print(4)

add_3=Add(3)
add_3.print(4)
