from django.shortcuts import render
from django.http import HttpResponse
from telethon import TelegramClient, events
from telethon.tl.functions.channels import JoinChannelRequest
import asyncio
import time
import json
import codecs
from datetime import date, timedelta
import random
import string
from telethon.tl.functions.account import UpdateUsernameRequest
import requests
import sys
import os
import shutil
from telethon.tl.functions.channels import JoinChannelRequest
import socks
from faker import Faker
from selectolax.parser import HTMLParser
from telethon.tl.functions.account import UpdateUsernameRequest
from telethon.tl.functions.account import UpdateProfileRequest
from telethon.tl.functions.channels import LeaveChannelRequest
import re

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def client_init(result):
    proxy_param = proxy_set()
    # proxy = (socks.HTTP, proxy_param['host'], proxy_param['port'], proxy_param['username'], proxy_param['password'])
    proxy = (socks.SOCKS5, proxy_param['host'], proxy_param['port'], proxy_param['username'], proxy_param['password'])

    print("client_init:"+str(proxy_param))
    config = {}
    config['proxy'] = proxy
    config['api'] = {
        'api_id':int(result['api_id']),
        'api_hash':str(result['api_hash']),
    }
    fo = codecs.open("config/"+ str(result['phone']) +".txt", "a", 'utf-8')
    fo.write(str(config))
    fo.close()

    return TelegramClient('session/' + result['phone'], int(result['api_id']), result['api_hash'], proxy=proxy)

def client_init2(result):
    proxy_param = proxy_set()
    proxy = (socks.SOCKS5, proxy_param['host'], proxy_param['port'], proxy_param['username'], proxy_param['password'])
    # print("client_init2:" + str(proxy_param))
    return TelegramClient('session/' + result['phone'], 18252973, '7996fe1f8cd8223ddbca884fccdfa880', proxy=proxy)


