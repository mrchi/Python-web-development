#!/usr/bin/env python3
# coding=utf-8

"""
Thread Local 实现了 不同的线程对于内容的修改只在当前线程内生效，不同线程之间互不影响。
"""

import threading

mydata = threading.local()
mydata.score = 100
logs = []

print(mydata.score)


def f():
    mydata.score = 99
    logs.append(mydata.score)

t = threading.Thread(target=f)
t.start()
t.join()

print(mydata.score)
print(logs)
