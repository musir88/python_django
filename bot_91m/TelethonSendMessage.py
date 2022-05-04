from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import LeaveChannelRequest
from telethon.tl.functions.channels import JoinChannelRequest
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.messages import ImportChatInviteRequest
import webbrowser
import asyncio
import time
import json
import codecs
from datetime import date, timedelta
import random
import string
import requests
import sys
import os
import shutil
import socks
from faker import Faker
from selectolax.parser import HTMLParser
import re

class TelethonSendMessage:

    def proxy_set(self):
        proxy = [
            {'host': '216.185.47.218', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
            {'host': '50.114.107.228', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
            {'host': '50.114.107.105', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
            {'host': '216.185.46.220', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
            {'host': '154.16.150.211', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
            {'host': '50.114.107.226', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
            {'host': '50.114.107.104', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
            {'host': '216.185.46.23', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
            {'host': '50.114.107.223', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
            {'host': '216.185.46.28', 'port': '49161', 'username': 'tigerfpv', 'password': 'V4LEgUcmy7'},
        ]
        return random.choice(proxy)

    def client_init2(self, result):
        proxy_param = self.proxy_set()
        proxy = (
        socks.SOCKS5, proxy_param['host'], proxy_param['port'], proxy_param['username'], proxy_param['password'])
        # print("client_init2:" + str(proxy_param))
        return TelegramClient('session/' + result['phone'], 18252973, '7996fe1f8cd8223ddbca884fccdfa880', proxy=proxy)

    async def telethonErrorMessage(self, result={}, e='', code=1000):
        result['code'] = code
        # result['status'] = False
        result['messageEnglish'] = str(e)
        if str(e).find('The user has been deleted/deactivated') != -1:

            result['message'] = 'USER_DEACTIVATED_BAN'
            result['messageChinese'] = '用户已被删除/停用'
            path = "session/supok/" + result['phone'] + ".session"

            await self.removesessionNumber(result['phone'])
            await self.noticeAdmin(result)

        if str(e).find('The used phone number has been banned from Telegram and cannot be used anymore') != -1:
            # del result['messageEnglish']
            result['message'] = 'USER_DEACTIVATED_BAN'
            result['messageChinese'] = '用户已被官方禁用'
            await self.removesessionNumber(result['phone'])
            await self.noticeAdmin(result)

        if str(e).find('The key is not registered in the system (caused by ResolveUsernameRequest)') != -1:
            # del result['messageEnglish']
            result['message'] = 'USER_DEACTIVATED_BAN'
            result['messageChinese'] = '用户已被官方禁用'
            await self.removesessionNumber(result['phone'])
            await self.noticeAdmin(result)

        if str(e).find("You're banned from sending messages in supergroups/channels") != -1:
            # del result['messageEnglish']
            result['message'] = 'USER_BANNED_IN_CHANNEL'
            result['messageChinese'] = '用户已被官方禁止公开发言'
            await self.noticeAdmin(result, 'USER_BANNED_IN_CHANNEL')


        if str(e).find("You can't write in this chat") !=-1:
            # del result['messageEnglish']
            result['message'] = 'CHANNEL_MUTE'
            result['messageChinese'] = '群组禁言'

        if str(e).find("The channel specified is private and you lack permission to access it. Another reason may be that you were banned from it") != -1:
            # del result['messageEnglish']
            result['message'] = 'CHANNEL_MUTE_ACCESS'
            result['messageChinese'] = '群组禁止访问'


        fo = codecs.open("error_log/"+ result['admin'] + "-" + str(date.today()) + ".txt", "a", 'utf-8')
        fo.write("\n" + str(result))
        fo.close()

        # del result['messageEnglish']

        # print(result)
        return result

    async def noticeAdmin(self,result, message='USER_DEACTIVATED_BAN'):
        notice_admin = {};
        notice_admin['telegram_id'] = ''
        notice_admin['channel'] = ''
        notice_admin['version'] = '--'
        notice_admin['send_type'] = '--'
        notice_admin['date'] = '--'
        notice_admin['phone'] = result['phone']
        notice_admin['result'] = message
        return requests.post(url='http://91m.live/swoole/telegramapi_task_eXecl_result', data=notice_admin)

    def NOVERIFY_CHANNEL(self, content, admin=''):
        fo = codecs.open("NOVERIFY_CHANNEL/" + str(admin) + "→" + str(date.today()) + ".txt", "a", 'utf-8')
        fo.write("\n" + content)
        fo.close()

    def boturl_log(self, content, admin=''):
        fo = codecs.open("boturl_log/" + str(admin) + ".txt", "a", 'utf-8')
        fo.write("\n" + content)
        fo.close()


    async def removesessionNumber(self, phone):

        path = "config/" + phone + ".txt"
        if os.path.exists(path) == True:
            os.remove(path)

        path = "session/supok/" + phone + ".session"
        if os.path.exists(path) == True:
            os.remove(path)

        path = "session/" + phone + ".session"
        if os.path.exists(path) == True:
            os.remove(path)

    async def noticeAdmin(self, result, message='USER_DEACTIVATED_BAN'):
        notice_admin = {};
        notice_admin['telegram_id'] = ''
        notice_admin['channel'] = ''
        notice_admin['version'] = '--'
        notice_admin['send_type'] = '--'
        notice_admin['date'] = '--'
        notice_admin['phone'] = result['phone']
        notice_admin['result'] = message
        return requests.post(url='http://91m.live/swoole/telegramapi_task_eXecl_result', data=notice_admin)

    def send_log(self, content, admin=''):
        fo = codecs.open("send_log/" + str(admin) + "→" + str(date.today()) + ".txt", "a", 'utf-8')
        fo.write("\n" + content)
        fo.close()

    def verifychannellog(self, content, admin=''):
        fo = codecs.open("验证CHANNEL/" + str(admin) + "→" + str(date.today()) + ".txt", "a", 'utf-8')
        fo.write("\n" + content)
        fo.close()




    async def send_message(self, data):
        phone = data['session_string']
        channel = data['channel']
        content = data['content']

        if 'admin_id' in data:
            admin_id = data['admin_id']

        if 'admin' in data:
            admin_id = data['admin']

        if 'is_fake_content' not in data:
            data['is_fake_content'] = 2
        admin_id = str(admin_id)

        result = {}
        result['phone'] = phone
        result['channel'] = channel
        result['admin'] = admin_id
        result['submit'] = 'send_message'

        is_fake_content =data['is_fake_content']
        if is_fake_content == '1':
            fake_content = data['fake_content']
            send_content = fake_content
        else:
            send_content = content

        result['is_fake_content'] = is_fake_content
        #
        try:
            client = self.client_init2(result)
            await client.connect()
        except Exception as e:
            await client.disconnect()
            result = await self.telethonErrorMessage(result, e, 1008)
            # print(result)
            # del result['status']
            return json.dumps(result, ensure_ascii=False)

        try:
            await client.send_message(channel, send_content)
        except Exception as e:

            del result['is_fake_content']

            if str(e).find("Chat admin privileges are required to do that in the specified chat") != -1:
                await client(LeaveChannelRequest(channel))

            if str(e).find("You can't write in this chat") != -1:
                await client(LeaveChannelRequest(channel))

            await client.disconnect()
            result = await self.telethonErrorMessage(result, e, 10010)
            # del result['status']
            return json.dumps(result, ensure_ascii=False)

        # 如果不是伪内容 直接记录发送日志
        if is_fake_content == '1':

            send_log_cnotent = phone + " → " + channel + " → " + send_content
            self.send_log(send_log_cnotent)

            get_me = await client.get_me()
            photos = await client.get_messages(channel, 10)
            for x in photos:
                # print(x.from_id)
                # print(x.from_id.user_id)
                if x.text == send_content and x.from_id.user_id == get_me.id:
                    edit_message = {
                        'session_string': phone,
                        'channel': channel,
                        'msg_id': x.id,
                        'content': content,
                        'fake_content_sleep': time.time(),
                    }
                    result['edit_message'] = edit_message
                    continue
                    # await client.edit_message(channel, x.id, '【 接中！】')
                # print(x.text)

        else:
            # 记录发送日志
            send_log_cnotent = phone + " → " + channel + " → " + send_content
            self.send_log(send_log_cnotent, admin_id)

        result['status'] = True
        await client.disconnect()
        return json.dumps(result, ensure_ascii=False)
        # return True

    async def join_channel(self, data):
        result = {};
        phone = data['session_string']
        channel = data['channel']

        if 'admin' in data:
            admin = data['admin']
        if 'admin_id' in data:
            admin = data['admin_id']
        admin = str(admin)

        result['channel'] = channel
        result['phone'] = phone
        result['admin'] = admin

        try:
            client = self.client_init2(result)
            await client.connect()
        except Exception as e:
            await client.disconnect()
            result = await self.telethonErrorMessage(result, e)
            return json.dumps(result, ensure_ascii=False)


        # try:
        #     # await client.send_message("https://t.me/policr_mini_bot/start/erification_v1_-1001102358104", "/start")
        #     # await client.send_message("https://t.me/policr_mini_bot/start=verification_v1_-1001102358104", "/start")
        #     username = await client.get_entity('https://t.me/policr_mini_bot/start=verification_v1_-1001102358104')
        #     print(username)
        # except Exception as e:
        #     await client.disconnect()
        #     result = await self.telethonErrorMessage(result, e, 'send_message')
        #     return json.dumps(result, ensure_ascii=False)


        try:
            await client(JoinChannelRequest(channel))
            result['status'] = True
        except Exception as e:
            await client.disconnect()
            result = await self.telethonErrorMessage(result, e, 'JoinChannelRequest')
            return json.dumps(result, ensure_ascii=False)

        send_log_cnotent = phone + " → " + channel + " → 加群"
        self.send_log(send_log_cnotent, admin)
        # print(send_log_cnotent)

        await asyncio.sleep(2)

        is_VERIFY = False


        try:
            photos = await client.get_messages(channel, 30)
        except Exception as e:
            await client.disconnect()
            result = await self.telethonErrorMessage(result, e, 'get_channelmessages')
            return json.dumps(result, ensure_ascii=False)

        # try:
        for x in photos:
            if hasattr(x, 'reply_markup') == True and x.reply_markup != None and x.mentioned == True:
                # print(x.message)
                # 记录日志
                # 验证CHANNEL
                send_log_cnotent = phone + " → " + channel + "\n" + x.message + "\n"
                self.verifychannellog(send_log_cnotent, admin)

                is_VERIFY = True

                print("==============")
                print(len(x.reply_markup.rows))
                print(x.reply_markup.rows)
                print("==============")

                print(1)
                if len(x.reply_markup.rows) == 1:
                    result['verify'] = True
                    print(2)
                    # asyncio.create_task(x.click(0))
                    # time.sleep(1)
                    # print(str(x.reply_markup.rows[0].buttons[0]) + " → " + channel)
                    # print(str(x.reply_markup.rows[0].buttons[0].data) + " → " + channel)
                    # await x.click(0)

                    print(x.message)

                    if hasattr(x.reply_markup.rows[0].buttons[0], 'url') == True:
                        bot_url = x.reply_markup.rows[0].buttons[0].url
                        # print(bot_url)
                        print(str(x.reply_markup.rows[0].buttons[0]) + " → " + channel + " → " + phone)
                        # await x.click(x.reply_markup.rows[0].buttons[0].text)
                        # await x.click(bot_url)
                        # await client(ImportChatInviteRequest(bot_url))
                        # await client.send_message('@policr_mini_bot', "/start")




                        if str(bot_url).find("?") != -1:
                            self.boturl_log(str(bot_url) + " → " + channel+ " → " + phone, admin)

                            boturl_array = str(bot_url).split("?")
                            # print(boturl_array[0])
                            print(boturl_array)

                            Order = re.sub("=", " ", boturl_array[1])

                            # await client.send_message(boturl_array[0], bot_url)
                            # await client.send_message(boturl_array[0], bot_url)
                            # webbrowser.open("tg://resolve?domain=policr_mini_bot&start=verification_v1_-1001354379829")
                            # requests.get("https://my.telegram.org?domain=policr_mini_bot&start=verification_v1_-1001354379829")
                            # webbrowser.open("https://my.telegram.org?domain=policr_mini_bot&start=verification_v1_-1001354379829")


                            # await client.send_message(boturl_array[0], '/start '+str(bot_url).split("start=")[1])

                            try:
                                await client.send_message(boturl_array[0], "/"+Order)
                            except Exception as e:
                                await client.disconnect()
                                result = await self.telethonErrorMessage(result, e, 'channel多步验证开始发送命令 ①')
                                return json.dumps(result, ensure_ascii=False)

                            try:
                                await asyncio.sleep(2)
                                bot_message = await client.get_messages(boturl_array[0], 3)
                            except Exception as e:
                                await client.disconnect()
                                result = await self.telethonErrorMessage(result, e, 'channel多步验证 ②')
                                return json.dumps(result, ensure_ascii=False)



                            # print(bot_message)



                            for botphotos_x in bot_message:

                                print(botphotos_x.message)

                                # 针对个别群破解
                                if str(botphotos_x.message).find('那条河流是在湖南境内的') != -1:
                                    try:
                                        print('==================')
                                        print(botphotos_x)
                                        print('==================')
                                        print(botphotos_x.reply_markup)
                                        print('==================')
                                        print(botphotos_x.reply_markup.rows)
                                        print(botphotos_x.reply_markup['rows'])
                                        print('==================')
                                        # for bottons_key,bottons_son in botphotos_x.reply_markup.rows:
                                        #
                                            # print(bottons_son)
                                        #     print(bottons_son)
                                        #     print(bottons_son.text)
                                    except Exception as e:
                                        await client.disconnect()
                                        result = await self.telethonErrorMessage(result, e, 'channel多步验证 ③')
                                        return json.dumps(result, ensure_ascii=False)

                            # 针
                            # for bottons_key,bottons_son in botphotos_x.reply_markup.row:
                            #     print(bottons_key)
                            #     print(bottons_son)


                            #     print(botphotos_x.message)
                            # #     print(botphotos_x.media)
                            #     if hasattr(botphotos_x,'reply_markup') == True and botphotos_x.reply_markup != None:
                            # #         # print(len(botphotos_x.reply_markup.rows))
                            # #         print(botphotos_x.reply_markup.rows)
                            #         if str(botphotos_x.message).find('那条河流是在湖南境内的') != -1 :
                            #             for bottons_son_idx, bottons_son in botphotos_x.reply_markup:
                            #                 if str(bottons_son.text).find('浏阳河') != -1:
                            #                     print(str(bottons_son))
                            #         # await x.click(bottons_son_idx)
                            #         break



                        # await x.click(0)

                        # https: // t.me / +nncvrweqRs44Y2Yx
                        # KeyboardButtonUrl(text='前往验证', url='https://t.me/+nncvrweqRs44Y2Yx') → https: // t.me / hugoblog

                        send_log_cnotent = phone + " → " + channel + "\n bot_url:" + bot_url + "\n"
                        self.verifychannellog(send_log_cnotent, admin)
                    else:
                        print(str(x.reply_markup.rows[0].buttons[0]) + " → " + channel+ " → " + phone)
                        await x.click(0)


                    # await client.send_message('@lzh2020', str(x.reply_markup.rows[0].buttons[0].text)+" → "+channel)
                    print(3)
                    break

                if len(x.reply_markup.rows) > 1:
                    # print(str(x.reply_markup.rows))
                    # print(x.message)

                    try:
                        if str(x.message).find("请按顺序点击") != -1:
                            message = str(x.message)
                            message = message.split("\n")
                            message = message.pop()

                            message = re.sub("（", "(", message)
                            message = re.sub("）", ")", message)
                            message = re.findall(r'[(](.*?)[)]', message)[0]
                            message = message.split("、")
                            # print(message)
                            for row_idx,row in x.reply_markup.rows:
                                for bottons in row.buttons:
                                    for son_idx, son in message:
                                        if son == bottons.text:
                                            result['verify'] = True
                                            print(str(bottons.text) + " → " + channel)
                                            # asyncio.create_task(x.click(bottons.data))
                                            await asyncio.sleep(1)
                                            print(row_idx)
                                            print(son_idx)
                                            await x.click(row_idx, son_idx)
                                            # await x.click(bottons.data)
                    except Exception as e:
                        await client.disconnect()
                        result = await self.telethonErrorMessage(result, e, '请按顺序点击-no')
                        return json.dumps(result, ensure_ascii=False)


                if is_VERIFY == False:
                    # NOVERIFY_CHANNEL
                    send_log_cnotent = channel
                    self.NOVERIFY_CHANNEL(send_log_cnotent, admin)

        # except Exception as e:
        #     await client.disconnect()
        #     result = await self.telethonErrorMessage(result, e, 'click-no')
        #     return json.dumps(result, ensure_ascii=False)

        await client.disconnect()
        result['submit'] = 'join_channel'
        return json.dumps(result, ensure_ascii=False)


    async def ImportChatInviteRequest(self, data):
        result = {};
        phone = data['session_string']
        channel = data['channel']

        if 'admin' in data:
            admin = data['admin']
        if 'admin_id' in data:
            admin = data['admin_id']
        admin = str(admin)

        result['channel'] = channel
        result['phone'] = phone
        result['admin'] = admin

        try:
            client = self.client_init2(result)
            await client.connect()
        except Exception as e:
            await client.disconnect()
            result = await self.telethonErrorMessage(result, e)
            return json.dumps(result, ensure_ascii=False)

        try:
            updates = await client(ImportChatInviteRequest('ilY7WUw4Vf02NWU1'))
        except Exception as e:
            await client.disconnect()
            result = await self.telethonErrorMessage(result, e, 'ImportChatInviteRequest')
            return json.dumps(result, ensure_ascii=False)

        result['submit'] = 'join_channel'
        return json.dumps(result, ensure_ascii=False)