# *_*coding:utf-8 *_*
#

import requests

from constant import PARAMS_MASK

header = {
    'Host': 'xcxb.aiyichuan.com',
    'Connection': 'keep-alive',
    'accept': 'application/json',
    'cookie': 'session_key=88fcff2cc94fb5e8e4a619366eaade5c;version=2;fenxiaoid=72458;beta=0;lat=34.00525;lng=119.38845;',
    'charset': 'utf-8',
    'content-type': 'application/x-www-form-urlencoded',
    'Content-Length': '0',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 MicroMessenger/7.0.10.1580(0x27000A5E) Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm64',
    'Accept-Encoding': 'gzip',
    'Referer': 'https://servicewechat.com/wxc3a015f485d3e947/17/page-frame.html'
}

order_url = 'https://xcxb.aiyichuan.com/wxapp/v1.Act/add_order'  # POST

session = requests.session()

while True:
    response = session.post(url=order_url, params=PARAMS_MASK, headers=header)

    data = response.json()
    code = data['errcode']
    msg = data['errmsg']

    if code == 1000:
        data = data['data']
        order_id = data['order_id']
        print('您已成功下单，订单号：{}，请尽快付款，5分钟内完成交易'.format(order_id))
        break

    print(msg)