def proxy_set():
    proxy = [
        {'host': '216.185.47.218', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '50.114.107.228', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '50.114.107.105', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '216.185.46.220', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '154.16.150.211', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '50.114.107.226', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '50.114.107.104', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '216.185.46.23', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '50.114.107.223', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
        {'host': '216.185.46.28', 'port': '49161', 'username':'tigerfpv', 'password':'V4LEgUcmy7'},
    ]
    return random.choice(proxy)



def verifychannellog(content, admin=''):
    fo = codecs.open("验证CHANNEL/"+ str(admin) + "→" + str(date.today()) +".txt", "a", 'utf-8')
    fo.write("\n"+content)
    fo.close()


def send_log(content, admin=''):
    fo = codecs.open("send_log/"+ str(admin) + "→" + str(date.today()) +".txt", "a", 'utf-8')
    fo.write("\n"+content)
    fo.close()


def NOVERIFY_CHANNEL(content, admin=''):
    fo = codecs.open("NOVERIFY_CHANNEL/"+ str(admin) + "→" + str(date.today()) +".txt", "a", 'utf-8')
    fo.write("\n"+content)
    fo.close()

async def login(request):
    phone = request.GET['session_string']
    client = TelegramClient('session/'+phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')



    await client.connect()

    client.disconnect()


    # in case of script ran first time it will
    # ask either to input token or otp sent to
    # number or sent or your telegram id

    sent = await client.send_code_request(phone=phone, force_sms=True)
    print(sent)
    code = input("请输入手机收到的验证码...\n")
    await client.sign_in(phone=phone, code=code)



    try:
        print(123)
        # receiver user_id and access_hash, use
        # my user_id and access_hash for reference
        # receiver = InputPeerUser('user_id', 'user_hash')

        # sending message using telegram client
        # client.send_message(receiver, message, parse_mode='html')
    except Exception as e:

        # there may be many error coming in while like peer
        # error, wrong access_hash, flood_error, etc
        print(e);

    # disconnecting the telegram session
    client.disconnect()


    return HttpResponse("Hello, world.login.")


async def send_Message(request):
    phone         = request.GET['session_string']
    channel         = request.GET['channel']
    content         = request.GET['content']
    admin_id         = request.GET['admin_id']

    result = {}
    result['phone'] = phone
    result['channel'] = channel
    result['admin_id'] = admin_id

    is_fake_content = request.GET['is_fake_content']
    if is_fake_content == '1':
        fake_content = request.GET['fake_content']
        send_content = fake_content
    else:
        send_content = content

    result['is_fake_content'] = is_fake_content


    try:
        # client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        client = client_init2(result)
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e,1008)
        return HttpResponse(json.dumps(result))


    try:
        await client.send_message(channel, send_content)
    except Exception as e:


        if str(e).find("Chat admin privileges are required to do that in the specified chat") != -1 :
            await client(LeaveChannelRequest(channel))

        if str(e).find("You can't write in this chat") != -1 :
            await client(LeaveChannelRequest(channel))

        await client.disconnect()
        result = await telethonErrorMessage(result, e,10010)
        return HttpResponse(json.dumps(result))



    #如果不是伪内容 直接记录发送日志
    if is_fake_content == '1':

        send_log_cnotent = phone + " → " + channel + " → " + send_content
        send_log(send_log_cnotent)

        get_me = await client.get_me()
        photos = await client.get_messages(channel, 10)
        for x in photos:
            # print(x.from_id)
            # print(x.from_id.user_id)
            if x.text == send_content and x.from_id.user_id == get_me.id:
                edit_message = {
                    'session_string':phone,
                    'channel':channel,
                    'msg_id':x.id,
                    'content':content,
                    'fake_content_sleep':time.time(),
                }
                result['edit_message'] = edit_message
                continue
                # await client.edit_message(channel, x.id, '【 接单中！】')
            # print(x.text)

    else:
        # 记录发送日志
        send_log_cnotent = phone + " → " + channel + " → " + send_content
        send_log(send_log_cnotent, admin_id)

    result['status'] = True

    await client.disconnect()
    return HttpResponse(json.dumps(result))


async def handler(update):
    if update.is_private:  # only auto-reply to private chats
        time.sleep(1)
        await update.respond('你好')
    print(update)


async def automatic_reply(request):
    phone = request.GET['session_string']
    # client = TelegramClient('session/'+phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
    # await client.start()

    async with TelegramClient('session/'+phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880') as client:
        # Register the update handler so that it gets called
        client.add_handle_new_message(handler)
        #
        # async def handle_new_message(event):
        #     if event.is_private:  # only auto-reply to private chats
        #         time.sleep(1)
        #         await event.respond('你好')


        # Run the client until Ctrl+C is pressed, or the client disconnects
        print('(Press Ctrl+C to stop this)')
        await client.run_until_disconnected()




    #
    # @client.on(events.NewMessage(incoming=True))
    # async def handle_new_message(event):
    #     if event.is_private:  # only auto-reply to private chats
    #         time.sleep(1)
    #         await event.respond('你好')
    # #     channel = 'lzh2020'
    # #     await client.send_message(channel, '登录成功')
    #
    # await client.disconnect()
    # client.run_until_disconnected()

    return HttpResponse("automatic_reply: "+phone+" 成功")


# 获取所有已加入的群
async def get_channel(request):

    result = {}
    phone = request.GET['session_string']
    result['phone'] = phone
    try:
        # client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        client = client_init2(result)
        await client.connect()

    except Exception as e:
        result = await telethonErrorMessage(result, e, 1009)
        await client.disconnect()
        return HttpResponse(json.dumps(result, ensure_ascii=False))

    try:
        channel = []
        async for dialog in client.iter_dialogs():
            if dialog.is_channel == True:
                channel_son = {
                    'id': dialog.id,
                    'name': dialog.name,
                    'username': dialog.entity.username,
                }
                channel.append(channel_son)
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e,1008)
        return HttpResponse(json.dumps(result, ensure_ascii=False))

    await client.disconnect()
    return HttpResponse(json.dumps({"status":True, "channel":channel}, ensure_ascii=False))


# 获取未读的用户的消息
async def chat_newmessage(request):
    phone = request.GET['session_string']

    result = {}
    result['phone'] = phone

    try:
        client = client_init2(result)
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e,10087)
        return HttpResponse(json.dumps(result, ensure_ascii=False))




# 获取验证码
async def getTelegramCode(request):

    result = {}
    phone = request.GET['session_string']
    result['phone'] = phone
    try:
        # client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        # client = client_init2(result)
        client = client_init2(result)
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e)
        return HttpResponse(json.dumps(result))


    try:
        photos = await client.get_messages(777000, 1)
        for x in photos:
            result['code'] = x.text
            continue
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e)
        return HttpResponse(json.dumps(result))

    await client.disconnect()
    return HttpResponse(result['code'])
    # return HttpResponse(json.dumps(result))


