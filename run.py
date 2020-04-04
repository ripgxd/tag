from telethon.tl.types import ChannelParticipantsAdmins
from telethon import TelegramClient, events
from config import api_id, api_hash

client = TelegramClient('user', api_id, api_hash)
client.start()

admins = []
global text



# @client.on(events.NewMessage(pattern='!get'))
# async def get_admins(event):
#     admins.clear()
#     async for user in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
#         print(f"{user.id} - {user.first_name} {user.last_name}")
#         admins.append(user.id)
#     print("done")
    

@client.on(events.NewMessage(pattern='!mn'))
async def mention(event):
    admins.clear()
    async for user in client.iter_participants(event.chat_id, filter=ChannelParticipantsAdmins):
        print(f"{user.id} - {user.first_name} {user.last_name}")
        admins.append(user.id)

    if event.from_id in admins:
        
        text = text_buffer = event.raw_text.replace("!mn ", "")
        async for user in client.iter_participants(event.chat_id):
            
            if user.id not in admins:
            
                await client.send_message(event.chat_id, f"[{text}](tg://user?id={user.id})")

        await client.send_message(event.chat_id, ">КІНЧИВ<")

# def name(first, last):
#     return first if last == None else f"{first} {last}"

with client:
    client.run_until_disconnected()