from telethon import events
import Helper.formating_results as format
from API.nhentaiapi import nhentaiapi as nh
from config import bot

class Nhentai():

    @bot.on(events.NewMessage(pattern="/nh"))
    async def event_handler_anime(event):
        if '/nh' == event.raw_text:
            await bot.send_message(
                event.chat_id,
                'Command must be used like this\n/nh <hentai code\nexample: /nh 339989',
                file='https://media1.tenor.com/images/eaac56a1d02536ed416b5a080fdf73ba/tenor.gif?itemid=15075442'
            )
        elif '/nh' in event.raw_text:
            text = event.raw_text.split()
            text.pop(0)
            code = " ".join(text)
            chapter = nh.get_chapter_by_code(code)
            format.manga_chapter_html(f"{code}", chapter)
            await bot.send_message(
                event.chat_id,
                "Open this in google chrome",
                file= f"{code}.html"
            )