# 获取禁言信息
async def get_pubspeak_message(request):

    result = {}
    phone = request.GET['session_string']
    result['phone'] = phone

    # await time.sleep(2)
    # time.sleep(2)

    try:
        # client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        client = client_init2(result)
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e)
        return HttpResponse(json.dumps(result))
    try:
        photos = await client.get_messages('@SpamBot', 1)
        for x in photos:
            result['getHistory'] = x.text
            continue
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e)



        return HttpResponse(json.dumps(result))

    await client.disconnect()
    # return HttpResponse(result['code'])
    result['status'] = True
    # print(result)
    return HttpResponse(json.dumps(result))


async def removesessionNumber(phone):

    path = "config/" + phone + ".txt"
    if os.path.exists(path) == True:
        os.remove(path)

    path = "session/supok/" + phone + ".session"
    if os.path.exists(path) == True:
        os.remove(path)

    path = "session/" + phone + ".session"
    if os.path.exists(path) == True:
        os.remove(path)



async def telethonErrorMessage(result={}, e='', code=1000):
    result['code'] = code
    result['status'] = False
    result['messageEnglish'] = str(e)
    if str(e).find('The user has been deleted/deactivated') != -1:
        result['message'] = 'USER_DEACTIVATED_BAN'
        result['messageChinese'] = '用户已被删除/停用'
        path = "session/supok/" + result['phone'] + ".session"

        await removesessionNumber(result['phone'])
        await noticeAdmin(result)

    if str(e).find('The used phone number has been banned from Telegram and cannot be used anymore') != -1:
        result['message'] = 'USER_DEACTIVATED_BAN'
        result['messageChinese'] = '用户已被官方禁用'
        await removesessionNumber(result['phone'])
        await noticeAdmin(result)

    if str(e).find('The key is not registered in the system (caused by ResolveUsernameRequest)') != -1:
        result['message'] = 'USER_DEACTIVATED_BAN'
        result['messageChinese'] = '用户已被官方禁用'
        await removesessionNumber(result['phone'])
        await noticeAdmin(result)

    if str(e).find("You're banned from sending messages in supergroups/channels") != -1:
        result['message'] = 'USER_BANNED_IN_CHANNEL'
        result['messageChinese'] = '用户已被官方禁止公开发言'
        await noticeAdmin(result, 'USER_BANNED_IN_CHANNEL')



    fo = codecs.open("error_log/"+ str(date.today()) +".txt", "a", 'utf-8')
    fo.write("\n"+str(result))
    fo.close()


    # print(result)
    return result


async def noticeAdmin(result,message='USER_DEACTIVATED_BAN'):
    notice_admin = {};
    notice_admin['telegram_id'] = ''
    notice_admin['channel'] = ''
    notice_admin['version'] = '--'
    notice_admin['send_type'] = '--'
    notice_admin['date'] = '--'
    notice_admin['phone'] = result['phone']
    notice_admin['result'] = message
    return requests.post(url='http://91m.live/swoole/telegramapi_task_eXecl_result', data=notice_admin)


# 修改二次验证码
async def update2fa(request):
    result = {}
    phone = request.GET['session_string']

    try:
        client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        if not client.is_user_authorized():
            result['status'] = False
            result['message'] = '疑似未登录'
            result['phone'] = phone
            return HttpResponse(json.dumps(result))
        await client.start()
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
        return HttpResponse(json.dumps(result))

    try:
        await client.edit_2fa(new_password='91m123456')
    except Exception as e:
        await client.disconnect()
        result['status'] = False
        result['message'] = str(e)
        return HttpResponse(json.dumps(result))

    await client.disconnect()
    result['status'] = True
    return HttpResponse(json.dumps(result))


async def waste_number(phone='', tg_status=''):
    admin_host = 'https://91m.live/telegram_api/waste_number'
    params = {}
    params['phone'] = phone
    params['tg_status'] = tg_status
    res = requests.post(url=admin_host, data=params)
    print(res)

