from AnimeGalleryBot import tg_client as bot
from telethon import Button
from AnimeGalleryBot.gogoanimeapi import gogoanime as gogo
from AnimeGalleryBot.helper_functions import *

async def callback_for_latest(event):
    data = event.data.decode('utf-8')
    split_data = data.split(":")
    animeid = split_data[-1]
    await send_details(event, animeid)

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
            f'Choose Episode:',
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
            f'Choose Episode:',
            buttons=button2
            )
            
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
        f'Choose Episode:',
        buttons=button3
    )

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
        f'Choose Episode:',
        buttons=button3
    )

async def callback_for_downlink(event):
    data = event.data.decode('utf-8')
    data_split = data.split(':')
    await send_download_link(event, data_split[2], data_split[1])

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

async def callback_for_details(event):
    data = event.data.decode('utf-8')
    await send_details(event, data)

async def callback_for_details_long(event):
    data = event.data.decode('utf-8')
    x = data.split(":")
    await send_details(event, x[1])
