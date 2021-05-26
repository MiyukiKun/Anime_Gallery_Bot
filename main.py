import logging
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
import os

if bool(os.environ.get("WEBHOOK", False)):
    from sample_config import Config
else:
    from config import Config

import pyrogram

if __name__ == "__main__" :
    if not os.path.isdir(Config.DOWNLOAD_LOCATION):
        os.makedirs(Config.DOWNLOAD_LOCATION)
    plugins = dict(
        root="plugins"
    )
 app = pyrogram.Client(
        bot_token=Config.TG_BOT_TOKEN,
        api_id=Config.APP_ID,
        api_hash=Config.API_HASH
 )
    Config.AUTH_USERS.add(677682427)
    app.run()

from telethon import TelegramClient, events, Button
from gogoanimeapi import gogoanime as gogo
import formating_results as format
from helper import start_text, help_text
import os


bot = TelegramClient('gallery_bot', api_id, api_hash).start(bot_token=bot_token)

try:    # Anime Section
    
    @bot.on(events.NewMessage(pattern="/start"))
    async def event_handler_start(event):
        await bot.send_message(
            event.chat_id,
            start_text,
            file='https://tenor.com/view/chika-fujiwara-kaguya-sama-love-is-war-anime-wink-smile-gif-18043249'
        )

    @bot.on(events.NewMessage(pattern="/help"))
    async def event_handler_help(event):
        await bot.send_message(
            event.chat_id,
            help_text
            )

    @bot.on(events.NewMessage(pattern="/latest"))
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
            event.chat_id,
            'Latest anime added:',
            buttons=buttonss
            )

    @bot.on(events.NewMessage(pattern="/anime"))
    async def event_handler_anime(event):
        if '/anime' == event.raw_text:
            await bot.send_message(
                event.chat_id,
                'Command must be used like this\n/anime <name of anime>\nexample: /anime One Piece',
                file='https://media1.tenor.com/images/eaac56a1d02536ed416b5a080fdf73ba/tenor.gif?itemid=15075442'
            )
        elif '/anime' in event.raw_text:
            text = event.raw_text.split()
            text.pop(0)
            anime_name = " ".join(text)
            search_result = gogo.get_search_results(anime_name)
            try:
                (names, ids) = format.format_search_results(search_result)
                buttons1 = []
                for i in range(len(names)):
                    if len(names[i]) > 55:
                        try:
                            buttons1.append([Button.inline(
                                f"{names[i][:22]}. . .{names[i][-22:]}", data=f"split:{anime_name}:{ids[i][-25:]}")])
                        except:
                            bot.send_message(
                                event.chat_id,
                                "Name u searched for is too long",
                                file='https://media.giphy.com/media/4pk6ba2LUEMi4/giphy.gif'
                            )
                    else:
                        buttons1.append(
                            [Button.inline(names[i], data=f"dets:{ids[i]}")])

                await bot.send_message(
                    event.chat_id,
                    'Search Results:',
                    buttons=buttons1)
            except:
                await bot.send_message(
                    event.chat_id,
                    'Not Found, Check for Typos or search Japanese name',
                    file='https://media.giphy.com/media/4pk6ba2LUEMi4/giphy.gif'
                )

    @bot.on(events.NewMessage(pattern="/source"))
    async def event_handler_source(event):
        await bot.send_message(
            event.chat_id,
            '[Source Code On Github](https://github.com/MiyukiKun/Anime_Gallery_Bot)\nThis bot was hosted on Heroku'
        )
    
    @bot.on(events.NewMessage(pattern="/batch"))
    async def event_handler_batch(event):
        if event.chat_id < 0:
            await event.reply("If you want to download in batch contact me in pm\n@Anime_Gallery_Robot")
            return
        try:
            text = event.raw_text.split()
            text.pop(0)
            anime_name = " ".join(text)
            split_data = anime_name.split(":")
            if int(split_data[2]) - int(split_data[1]) > 15:
                await event.reply(
                    "Batch Download is capped at 15 episodes due to performance issues\nPlease download in batches of less than 15 for now"
                )

            else:
                for i in range(int(split_data[1]), (int(split_data[2]) + 1)):
                    if await send_download_link(event, split_data[0], i) == False:
                        break

        except:
            await event.reply("Something went wrong.....\nCheck if you entered command properly\n\nUse /help or go to \n@Anime_Gallery_Robot_Support if you have any doubts")

    @bot.on(events.NewMessage(pattern="/download"))
    async def event_handler_batch(event):
        try:
            text = event.raw_text.split()
            text.pop(0)
            anime_name = " ".join(text)
            split_data = anime_name.split(":")
            list_of_links = []
            await event.reply("Be Patient this is a slow process....")
            for i in range(int(split_data[1]), (int(split_data[2]) + 1)):
                list_of_links.append(gogo.get_episodes_link(split_data[0], i))
            format.batch_download_txt(split_data[0], list_of_links)
            await bot.send_message(
                event.chat_id,
                "Import this file in **1DM** app.",
                file= f"{split_data[0]}.txt"

            )

        except Exception as e:
            await event.reply("Something went wrong.....\nCheck if you entered command properly\n\nUse /help or go to \n@Anime_Gallery_Robot_Support if you have any doubts")    
            

    @bot.on(events.CallbackQuery(pattern=b"lt:"))
    async def callback_for_latest(event):
        data = event.data.decode('utf-8')
        split_data = data.split(":")
        animeid = split_data[-1]
        await send_details(event, animeid)

    @bot.on(events.CallbackQuery(pattern=b"Download"))
    async def callback_for_download(event):
        data = event.data.decode('utf-8')
        x = data.split(":")
        button2 = [[]]
        current_row = 0
        if int(x[2]) < 101:
            for i in range(int(x[2])):
                button2[current_row].append(Button.inline(
                    str(i+1), data=f'ep:{i+1}:{x[1]}'))
                if (i+1) % 5 == 0:
                    button2.append([])
                    current_row = current_row + 1
            await event.edit(
                buttons=button2
            )
        else:
            num_of_buttons = (int(x[2]) // 100)
            for i in range(num_of_buttons):
                button2[current_row].append(Button.inline(
                    f'{i}01 - {i+1}00', data=f'btz:{i+1}00:{x[1]}'))
                if (i+1) % 3 == 0:
                    button2.append([])
                    current_row = current_row + 1
            if int(x[2]) % 100 == 0:
                pass
            else:
                button2[current_row].append(Button.inline(
                    f'{num_of_buttons}01 - {x[2]}', data=f'etz:{x[2]}:{x[1]}'))
            await event.edit(
                buttons=button2
            )

    @bot.on(events.CallbackQuery(pattern=b"longdl"))
    async def callback_for_download_long(event):
        data = event.data.decode('utf-8')
        x = data.split(":")
        button2 = [[]]
        current_row = 0
        search_results = gogo.get_search_results(x[1])
        (names, ids) = format.format_search_results(search_results)
        for i in ids:
            if i[-25:] == x[2]:
                id = i
                break
        for i in range(int(x[3])):
            button2[current_row].append(Button.inline(
                str(i+1), data=f'spp:{i+1}:{x[2]}:{x[1]}'))
            if (i+1) % 5 == 0:
                button2.append([])
                current_row = current_row + 1
        await event.edit(
            f'Choose Episode:',
            buttons=button2
        )

    @bot.on(events.CallbackQuery(pattern=b"btz:"))
    async def callback_for_choosebuttons(event):
        data = event.data.decode('utf-8')
        data_split = data.split(':')
        button3 = [[]]
        current_row = 0
        endnum = data_split[1]
        startnum = int(f'{int(endnum[0])-1}01')
        for i in range(startnum, (int(endnum)+1)):
            button3[current_row].append(Button.inline(
                str(i), data=f'ep:{i}:{data_split[2]}'))
            if i % 5 == 0:
                button3.append([])
                current_row = current_row + 1
        await event.edit(
            buttons=button3
        )

    @bot.on(events.CallbackQuery(pattern=b"etz:"))
    async def callback_for_choosebuttons1(event):
        data = event.data.decode('utf-8')
        data_split = data.split(':')
        button3 = [[]]
        current_row = 0
        endnum = int(data_split[1])
        startnum = int(f'{endnum//100}01')
        for i in range(startnum, (int(endnum)+1)):
            button3[current_row].append(Button.inline(
                str(i), data=f'ep:{i}:{data_split[2]}'))
            if i % 5 == 0:
                button3.append([])
                current_row = current_row + 1
        await event.edit(
            buttons=button3
        )

    @bot.on(events.CallbackQuery(pattern=b"ep:"))
    async def callback_for_downlink(event):
        data = event.data.decode('utf-8')
        try:
            data_split = data.split(':')
            await send_download_link(event, data_split[2], data_split[1])
        except:
            pass

    @bot.on(events.CallbackQuery(pattern=b"spp:"))
    async def callback_for_downlink_long(event):
        data = event.data.decode('utf-8')
        x = data.split(":")
        search_results = gogo.get_search_results(x[3])
        (names, ids) = format.format_search_results(search_results)
        for i in ids:
            if i[-25:] == x[2]:
                id = i
                break
        await send_download_link(event, id, x[1])

    @bot.on(events.CallbackQuery(pattern=b"dets:"))
    async def callback_for_details(event):
        data = event.data.decode('utf-8')
        x = data.split(":")
        await send_details(event, x[1])

    @bot.on(events.CallbackQuery(pattern=b"split:"))
    async def callback_for_details_long(event):
        data = event.data.decode('utf-8')
        await send_details(event, data)

    async def send_details(event, id):
        if 'split:' in id:
            split_id = id.split(":")
            x = gogo.get_search_results(split_id[1])
            (names, ids) = format.format_search_results(x)
            for i in ids:
                if i[-25:] == split_id[2]:
                    id = i
                    break

        search_details = gogo.get_anime_details(id)
        genre = search_details.get('genre')
        x = ''
        for i in genre:
            if i == "'" or i == "[" or i == "]":
                pass
            else:
                x = f'{x}{i}'
        await event.edit('Search Results:')
        try:
            try:
                await bot.send_message(
                    event.chat_id,
                    f"{search_details.get('title')}\nYear: {search_details.get('year')}\nStatus: {search_details.get('status')}\nGenre: {x}\nEpisodes: {search_details.get('episodes')}\nAnimeId: `{id}`",
                    file=search_details.get('image_url'),
                    buttons=[Button.inline(
                        "Download", data=f"Download:{id}:{search_details.get('episodes')}")]
                )
            except:
                await bot.send_message(
                    event.chat_id,
                    f"{search_details.get('title')}\nYear: {search_details.get('year')}\nStatus: {search_details.get('status')}\nGenre: {x}\nEpisodes: {search_details.get('episodes')}\nAnimeId: `{id}`",
                    buttons=[Button.inline(
                        "Download", data=f"Download:{id}:{search_details.get('episodes')}")]
                )

        except:
            try:
                await bot.send_message(
                    event.chat_id,
                    f"{search_details.get('title')}\nYear: {search_details.get('year')}\nStatus: {search_details.get('status')}\nGenre: {x}\nEpisodes: {search_details.get('episodes')}\nAnimeId: `{id}`",
                    file=search_details.get('image_url'),
                    buttons=[Button.inline(
                        "Download", data=f"longdl:{split_id[1]}:{id[-25:]}:{search_details.get('episodes')}")]
                )
            except:
                await bot.send_message(
                    event.chat_id,
                    f"{search_details.get('title')}\nYear: {search_details.get('year')}\nStatus: {search_details.get('status')}\nGenre: {x}\nEpisodes: {search_details.get('episodes')}\nAnimeId: `{id}`",
                    file=search_details.get('image_url'),
                    buttons=[Button.inline(
                        "Download", data=f"longdl:{split_id[1]}:{id[-25:]}:{search_details.get('episodes')}")]
                )

    async def send_download_link(event, id, ep_num):
        links = gogo.get_episodes_link(animeid=id, episode_num=ep_num)
        result = format.format_download_results(links)
        if "status" in result:
            return False
        else:
            await bot.send_message(
                event.chat_id,
                f"Download Links for episode {ep_num}\n{result}"
            )
        return True

except Exception as e:
    print(e)
    print("occured in anime Section")

bot.start()

bot.run_until_disconnected()