async def supstatus(phone='', supstatus=1):
    admin_host = 'https://91m.live/telegram_api/update_telegram_supstatus'
    params = {}
    params['phone'] = phone
    params['supstatus'] = supstatus
    res = requests.post(url=admin_host, data=params)
    print(res)


def suphtml(phone, api_id, api_hash):
    # html = '<form>phone:<input type="text" name="session_string" value="'+phone+'"><br>code:<input type="text" name="code" value=""><br><input type="text" name="submit_step" value="2" style="display:none;"><input type="submit" value="Submit"></form>'

    html_start = '<form>'
    html_input = 'api_id: <input type="text" name="api_id" id="api_id" value="'+ str(api_id) +'">'
    html_input = html_input + '<br>api_hash: <input type="text" name="api_hash" id="api_hash" value="'+api_hash+'">'
    html_input = html_input + '<br>phone: <input type="text" name="session_string" id="phone" value="'+phone+'">'
    html_input = html_input + '<br>code: <input type="text" name="code" id="code" value="">'
    html_input = html_input + '<br><input type="text" name="submit_step" id="submit_step" value="2" style="display:none;">'
    html_submit = '<br><input type="submit" value="Submit" id="submit">'
    html_stop = '</form>'
    html = html_start + html_input + html_submit + html_stop

    f = open('main_static/sup.html', 'r')
    html = html + f.read()
    f.close()

    return html



# 发送验证码
# @csrf_exempt
# @csrf_exempt
# @method_decorator(csrf_exempt, name='dispatch')
async def send_code_request(request):

    result = {}
    phone = request.GET['session_string']
    result['phone'] = phone

    result['api_id'] = request.GET['api_id']
    result['api_hash'] = request.GET['api_hash']

    # return HttpResponse('<script type="text/javascript">alert("你好");</script>')

    print(result)

    try:
        client = client_init(result)
        # client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        await client.connect()
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
        result['message_code'] = 1002
        # return render(request, "send_code_request.html", result)
        await telethonErrorMessage(result, e, 1002)
        return HttpResponse(json.dumps(result, ensure_ascii=False))

    try:
        await client.send_code_request(phone, force_sms=True)
        result['message'] = 'send code ok'

        # 通知后台该去获取验证码了
        await supstatus(phone, 2)

    except Exception as e:
        await client.disconnect()
        os.remove("session/"+phone+".session")

        result['status'] = False
        result['message'] = str(e)
        result['message_code'] = 1004
        time_start = time.time()
        await telethonErrorMessage(result, e, 1004)

        # 号被禁用
        if result['message'] == 'The used phone number has been banned from Telegram and cannot be used anymore. Maybe check https://www.telegram.org/faq_spam (caused by SendCodeRequest)' :
            await waste_number(phone, result['message'])
            return HttpResponse('<script>window.close();</script>')

        if result['message'] == 'The used phone number has been banned from Telegram and cannot be used anymore. Maybe check https://www.telegram.org/faq_spam (caused by SendCodeRequest)':
            await waste_number(phone, result['message'])
            return HttpResponse('<script>window.close();</script>')

        if result['message'].find("Two-steps verification is enabled and a password is required") != -1 :
            await waste_number(phone, result['message'])
            await removesessionNumber(result['phone'])
            return HttpResponse('<script>window.close();</script>')

        return HttpResponse(json.dumps(result, ensure_ascii=False))

    submit_step = request.GET['submit_step']
    # 接码成功 完善注册信息
    if submit_step == '2':
        try:
            first_name = ''.join(random.sample(['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f','e', 'd', 'c', 'b', 'a'], random.randint(3,6)))
            last_name = ''.join(random.sample(['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f','e', 'd', 'c', 'b', 'a'], random.randint(3,6)))
            fake = Faker("zh_CN")
            first_name = fake.name()
            last_name = fake.name()
            code = request.GET['code']
            await client.sign_up(code=code, first_name=first_name,last_name=last_name,phone=phone)
            await supstatus(phone, 3) # 通知后台号码注册成功了
        except Exception as e:
            await client.disconnect()
            # os.remove("session/" + phone + ".session")
            # await waste_number(phone, result['message'])

            await telethonErrorMessage(result, e, 1003)

            result['status'] = False
            result['message'] = str(e)
            result['message_code'] = 1003
            # return HttpResponse('<script>window.close();</script>')
            return HttpResponse(json.dumps(result))
            # return render(request, "send_code_request.html", result)

        # 设置二次验证码
        try:
            await client.edit_2fa(new_password='91m123456')
        except Exception as e:
            await client.disconnect()
            os.remove("session/" + phone + ".session")
            await waste_number(phone, result['message'])

            result['status'] = False
            result['message'] = str(e)
            result['message_code'] = 1006
            await telethonErrorMessage(result, e, 1006)
            return HttpResponse('<script>window.close();</script>')
            # return HttpResponse(json.dumps(result))
            # return render(request, "send_code_request.html", result)

        # 设置用户名
        try:
            username = ''.join(random.sample(['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g','f', 'e', 'd', 'c', 'b', 'a'], random.randint(8,15)))
            await client(UpdateUsernameRequest(username))
            result['username'] = username
        except Exception as e:
            await client.disconnect()
            await telethonErrorMessage(result, e, 1006)
            return HttpResponse('<script>window.close();</script>')
            # return HttpResponse(json.dumps(result))

        result['message'] = 'sign_up ok'

    await client.disconnect()

    if submit_step == '1':
        html = suphtml(phone,result['api_id'],  result['api_hash'])
        return HttpResponse(html)

    if submit_step == '2':
        shutil.copyfile("session/" + phone + ".session","session/supok/" + phone + ".session")
        await sign_up_ok(phone)

    result['submit_step'] = submit_step

    result['admin_host'] = ''
    # result['admin_host'] = 'http://91m.live/'

    # return render(request, "send_code_request.html", result)

    result['status'] = True
    return HttpResponse(json.dumps(result, ensure_ascii=False))


