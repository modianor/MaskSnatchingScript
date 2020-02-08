# *_*coding:utf-8 *_*
#
import time
from threading import Thread


# 多线程并发，是不是看着和多进程很类似
def func(n):
    print('hello world')


# 并发效果，1秒打印出了所有的数字
for i in range(10):
    t = Thread(target=func, args=(i,))
    t.start()