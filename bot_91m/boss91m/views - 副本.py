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

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


def send_log(content):
    fo = codecs.open("send_log/"+ str(date.today()) +".txt", "a", 'utf-8')
    fo.write("\n"+content)
    fo.close()




async def login(request):
    phone = request.GET['session_string']
    client = TelegramClient('session/'+phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')



    client.disconnect()








    await client.connect()



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

    result = {}
    is_fake_content = request.GET['is_fake_content']
    if is_fake_content == '1':
        fake_content = request.GET['fake_content']
        send_content = fake_content
    else:
        send_content = content

    result['is_fake_content'] = is_fake_content


    try:
        client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        await client.start()
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
        return HttpResponse(json.dumps(result))


    try:
        await client.send_message(channel, send_content)
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
        await client.disconnect()
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
        send_log(send_log_cnotent)

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

    try:
        client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        await client.start()
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
        return HttpResponse(json.dumps(result))

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
        result['status'] = False
        result['message'] = str(e)
        await client.disconnect()
        return HttpResponse(json.dumps(result))

    await client.disconnect()
    return HttpResponse(json.dumps({"status":True, "channel":channel}))


# 获取未读的用户的消息
async def chat_newmessage(request):
    phone = request.GET['session_string']

    result = {}

    try:
        client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        await client.start()
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
        return HttpResponse(json.dumps(result))


# 获取验证码
async def getTelegramCode(request):

    result = {}
    phone = request.GET['session_string']

    try:
        client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        await client.start()
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
        return HttpResponse(json.dumps(result))


    try:
        photos = await client.get_messages(777000, 1)
        for x in photos:
            result['code'] = x.text
            continue
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
        await client.disconnect()
        return HttpResponse(json.dumps(result))

    await client.disconnect()
    return HttpResponse(json.dumps(result))


# 修改二次验证码
async def update2fa(request):
    result = {}
    phone = request.GET['session_string']

    try:
        client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
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


async def waste_number(phone=''):
    admin_host = 'http://91m.live/telegram_api/waste_number'
    params = {}
    params['phone'] = phone
    res = requests.post(url=admin_host, data=params)
    print(res)

async def supstatus(phone='', supstatus=1):
    admin_host = 'http://91m.live/telegram_api/update_telegram_supstatus'
    params = {}
    params['phone'] = phone
    params['supstatus'] = supstatus
    res = requests.post(url=admin_host, data=params)
    print(res)


# 发送验证码
# @csrf_exempt
# @csrf_exempt
# @method_decorator(csrf_exempt, name='dispatch')
async def send_code_request(request):

    result = {}
    phone = request.GET['session_string']
    result['phone'] = phone


    # result['Access - Control - Allow - Origin”'] = ' * '
    # result['Access - Control - Allow - Methods'] = 'POST, GET, OPTIONS'
    # result['Access - Control - Max - Age'] = '1000'
    # result['Access - Control - Allow - Headers'] = ' * '

    print(result)

    try:
        # client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        client = TelegramClient('session/' + phone, 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
        await client.connect()
    except Exception as e:
        result['status'] = False
        result['message'] = str(e)
        result['message_code'] = 1002
        # return render(request, "send_code_request.html", result)
        return HttpResponse(json.dumps(result))

    try:
        await client.send_code_request(phone, force_sms=True)
        result['message'] = 'send code ok'

        # 通知后台该去获取验证码了
        await supstatus(phone, 2)
    except Exception as e:
        await client.disconnect()
        result['status'] = False
        result['message'] = str(e)
        result['message_code'] = 1004

        # 号被禁用
        if result['message'] == 'The used phone number has been banned from Telegram and cannot be used anymore. Maybe check https://www.telegram.org/faq_spam (caused by SendCodeRequest)' :
            await waste_number(phone)

        if result['message'] == 'The used phone number has been banned from Telegram and cannot be used anymore. Maybe check https://www.telegram.org/faq_spam (caused by SendCodeRequest)':
            await waste_number(phone)
        # return render(request, "send_code_request.html", result)
        return HttpResponse(json.dumps(result))

    submit_step = request.GET['submit_step']
    # 接码成功 完善注册信息
    if submit_step == '2':
        try:
            first_name = ''.join(random.sample(['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f','e', 'd', 'c', 'b', 'a'], random.randint(3,6)))
            last_name = ''.join(random.sample(['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g', 'f','e', 'd', 'c', 'b', 'a'], random.randint(3,6)))
            code = request.GET['code']
            await client.sign_up(code=code, first_name=first_name,last_name=last_name,phone=phone)
            await supstatus(phone, 3) # 通知后台号码注册成功了
        except Exception as e:
            result['status'] = False
            result['message'] = str(e)
            result['message_code'] = 1003
            return HttpResponse(json.dumps(result))
            # return render(request, "send_code_request.html", result)

        # 设置二次验证码
        try:
            await client.edit_2fa(new_password='91m123456')
        except Exception as e:
            await client.disconnect()
            result['status'] = False
            result['message'] = str(e)
            result['message_code'] = 1006
            return HttpResponse(json.dumps(result))
            # return render(request, "send_code_request.html", result)

        # 设置用户名
        # try:
        #     username = ''.join(random.sample(['z', 'y', 'x', 'w', 'v', 'u', 't', 's', 'r', 'q', 'p', 'o', 'n', 'm', 'l', 'k', 'j', 'i', 'h', 'g','f', 'e', 'd', 'c', 'b', 'a'], random.randint(8,13)))
        #     await client(UpdateUsernameRequest(username))
        # except Exception as e:
        #     await client.disconnect()
        #     result['status'] = False
        #     result['message'] = str(e)
        #     result['message_code'] = 1005
        #     # return render(request, "send_code_request.html", result)
        #     return HttpResponse(json.dumps(result))

        result['message'] = 'sign_up ok'

    await client.disconnect()


    result['submit_step'] = submit_step

    result['admin_host'] = ''
    # result['admin_host'] = 'http://91m.live/'

    # return render(request, "send_code_request.html", result)

    result['status'] = True
    return HttpResponse(json.dumps(result))


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


async def sign_up_ok(request):
    print(123)
    # data = {};
    # data['phone'] = request.GET['phone']
    # admin_host = 'http://91m.live/telegram_api/login_ok'
    #
    # res = requests.post(url=admin_host, data=data)
    # return HttpResponse(res)