# 发送验证码
async def sign_up(request):
    result = {}
    phone = request.GET['session_string']
    code = request.GET['code']

    try:
        client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        await client.connect()
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
        return HttpResponse(json.dumps(result))

    try:
        await client.sign_up(code=code, first_name='io2022',last_name='l407',phone=phone)
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
        return HttpResponse(json.dumps(result))

    #
    # try:
    #     await client.edit_2fa(new_password='91m123456')
    # except Exception as e:
    #     await client.disconnect()
    #     result['status'] = False
    #     result['message'] = str(e)
    #     return HttpResponse(json.dumps(result))

    # await client.disconnect()
    result['status'] = True
    return HttpResponse(json.dumps(result))


async def get_sign_up(request):
    print(123)
    data = {};
    # data['phone'] = request.GET['phone']
    # admin_host = 'http://91m.live/telegram_api/get_login_code'
    #
    # res = requests.post(url=admin_host, data=data)
    # return HttpResponse(res)


async def sign_up_ok(phone):
    # print(123)
    data = {};
    data['phone'] = phone
    admin_host = 'http://91m.live/telegram_api/login_ok'

    res = requests.post(url=admin_host, data=data)
    return HttpResponse(res)


# 加入群组
async def join_channel(request):
    result = {};
    phone = request.GET.get('session_string', '')
    admin = request.GET.get('admin', '')
    channel = request.GET.get('channel', '')

    if phone == '':
        phone = request.POST.post('session_string', '')

    if channel == '':
        channel = request.POST.post('channel', '')

    if admin == '':
        admin = request.POST.post('admin', '')


    result['channel'] = channel
    result['phone'] = phone
    # return HttpResponse(json.dumps(result))
    # print(result)

    try:
        # client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        client = client_init2(result)
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e)
        return HttpResponse(json.dumps(result, ensure_ascii=False))

    try:
        await client(JoinChannelRequest(channel))
        result['status'] = True
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e)
        return HttpResponse(json.dumps(result, ensure_ascii=False))

    send_log_cnotent = phone + " → " + channel  + " → 加群"
    send_log(send_log_cnotent, admin)
    # print(send_log_cnotent)

    time.sleep(2)

    is_VERIFY = False

    try:
        photos = await client.get_messages(channel, 30)
        for x in photos:
            if hasattr(x, 'reply_markup') == True and x.reply_markup != None and x.mentioned == True:
                # 记录日志
                # 验证CHANNEL
                send_log_cnotent = phone + " → " + channel + "\n"+x.message + "\n"
                verifychannellog(send_log_cnotent, admin)

                is_VERIFY = True


                if len(x.reply_markup.rows) == 1:
                    result['verify'] = True
                    asyncio.create_task(x.click(0))
                    # await client.send_message('@lzh2020', str(x.reply_markup.rows[0].buttons[0].text)+" → "+channel)
                    print(str(x.reply_markup.rows[0].buttons[0].text) + " → " + channel)
                    break

                if len(x.reply_markup.rows) > 1:
                    # print(str(x.reply_markup.rows))
                    print(x.message)

                    if str(x.message).find("请按顺序点击") != -1:
                        message = str(x.message)
                        message = message.split("\n")
                        message = message.pop()

                        message = re.sub("（", "(", message)
                        message = re.sub("）", ")", message)
                        message = re.findall(r'[(](.*?)[)]', message)[0]
                        message = message.split("、")
                        for row in x.reply_markup.rows:
                            for bottons in row.buttons:
                                for son in message:
                                    if son == bottons.text:
                                        result['verify'] = True
                                        print(str(bottons.text) + " → " + channel)
                                        # asyncio.create_task(x.click(bottons.data))
                                        # time.sleep(1)
                                        x.click(bottons.data)
        if is_VERIFY == False:
            # NOVERIFY_CHANNEL
            send_log_cnotent = channel
            NOVERIFY_CHANNEL(send_log_cnotent, admin)

    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e,'click')
        return HttpResponse(json.dumps(result))

    await client.disconnect()

    # joinchannel_url =  + "boss91m/channelVerify" + "?channel=" + x['channel'] + "&session_string=" + \
    #                   x['session_string']
    # updateProfile = requests.post(joinchannel_url, data=x)
    # await automaticValidationChannel(phone, channel)

    return HttpResponse(json.dumps(result, ensure_ascii=False))


