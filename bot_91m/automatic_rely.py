from telethon import TelegramClient, events
import time

# 使用my.telegram.org中的您自己的值
api_id = 18252973
api_hash = '7996fe1f8cd8223ddbca884fccdfa880'
phone = '5519987327612'

# client = TelegramClient('+543454133979', 18252973, '7996fe1f8cd8223ddbca884fccdfa880')
client = TelegramClient('session/6285817314155', 18252973, '7996fe1f8cd8223ddbca884fccdfa880')


@client.on(events.NewMessage(incoming=True))
async def handle_new_message(event):
    if event.is_private:  # only auto-reply to private chats
        # time.sleep(1)
        await event.respond('你好')
        # client.disconnect()

client.start()
client.run_until_disconnected()

# https://github.com/LonamiWebs/Telethon/blob/4b16183d2bbe80cbf4dabdb266a8015c5bf975cc/telethon_examples/README.md

