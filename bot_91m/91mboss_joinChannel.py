import asyncio
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
import os
import random
import time
import uuid
import time
import codecs
import re


session_number=[]
confing = {
    "admin":"40",
    "sleep_time":1,
}

import TelethonSendMessage
TelethonSendMessage = TelethonSendMessage.TelethonSendMessage()

async def get_session_number():
    for file in os.listdir("session"):
        file_name = str(file)

        if file_name.find('.session') != -1:
            file_name = re.sub(".session", "", file_name)
            file_name = re.sub("-journal", "", file_name)
            if str(file_name).find('-journal') != -1:
                os.remove(str(file))
                continue
            session_number.append(file_name)
    return True

async def get_channel():
    f = open("data/channel.txt", encoding="utf-8")
    channel = f.read()
    f.close()
    return channel

async def main():
    await get_session_number()

    channel_list = await get_channel()
    channel_list = channel_list.split("\n")


    for session in session_number:
        # print(session)
        count_channel = len(channel_list)
        random.shuffle(channel_list)
        if count_channel < 1 :
            break
        data = {
            'session_string':session,
            'channel':list.pop(channel_list),
            'admin':confing['admin'],
            # 'channel':random.choice(channel_list),
        }
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(TelethonSendMessage.send_message(data))
        print(result)
        # print(data)
        time.sleep(confing['sleep_time'])
    # print(len(channel_list))


    print('加群完成')

asyncio.get_event_loop().run_until_complete(main())