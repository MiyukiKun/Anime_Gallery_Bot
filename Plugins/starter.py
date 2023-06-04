from Helper.helper import start_text, help_text
from config import bot, bot_username
from telethon import events
from database import UsersDB

users = UsersDB()

class Start():

    @bot.on(events.NewMessage(pattern=fr"^/start$|^/start@{bot_username}"))
    async def event_handler_start(event):
        users.add({"_id": event.chat_id, "username": event.sender.username, "name": f"{event.sender.first_name} {event.sender.last_name}"})
        await bot.send_message(
            event.chat_id,
            start_text,
            file='https://tenor.com/view/chika-fujiwara-kaguya-sama-love-is-war-anime-wink-smile-gif-18043249'
        )

    @bot.on(events.NewMessage(pattern=fr"^/help$|^/help@{bot_username}"))
    async def event_handler_help(event):
        await bot.send_message(
            event.chat_id,
            help_text
            )