async def save_me_user(phone, user):
    # print(user)

    path = "user_chat/" + phone
    if os.path.exists(path) == True:
        # print(path)
        os.remove(path)

    fo = codecs.open(path+".txt", "a", 'utf-8')
    fo.write(str(user))
    fo.close()

    return True





async def  get_user(request):
    # 获取所有已加入的群
    result = {}
    phone = request.GET['session_string']
    result['phone'] = phone
    try:
        # client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        client = client_init2(result)
        await client.connect()

    except Exception as e:
        result = await telethonErrorMessage(result, e, 1009)
        await client.disconnect()
        return HttpResponse(json.dumps(result, ensure_ascii=False))

    try:
        channel = []
        user = []
        async for dialog in client.iter_dialogs():
            if dialog.is_channel == True:
                channel_son = {
                    'id': dialog.id,
                    'name': dialog.name,
                    'username': dialog.entity.username,
                }
                channel.append(channel_son)

            if dialog.is_user == True:
                # print(dialog.id)
                # print(dialog.name)
                # print(dialog.entity.username)
                user_son = {
                    'id': dialog.id,
                    'name': dialog.name,
                    'username': dialog.entity.username,
                }
                user.append(user_son)
        save_result = await save_me_user(phone, user)
        #
        data = {}
        data['user'] = user
        data['channel'] = channel
        data['phone'] = phone
        notice_admin = {
            "data": json.dumps(data)
        }
        # savedialog = requests.get(url='http://bs91mnotice.xyz/savedialog?data='+str(json.dumps(data)))
        savedialog = requests.post(url='http://bs91mnotice.xyz/savedialog', data=notice_admin)
        # print('http://bs91mnotice.xyz/savedialog?data='+str(json.dumps(data)))
        # print(savedialog.text)
        # print(HTMLParser(savedialog.text).body.text())
        return HttpResponse(HTMLParser(savedialog.text).body.text())

    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e, 1008)
        return HttpResponse(json.dumps(result, ensure_ascii=False))


    await client.disconnect()
    return HttpResponse(json.dumps({"status": True, "user": user, "channel": channel}, ensure_ascii=False))





async def async_sleep(client=''):
    await asyncio.sleep(5)
    print(123)
    await asyncio.sleep(5)
    print(2)
    return 1

async def asyncget_user(request):
    start = time.time()

    number = 890

    async def get(url):

        return 1

    async def request():
        url = 'https://static1.scrape.center/'
        # await get(url)
        time.sleep(2)
        print(123)


    tasks = [asyncio.ensure_future(request()) for _ in range(number)]
    # loop = asyncio.get_event_loop()
    # loop.run_until_complete()
    asyncio.wait(tasks)
    end = time.time()
    print('Number:', number, 'Cost time:', end - start)

    # asyncio.create_task(async_sleep())


    return HttpResponse(json.dumps({"status": True}, ensure_ascii=False))

