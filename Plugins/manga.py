from telethon import events, Button
from API.Kissmangaapi import kissmangaapi as kiss
import Helper.formating_results as format
from config import bot, bot_username
from Helper.helper_functions import *
import os

class Manga():

    @bot.on(events.NewMessage(pattern=fr"^/manga|^/manga@{bot_username}"))
    async def event_handler_manga(event):
        if '/manga' == event.raw_text:
            await bot.send_message(
                event.chat_id,
                'Command must be used like this\n/manga <name of manga>\nexample: /manga One Piece',
                file='https://media1.tenor.com/images/eaac56a1d02536ed416b5a080fdf73ba/tenor.gif?itemid=15075442'
            )

        elif '/manga' in event.raw_text:
            text = event.raw_text.split()
            text.pop(0)
            manga_name = " ".join(text)
            results = kiss.get_search_results(manga_name)
            if len(results) == 0:
                await bot.send_message(
                    event.chat_id,
                    'Not Found, Check for Typos or search Japanese name',
                    file='https://media.giphy.com/media/4pk6ba2LUEMi4/giphy.gif'
                )
            else:
                    button= []
                    for manga in results:
                        try:
                            button.append([Button.inline(manga[0], data=f"mid:{manga[1]}")])
                        except:
                            pass

                    await bot.send_message(
                        event.chat_id,
                        "Search Results:",
                        buttons=button
                    )       


    @bot.on(events.NewMessage(pattern="/read"))
    async def event_handler_manga(event):
        try:
            text = event.raw_text.split()
            text.pop(0)
            anime_name = " ".join(text)
            split_data = anime_name.split(":")
            chap = kiss.get_manga_chapter(split_data[0], split_data[1])
            if chap == "Invalid Mangaid or chapter number":
                await event.reply("Something went wrong.....\nCheck if you entered command properly\nCommon mistakes:\nYou didnt mention chapter number\nyou added space after : , dont leave space")
                return
            f = format.manga_chapter_html(f"{split_data[0]}{split_data[1]}", chap)
            await bot.send_message(
                event.chat_id,
                "Open this in google chrome",
                file= f
            )
            os.remove(f)

        except Exception as e:
            await event.reply("Something went wrong.....\nCheck if you entered command properly\n\nUse /help if you have any doubts")
            print(e)

    @bot.on(events.CallbackQuery(pattern="mid:"))
    async def callback_for_mangadets(event):
        data = event.data.decode('utf-8')
        dets = kiss.get_manga_details(data[4:])
        await event.edit('Search Results:')
        await bot.send_message(
            event.chat_id,
            f"Name: {dets[0]}\nGenre: {', '.join(dets[2])}\nLatest Chapter: {dets[3]}\n\n\nCopy This command and add chapter number at end\n\n`/read {data[4:]}:`",
            file=dets[1]
        )
