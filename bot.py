import os
import json
from telethon import TelegramClient, events
from telethon.tl.custom import Button
import requests
from dotenv import load_dotenv

load_dotenv()
Apiid = os.getenv("API_ID")
ApiHash = os.getenv("API_HASH")
Token = os.getenv("BOT_TOKEN")
client = TelegramClient('session', Apiid, ApiHash).start(bot_token=Token)

def ToCatBox(Path):
    url = 'https://catbox.moe/user/api.php'
    files = {'fileToUpload': open(Path, 'rb')}
    data = {'reqtype': 'fileupload'}
    response = requests.post(url, data=data, files=files)
    if response.status_code == 200:
        return response.text.strip()
    else:
        return "**I'm Sorry...**"

#def ToData(UserId, FileLink):
#    UserData = json.load(open('CatBox.json', 'r')) if os.path.exists('CatBox.json') else {}
#    UserData.setdefault(str(UserId), {"true": "true", "link": []})["link"].append(FileLink)
#    json.dump(UserData, open('CatBox.json', 'w'), indent=4)

@client.on(events.NewMessage(pattern='/start'))
async def Welcome(event):
    buttons = [
        [Button.url('الـمـطـور', 'https://t.me/U3_F1')],
        [Button.url('Developer', 'https://t.me/U3_F1')],
        [Button.url('开发者帐号', 'https://t.me/U3_F1')]
    ]
    await event.reply(
        file='Hi.tgs',
        buttons=buttons
    )

@client.on(events.NewMessage(incoming=True, func=lambda e: e.is_private and (e.file)))
async def ToCatBoxComm(event):
    try:
        Path = await event.download_media()
        link = ToCatBox(Path)
        #ToData(event.sender_id, link)
        os.remove(Path)
        await event.reply(f"**Done:** [{link}]({link})", parse_mode='markdown')
    except Exception as e:
        await event.reply("**I'm Sorry...**", parse_mode='markdown')

client.run_until_disconnected()
