from telethon.tl.types import ChannelParticipantsAdmins
from telethon import TelegramClient, events
from config import api_id, api_hash

client = TelegramClient('user', api_id, api_hash)
client.start()


@client.on(events.NewMessage(pattern='!mn'))
async def mention(event):
    text = event.raw_text.replace("!mn ", "")
    chatId = event.chat_id
    counter = 0
    admins = []

    async for user in client.iter_participants(chatId, filter=ChannelParticipantsAdmins):
        admins.append(user.id)
   
    if event.from_id in admins:

        async for user in client.iter_participants(chatId, aggressive=True):
            if user.id in admins:
                continue
            else:
                counter += 1
                mnText = getText(text, user.first_name, user.last_name)
                client.send_message(chatId, f"[{mnText}](tg://user?id={user.id})")
         
        client.send_message(chatId, "Здається кінчив...")

    print(f"{event.chat} - count: {counter}")
    admins.clear()



def name(first, last):
    return first if last == None else f"{first} {last}"

def getText(text, firstname, lastname):
    if "name" in text:
        return text.replace("name", name(firstname, lastname))
    else:
        return text

with client:
    client.run_until_disconnected()
