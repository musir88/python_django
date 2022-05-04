import TelethonSendMessage
import asyncio
import time
TelethonSendMessage = TelethonSendMessage.TelethonSendMessage()

loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

result = loop.run_until_complete(TelethonSendMessage.join_channel({
    'session_string': '5511931597688',
    # 'session_string': '5519987327612',
    'channel': 'https://t.me/HuNanTG',
    # 'channel': 'https://t.me/ziyuan2',
    # 'channel': 'https://t.me/chatssr',
    # 'channel': 'https://t.me/zscd18',
    # 'channel': 'https://t.me/hugoblog',
    # 'channel': 'https://t.me/pshqo',
    'admin': '40',
}))
print(result)

# result = loop.run_until_complete(TelethonSendMessage.ImportChatInviteRequest({
#     'session_string': '5511931597688',
#     # 'session_string': '5519987327612',
#     'channel': 'https://t.me/HuNanTG',
#     # 'channel': 'https://t.me/ziyuan2',
#     # 'channel': 'https://t.me/chatssr',
#     # 'channel': 'https://t.me/zscd18',
#     # 'channel': 'https://t.me/hugoblog',
#     # 'channel': 'https://t.me/pshqo',
#     'admin': '40',
# }))
# print(result)



# while True :
#
#
#
#
# result = loop.run_until_complete(TelethonSendMessage.send_message({
#     'session_string':'5511931597688',
#     'channel':'https://t.me/policr_mini_bot?start=verification_v1_-1001389086983',
#     'content':'/start',
#     'admin_id':'40',
#     'is_fake_content':'2',
#     'fake_content':'大哥，是我啊',
# }))
# print(result)
#     time.sleep(10)


# loop.run_until_complete(TelethonSendMessage.send_message({
#     'phone':'5511968992865',
#     'channel':'@bs91m1',
#     'send_content':'你好'
# }))