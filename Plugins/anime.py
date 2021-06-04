from telethon import events, Button
from API.gogoanimeapi import gogoanime as gogo
import Helper.formating_results as format
from config import bot
from Helper.helper_functions import *

class Anime():

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
            if int(split_data[2]) - int(split_data[1]) > 100:
                await event.reply(
                    "Batch Download is capped at 100 episodes due to performance issues\nPlease download in batches of less than 100 for now"
                )
                return
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

        except:
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