async def  replyclient(request):

    result = {}
    phone = request.GET.get('session_string', '')
    if phone == '':
        phone = request.POST.get('session_string', '')

    username = request.GET.get('client_username', '')
    if username == '':
        username = request.POST.get('client_username', '')

    peer_id = request.GET.get('peer_id', '')
    if peer_id == '':
        peer_id = request.POST.get('peer_id', '')


    automatic_reply = request.GET.get('automatic_reply', '')
    if automatic_reply == '':
        automatic_reply = request.POST.get('automatic_reply', '')


    result['phone'] = phone
    result['username'] = username
    result['peer_id'] = peer_id
    result['automatic_reply'] = automatic_reply
    result['submit'] = 2

    print(result)

    try:
        client = client_init2(result)
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e,1008)
        print(result)
        return HttpResponse(json.dumps(result))

    if username == '':
        try:
            async for dialog in client.iter_dialogs():
                if dialog.is_user == True:
                   if dialog.id == int(peer_id):
                       await client.send_message(dialog.id, automatic_reply)
                       replyclient = requests.post(url='http://bs91mnotice.xyz/replyclient', data=result)
                       print(replyclient.text)
        except Exception as e:
            await client.disconnect()

            if str(e).find("The specified user was deleted") != -1:
                replyclient = requests.post(url='http://bs91mnotice.xyz/replyclient', data=result)
                print(replyclient.text)



            result = await telethonErrorMessage(result, e,10011)
            print(result)
            return HttpResponse(json.dumps(result))

    if username != '':
        try:
            await client.send_message(username, automatic_reply)
            replyclient = requests.post(url='http://bs91mnotice.xyz/replyclient', data=result)
            print(replyclient.text)
        except Exception as e:
            await client.disconnect()

            if str(e).find("The specified user was deleted") != -1:
                replyclient = requests.post(url='http://bs91mnotice.xyz/replyclient', data=result)
                print(replyclient.text)
            result = await telethonErrorMessage(result, e,10010)
            print(result)
            return HttpResponse(json.dumps(result))
    result['status'] = True
    return HttpResponse(json.dumps(result))


async def updateProfile(request):

    about = request.GET.get('about', '')
    if about == '':
        about = request.POST.get('about', '')

    first_name = request.GET.get('first_name', '')
    if first_name == '':
        first_name = request.POST.get('first_name', '')

    last_name = request.GET.get('last_name', '')
    if last_name == '':
        last_name = request.POST.get('last_name', '')

    phone = request.GET.get('session_string', '')
    if phone == '':
        phone = request.POST.get('session_string', '')

    telegram_id = request.GET.get('telegram_id', '')
    if telegram_id == '':
        telegram_id = request.POST.get('telegram_id', '')


    result = {}
    result['about'] = about
    result['last_name'] = last_name
    result['first_name'] = first_name
    result['session_string'] = phone
    result['phone'] = phone

    try:
        client = client_init2(result)
        await client.connect()
    except Exception as e:
        # await client.disconnect()
        result = await telethonErrorMessage(result, e)
        return HttpResponse(json.dumps(result, ensure_ascii=False))

    try:
        if about != '':
            await client(UpdateProfileRequest(about=about))

        if last_name != '' and first_name != '':
            await client(UpdateProfileRequest(
                first_name=first_name,
                last_name=last_name,
            ))
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e, 1002)
        return HttpResponse(json.dumps(result))


    try:

        get_me = await client.get_me()
        noticeAdminParams = {}
        noticeAdminParams['first_name'] = get_me.first_name
        noticeAdminParams['last_name'] = get_me.last_name
        noticeAdminParams['username'] = get_me.username
        noticeAdminParams['telegram_id'] = telegram_id
        saveGetSelf = requests.post(url='http://91m.live/CronTab/saveGetSelf', data=noticeAdminParams)
        print(saveGetSelf.text)
        noticeAdminParams['saveGetSelf'] = saveGetSelf.text
        noticeAdminParams['phone'] = phone
        return HttpResponse(json.dumps(noticeAdminParams))
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e, 1008)
        return HttpResponse(json.dumps(result))
    return HttpResponse(json.dumps(result))




