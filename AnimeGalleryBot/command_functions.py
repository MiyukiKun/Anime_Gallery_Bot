from AnimeGalleryBot.helper import start_text, help_text
from AnimeGalleryBot import tg_client as bot
from AnimeGalleryBot.gogoanimeapi import gogoanime as gogo
from telethon import Button
from AnimeGalleryBot import formating_results as format

async def event_handler_start(event):
    await bot.send_message(
        event.sender_id,
        start_text,
        file='https://tenor.com/view/chika-fujiwara-kaguya-sama-love-is-war-anime-wink-smile-gif-18043249'
    )

async def event_handler_help(event):
    await bot.send_message(
        event.sender_id,
        help_text
        )

async def event_handler_latest(event):
    home_page = gogo.get_home_page()
    (names, ids, epnums) = format.format_home_results(home_page)
    buttonss = []
    for i in range(len(names)):
        try:
            buttonss.append(
                [Button.inline(names[i], data=f"lt:{ids[i]}")])
        except:
            pass
    await bot.send_message(
        event.sender_id,
        'Latest anime added:',
        buttons=buttonss
        )

async def event_handler_anime(event):
    if '/anime' == event.raw_text:
        await bot.send_message(
            event.sender_id,
            'Command must be used like this\n/anime <name of anime>\nexample: /anime One Piece',
            file='https://media1.tenor.com/images/eaac56a1d02536ed416b5a080fdf73ba/tenor.gif?itemid=15075442'
        )
    elif '/anime' in event.raw_text:
        search_result = gogo.get_search_results(event.raw_text[7:])
        try:
            (names, ids) = format.format_search_results(search_result)
            buttons1 = []
            for i in range(len(names)):
                if len(names[i]) > 55:
                    try:
                        buttons1.append([Button.inline(
                            f"{names[i][:22]}. . .{names[i][-22:]}", data=f"split:{event.raw_text[7:]}:{ids[i][-25:]}")])
                    except:
                        bot.send_message(
                            event.sender_id,
                            "Name u searched for is too long",
                            file='https://media.giphy.com/media/4pk6ba2LUEMi4/giphy.gif'
                        )
                else:
                    buttons1.append(
                        [Button.inline(names[i], data=f"dets:{ids[i]}")])

            await bot.send_message(
                event.sender_id,
                'Search Results:',
                buttons=buttons1)
        except:
            await bot.send_message(
                event.sender_id,
                'Not Found, Check for Typos or search Japanese name',
                file='https://media.giphy.com/media/4pk6ba2LUEMi4/giphy.gif'
            )

async def event_handler_source(event):
    await bot.send_message(
        event.sender_id,
        'Bot Owner: @President_Shirogane\n[Source Code On Github](https://github.com/MiyukiKun/Anime_Gallery_Bot)\nThis bot was hosted on Heroku'
    )