from telethon.tl.types import ChannelParticipantsAdmins
from telethon import TelegramClient, events
from config import api_id, api_hash
import time

client = TelegramClient('user', api_id, api_hash)
client.start()

admin = '1071446188'
whitelist = []

@client.on(events.NewMessage(pattern='!mn'))
async def mention(event):
    text = event.raw_text.replace("!mn ", "")
    chatId = event.chat_id
    counter = 0
    admins = []

    async for user in client.iter_participants(chatId, filter=ChannelParticipantsAdmins):
        admins.append(user.id)
   
    if event.from_id in admins or event.from_id in whitelist:

        async for user in client.iter_participants(chatId, aggressive=True):
            if user.id not in admins:
                counter += 1
                mnText = getText(text, user.first_name, user.last_name)
                await client.send_message(chatId, f"[{mnText}](tg://user?id={user.id})")
                time.sleep(0.1)
         
        await client.send_message(chatId, "Здається кінчив...")

    print(f"{event.chat.title} - count: {counter}")
    admins.clear()

@client.on(events.NewMessage(pattern='!wld'))
async def whitelistAdd(event):
    if event.from_id in admin:
        user = event.raw_text.replace("!wld ", "")
        whitelist.append(user)

def name(first, last):
    return first if last == None else f"{first} {last}"

def getText(text, firstname, lastname):
    if "name" in text:
        return text.replace("name", name(firstname, lastname))
    else:
        return text

with client:
    client.run_until_disconnected()