# @my_async
async def channelVerify(request):

    channel = request.GET.get('channel', '')
    if channel == '':
        channel = request.POST.get('channel', '')

    phone = request.GET.get('session_string', '')
    if phone == '':
        phone = request.POST.get('session_string', '')


    result = {}
    result['phone'] = phone
    result['channel'] = channel


    try:
        client = client_init2(result)
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e,1008)
        return HttpResponse(json.dumps(result))
    #
    # await client(LeaveChannelRequest(channel))
    # await client.disconnect()
    # return HttpResponse(json.dumps(result))



    try:
        get_me = await client.get_me()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e,'get_me')
        return HttpResponse(json.dumps(result))

    try:
        photos = await client.get_messages(channel, 50)
        for x in photos:
            if hasattr(x, 'reply_markup') == True and x.reply_markup != None and x.mentioned == True:
                if len(x.reply_markup.rows) == 1:
                    result['verify'] = True
                    asyncio.create_task(x.click(0))
                    # await client.send_message('@lzh2020', str(x.reply_markup.rows[0].buttons[0].text)+" → "+channel)
                    print(str(x.reply_markup.rows[0].buttons[0].text) + " → " + channel)
                    break

                if len(x.reply_markup.rows) > 1:
                    # print(str(x.reply_markup.rows))
                    print(x.message)

                    if str(x.message).find("请按顺序点击") != -1:
                        message = str(x.message)
                        message = message.split("\n")
                        message = message.pop()

                        message = re.sub("（", "(", message)
                        message = re.sub("）", ")", message)
                        message = re.findall(r'[(](.*?)[)]', message)[0]
                        message = message.split("、")
                        for row in x.reply_markup.rows:
                            for bottons in row.buttons:
                                for son in message:
                                    if son == bottons.text:
                                        result['verify'] = True
                                        asyncio.create_task(x.click(bottons.data))

    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e,'get_me')
        return HttpResponse(json.dumps(result))

    result['status'] = True
    await client.disconnect()

    send_log_cnotent = phone + " → " + channel + " → " + 'channelVerify'
    send_log(send_log_cnotent)
    print(result)
    return HttpResponse(json.dumps(result))


async def channelVerify2(phone, channel):
    result = {}
    result['phone'] = phone
    result['channel'] = channel


    try:
        client = client_init2(result)
        await client.connect()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e,1008)
        return HttpResponse(json.dumps(result))
    #
    # await client(LeaveChannelRequest(channel))
    # await client.disconnect()
    # return HttpResponse(json.dumps(result))



    try:
        get_me = await client.get_me()
    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e,'get_me')
        return HttpResponse(json.dumps(result))

    try:
        photos = await client.get_messages(channel, 50)
        for x in photos:
            if hasattr(x, 'reply_markup') == True and x.reply_markup != None and x.mentioned == True:
                if len(x.reply_markup.rows) == 1:
                    result['verify'] = True
                    asyncio.create_task(x.click(0))
                    # await client.send_message('@lzh2020', str(x.reply_markup.rows[0].buttons[0].text)+" → "+channel)
                    print(str(x.reply_markup.rows[0].buttons[0].text) + " → " + channel)
                    break

                if len(x.reply_markup.rows) > 1:
                    # print(str(x.reply_markup.rows))
                    print(x.message)

                    if str(x.message).find("请按顺序点击") != -1:
                        message = str(x.message)
                        message = message.split("\n")
                        message = message.pop()

                        message = re.sub("（", "(", message)
                        message = re.sub("）", ")", message)
                        message = re.findall(r'[(](.*?)[)]', message)[0]
                        message = message.split("、")
                        for row in x.reply_markup.rows:
                            for bottons in row.buttons:
                                for son in message:
                                    if son == bottons.text:
                                        result['verify'] = True
                                        asyncio.create_task(x.click(bottons.data))

    except Exception as e:
        await client.disconnect()
        result = await telethonErrorMessage(result, e,'get_me')
        return HttpResponse(json.dumps(result))

    result['status'] = True
    await client.disconnect()

    send_log_cnotent = phone + " → " + channel + " → " + 'channelVerify'
    send_log(send_log_cnotent)
    print(result)
    return HttpResponse(json.dumps(result))