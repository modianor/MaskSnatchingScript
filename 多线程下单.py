# *_*coding:utf-8 *_*
#
import os
import random
import threading  # Python主要通过标准库中的threading包来实现多线程
import time

import requests
import schedule

from constant import PARAMS_MASK


def doChore():  # 作为间隔  每次调用间隔0.5s
    time.sleep(0.5)


user_agent_list = [
    'Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 MicroMessenger/7.0.10.1580(0x27000A5E) Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm64',
    'Mozilla/5.0 (Windows NT 6.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1464.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.16 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.3319.102 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.93 Safari/537.36',
    'Mozilla/5.0 (Windows NT 6.2; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/32.0.1667.0 Safari/537.36',
    'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0) Gecko/20100101 Firefox/17.0.6',
    'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2224.3 Safari/537.36',
    'Mozilla/5.0 (X11; CrOS i686 3912.101.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/27.0.1453.116 Safari/537.36']

header = {
    'Host': 'xcxb.aiyichuan.com',
    'Connection': 'keep-alive',
    'accept': 'application/json',
    'cookie': 'session_key=88fcff2cc94fb5e8e4a619366eaade5c;version=2;fenxiaoid=72458;beta=0;lat=34.00525;lng=119.38845;',
    'charset': 'utf-8',
    'content-type': 'application/x-www-form-urlencoded',
    'Content-Length': '0',
    'User-Agent': random.choice(user_agent_list),
    'Accept-Encoding': 'gzip',
    'Referer': 'https://servicewechat.com/wxc3a015f485d3e947/17/page-frame.html'
}

i = 1  # 限购数量

lock = threading.Lock()  # 创建锁

order_url = 'https://xcxb.aiyichuan.com/wxapp/v1.Act/add_order'  # POST

session = requests.session()


def booth(tid):
    global i
    global lock
    while True:
        lock.acquire()  # 得到一个锁，锁定
        if i != 0:
            response = session.post(url=order_url, params=PARAMS_MASK, headers=header)
            data = response.json()
            code = data['errcode']
            msg = data['errmsg']

            if code == 1000:
                i = i - 1
                data = data['data']
                order_id = data['order_id']
                print('您已成功下单，订单号：{}，请尽快付款，5分钟内完成交易'.format(order_id))
                time.sleep(10)  # 此处必须休眠10秒，否则下单失败

            print(msg)
        else:
            print('完成抢单')
            os._exit(0)  # 退出程序
        lock.release()  # 释放锁
        # doChore()

    # Start of the main function


def buy_something():
    # 总共设置了10个线程
    for k in range(5):
        new_thread = threading.Thread(target=booth, args=(k,))  # 创建线程; Python使用threading.Thread对象来代表线程
        new_thread.start()  # 调用start()方法启动线程


if __name__ == '__main__':

    print('===================开启定时任务===================')

    schedule.every().day.at('11:30').do(buy_something)  # 11:30 准时开抢
    schedule.every().day.at('14:00').do(buy_something)  # 14:00 准时开抢
    schedule.every().day.at('16:00').do(buy_something)  # 16:00 准时开抢
    schedule.every().day.at('18:00').do(buy_something)  # 18:00 准时开抢

    while True:
        schedule.run_pending()

    print('===================关闭定时任务===================')
