# *_*coding:utf-8 *_*
#
import os
import random
import threading  # Python主要通过标准库中的threading包来实现多线程
import time
from typing import Dict

import requests

from constant import PARAMS_MASK
from utils import find_path


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
    'cookie': 'session_key=da24f430a4ac6e25d38f19604e9f3b2c;version=2;fenxiaoid=72458;beta=0;lat=34.00545;lng=119.38945;',
    'charset': 'utf-8',
    'content-type': 'application/x-www-form-urlencoded',
    'Content-Length': '0',
    'User-Agent': random.choice(user_agent_list),
    'Accept-Encoding': 'gzip',
    'Referer': 'https://servicewechat.com/wxc3a015f485d3e947/17/page-frame.html'
}

i = 1  # 限购数量

lock = threading.Lock()  # 创建锁

url = 'https://xcxb.aiyichuan.com/wxapp/v1.Act/index?scene=1089'
act_info_url = 'https://xcxb.aiyichuan.com/wxapp/v1.Act/act_info'  # GET
order_url = 'https://xcxb.aiyichuan.com/wxapp/v1.Act/add_order'  # POST

shop_id, mask_id, mask_name, flag = -1, -1, '', False

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
                print('code: {}, 您已成功下单，订单号：{}，请尽快付款，5分钟内完成交易'.format(code, order_id))
                time.sleep(10)  # 此处必须休眠10秒，否则下单失败

            print('code: {}, msg: {}'.format(code, msg))
        else:
            print('完成抢单')
            os._exit(0)  # 退出程序
        lock.release()  # 释放锁
        # doChore()

    # Start of the main function


def get_mask_info() -> bool:
    global shop_id, mask_id, mask_name, url, act_info_url, flag

    response = session.get(url=url, headers=header)

    data: Dict = response.json()

    print(data)

    man = find_path(data)
    user_data = data['data']['userinfo']

    print(user_data)
    mask_paths = man.in_value_path('口罩')
    mask_path = mask_paths[0][:-len('[link_name]') - 2] # 南通市区
    # mask_path = mask_paths[1][:-len('[link_name]') - 2] # 南通通州
    # mask_path = mask_paths[2][:-len('[link_name]') - 2] # 南通海门
    shiqu_mask = eval('data' + mask_path)
    mask_id = shiqu_mask['params']['id']
    mask_name = shiqu_mask['link_name']  # default value

    if '口罩' in mask_name:
        act_info_url = act_info_url + '?fid=' + str(mask_id) + '&share_uid=&coupon_uid='
        response = session.get(url=act_info_url, headers=header)
        data = response.json()
        for i, shop in enumerate(data['data']['get_all_price']['attr']):
            print('id：{}, {}, 库存：{}, 价格：{}, 限购：{}'.format(shop['id'], shop['name'], shop['kucun'],
                                                          shop['show_price'], shop['xiangou_num']))
            if '唐闸' in shop['name']: # 这里注意修改 就是你线下要去领取的药店的名称 部分名称和完整名称都可以 主要是用来判断获取shop_id
                shop_id = shop['id']
                PARAMS_MASK['goods_attr_id'] = shop_id
                PARAMS_MASK['fid'] = mask_id
                flag = True
    print('shop id: {}, mask id: {}, mask name: {}'.format(shop_id, mask_id, str(mask_name)))
    return flag


def buy_something():
    flag: bool = get_mask_info()
    while (not flag):
        flag = get_mask_info()

    print(PARAMS_MASK)
    # 如果你已经提前知道这两个属性的信息 那么你可以将上面的代码注释掉 并且反注释下面的两行代码 能够加快速度
    # PARAMS_MASK['goods_attr_id'] = 883
    # PARAMS_MASK['fid'] = 1950
    for k in range(5):
        new_thread = threading.Thread(target=booth, args=(k,))  # 创建线程; Python使用threading.Thread对象来代表线程
        new_thread.start()  # 调用start()方法启动线程


if __name__ == '__main__':
    buy_something()
    # # print('===================开启定时任务===================')
    # #
    # print('\n任务计划 === >')
    # print("\
    #          11: 30 准时开抢 \n \
    #         14: 00 准时开抢 \n \
    #         16: 00 准时开抢 \n \
    #         18: 00 准时开抢")
    #
    # # schedule.every().day.at('13:00').do(buy_something)  # 11:30 准时开抢
    # schedule.every().day.at('11:30').do(buy_something)  # 11:30 准时开抢
    # # schedule.every().day.at('14:00').do(buy_something)  # 14:00 准时开抢
    # # schedule.every().day.at('15:59').do(buy_something)  # 16:00 准时开抢
    # # schedule.every().day.at('18:00').do(buy_something)  # 18:00 准时开抢
    #
    # while True:
    #     schedule.run_pending()
    #
    # print('===================关闭定时任务===================')
