import requests
import json
import codecs
import random
from django.http import JsonResponse
import os
import django
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'dailyfresh.settings')
django.setup()




# admin_host = 'https://91m.live/trump_peerc_channel_implement'
# params = {}
# params['req_ip'] = '66.63.177.210'
# params['desc'] = '黑金 - joinChannel'
# res = requests.post(url=admin_host, data=params)
#
# print(params)
# print(json.loads(res.text))
# res = json.loads(res.text)
# print(res['data'])
# print(res['domain_name'])

headers={
  "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
  "Accept-Encoding": "gzip, deflate, br",
  "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
  "Connection":"keep-alive",
  "Host":  "36kr.com/newsflashes",
  "Upgrade-Insecure-Requests":"1",
  "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.13; rv:55.0) Gecko/20100101 Firefox/55.0"
}

headers = {
    'Content-type': 'application/json',
}

ua_list = [
    'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
    'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
    'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
]
param_son = {}
param_son['channel'] = 'YPATT'
param_son['session_string'] = '5511965342321'

response = requests.get('http://localhost:8888/boss91m/join_channel', headers={'User-Agent': random.choice(ua_list)})


# bot_url = "http://localhost:8888/boss91m/join_channel"
#
# res_son = requests.get(url=bot_url, data=param_son, headers=headers)
print(JsonResponse(response.text, safe=False))

# for x in res['data']:
#     bot_url = res['domain_name'] + "boss91m/join_channel"
#
#     param_son = {}
#     param_son['channel'] = x['channel']
#     param_son['session_string'] = x['session_string']
#
#     res_son = requests.get(url=bot_url, data=param_son)
#     print(bot_url)
#     print(x['channel'])
#     print(x['session_string'])
#
#     print(res_son.text)



