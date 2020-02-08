# *_*coding:utf-8 *_*
#
import json
from typing import Dict, List

import requests

user_agent_list = [
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
    'cookie': 'session_key=cf3ae4384b395557997080997d4070e9;version=2;fenxiaoid=72458;beta=0;lat=34.00545;lng=119.38945;',
    'charset': 'utf-8',
    'content-type': 'application/x-www-form-urlencoded',
    'Content-Length': '0',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 5.1.1; vivo X7 Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/39.0.0.0 Mobile Safari/537.36 MicroMessenger/7.0.10.1580(0x27000A5E) Process/appbrand0 NetType/WIFI Language/zh_CN ABI/arm64',
    'Accept-Encoding': 'gzip',
    'Referer': 'https://servicewechat.com/wxc3a015f485d3e947/17/page-frame.html'
}

url = 'https://xcxb.aiyichuan.com/wxapp/v1.Act/index?scene=1089'

act_info_url = 'https://xcxb.aiyichuan.com/wxapp/v1.Act/act_info?fid=1850&share_uid=&coupon_uid='  # GET

reply_url = 'https://xcxb.aiyichuan.com/wxapp/v1.Act/get_ajax_reply?fid=1850'  # GET

act_buy_url = 'https://xcxb.aiyichuan.com/wxapp/v1.Act/act_buy'  # POST

order_url = 'https://xcxb.aiyichuan.com/wxapp/v1.Act/add_order'  # POST

session = requests.session()

response = session.get(url=url, headers=header)

data: Dict = json.loads(response.text)

data = data['data']

user_data = data['userinfo']

data: List = data['forech_template']

mask_data = data[1]

mask_list_data = mask_data['ad_list'][0]['new_link']

shop_id = 653  # 653 the shop id is default value --  653
mask_id = mask_list_data['params']['id']  # 1850 the mask id is default value --  1850
mask_name = mask_list_data['link_name']  # default value

print('shop id: {}, mask id: {}, mask name: {}'.format(shop_id, mask_id, str(mask_name)))

print(user_data)

response = session.get(url=act_info_url, headers=header)

print(response.json())

response = session.get(url=reply_url, headers=header)

print(response.json())

# response = session.post(url=act_buy_url, headers=header)
#
# print(response.json())
#
# params = {
#     'goods_attr_id': '653',
#     'num': '1',
#     'author': '徐嘉伟',
#     'tel': '18100695026',
#     'fid': '1850',
#     'group_id': '0',
#     'price': '7.50'
# }
#
# response = session.post(url=order_url, params=params, headers=header)
#
# print(response.json())
