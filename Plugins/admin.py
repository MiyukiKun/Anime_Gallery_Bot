from telethon import events
from config import bot, owner_id
from database import UsersDB, ConfigDB
import json
import os
import asyncio

users = UsersDB()
cdb = ConfigDB()

class Admin:

    @bot.on(events.NewMessage(pattern="/stats", chats=owner_id))
    async def stats(event):
        userdata = users.full()
        if "export" in event.raw_text:
            with open("userdata.json", "w") as final:
                json.dump(userdata, final, indent=4)
            await event.reply(f"Statistics for bot:\n Total number of users: {len(userdata)}", file="userdata.json")
            os.remove("userdata.json")
        else:
            await event.reply(f"Statistics for bot:\n Total number of users: {len(userdata)}")

    @bot.on(events.NewMessage(pattern="/broadcast", chats=owner_id))
    async def broadcast(event):
        msg = await event.get_reply_message()
        userdata = users.full()
        for i in userdata:
            try:
                await bot.send_message(i['_id'], msg)
                await asyncio.sleep(0.5)
            except Exception as e:
                print(e)

    @bot.on(events.NewMessage(pattern="/update_token", chats=owner_id))
    async def update_token(event):
        msg = await event.get_reply_message().raw_text.split("\n")
        url = msg[0].split("	")[0]
        gogoanime = msg[1][6]
        auth = msg[0][6]

        cdb.modify(
                {
                    "_id":"GogoAnime"
                },
                {
                    "_id":"GogoAnime",
                    "url": url,
                    "gogoanime": gogoanime,
                    "auth": auth
                }
            )
    
        await event.reply("Token Updated Successfully.")

