import submit_main
import TelethonSendMessage
import time
import requests
import json
import codecs
import random
import os
from selectolax.parser import HTMLParser
import asyncio



submitMain = submit_main.submitMain()
TelethonSendMessage = TelethonSendMessage.TelethonSendMessage()

while True :

    try:
        admin_host = 'https://91m.live/trump_peerc_channel_implement'
        params = {}
        params['req_ip'] = '64.188.16.166'
        # params['desc'] = '黑金'
        res = requests.post(url=admin_host, data=params)
        res = json.loads(res.text)
    except Exception as e:
        print("爬取后台数据错误：" + str(e))




    ua_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0',
        'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; WOW64; Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; .NET4.0C; InfoPath.3)',
    ]

    # print(res['data'])
    if len(res['data']) == 0:
        print('tasks 空')
        time.sleep(10)
        continue

    channelVerify_list = []

    for x in res['data']:
        time.sleep(1)
        if 'joined_channel' == x['send_type']:

            for channel in x['channel']:
                x['channel'] = channel
                try:
                    loop = asyncio.new_event_loop()
                    asyncio.set_event_loop(loop)
                    result = loop.run_until_complete(TelethonSendMessage.send_message(x))
                    print(result)
                except Exception as e:
                    print("send_message错误：" + str(e))


        if 'joinChannel' == x['send_type']:
            try:
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                result = loop.run_until_complete(TelethonSendMessage.join_channel(x))
                print(result)
            except Exception as e:
                print("joinChannel错误：" + str(e))


        try:

            if 'replyclient' == x['send_type']:
                ua_son = random.choice(ua_list)
                replyclient = submitMain.replyclient(res, x, ua_son)


            if 'savedialogpush' ==  x['send_type']:
                ua_son = random.choice(ua_list)
                replyclient = submitMain.savedialogpush(res, x, ua_son)

            if 'update_profile' == x['send_type']:
                ua_son = random.choice(ua_list)
                updateProfile = submitMain.updateProfile(res, x, ua_son)

        except Exception as e:

            print(str(e))

    # time.sleep(1)






