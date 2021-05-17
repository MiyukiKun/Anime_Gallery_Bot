from telethon import TelegramClient, events, Button
from gogoanimeapi import gogoanime as gogo
import formating_results as format
import os

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)

try:
    @bot.on(events.NewMessage)
    async def event_handler(event):
        if '/anime' in event.raw_text:
            search_result = gogo.get_search_results(event.raw_text[6:])
            try:
                (names, ids) = format.format_search_results(search_result)   
                buttons1 = []
                for i in range(len(names)):
                    if len(names[i]) > 60:
                        await bot.send_message(event.sender_id, 'Result Found but Telegram doesnt allow for buttons to have more than 64 letters(trying to find a fix)')
                    else:
                        buttons1.append([Button.inline(names[i], data= ids[i])])

                await bot.send_message(
                        event.sender_id,
                        'Search Results:',
                        buttons=buttons1)
            except:
                    await bot.send_message(event.sender_id, 'Not Found')


    async def send_details(event, id):
        search_details = gogo.get_anime_details(id)
        genre = search_details.get('genre')
        x = ''
        for i in genre:
            if i == "'" or i == "[" or i == "]":
                pass
            else:
                x = f'{x}{i}'
        await bot.send_message(
                    event.sender_id,  
                    f"{search_details.get('title')}\nYear: {search_details.get('year')}\nStatus: {search_details.get('status')}\nGenre: {x}\nEpisodes: {search_details.get('episodes')}",
                    file=search_details.get('image_url'),
                    buttons=[Button.inline("Download", data=f"Download {id} {search_details.get('episodes')}")]
                    )

    async def send_download_link(event, id, ep_num):
        links = gogo.get_episodes_link(animeid=id, episode_num=ep_num)
        result = format.format_download_results(links)
        await bot.send_message(event.sender_id, f"Download Links for episode {ep_num}\n{result}")


    @bot.on(events.CallbackQuery)
    async def callback(event):
        data = event.data.decode('utf-8')
        if 'Download' in data:
            x = data.split()
            button2 = [[]]
            current_row = 0
            if int(x[2]) <101:
                for i in range(int(x[2])):
                    button2[current_row].append(Button.inline(str(i+1), data=f'ep{i+1}:{x[1]}'))
                    if (i+1) % 5 == 0:
                        button2.append([])
                        current_row = current_row +1
                await bot.send_message(
                            event.sender_id, 
                            f'Choose Episode:', 
                            buttons=button2
                            )
            else:
                pass  #Need to do something about 100+ episode anime

    @bot.on(events.CallbackQuery)
    async def callback(event):
        try:
            data = event.data.decode('utf-8')
            data_split = data.split(':')
            await send_download_link(event, data_split[1], data_split[0][2:])
        except:
            pass

    @bot.on(events.CallbackQuery)
    async def callback(event):
        id = event.data.decode('utf-8')
        try:
            await send_details(event, id)
        except:
            pass


except Exception as e:
    print(e)
    

bot.start()

bot.run_until_disconnected()
