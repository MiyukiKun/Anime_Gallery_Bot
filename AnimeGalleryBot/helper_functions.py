from AnimeGalleryBot import tg_client as bot
from telethon import Button
from AnimeGalleryBot.gogoanimeapi import gogoanime as gogo
from AnimeGalleryBot import formating_results as format

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
        await bot.send_message(
            event.sender_id,
            f"{search_details.get('title')}\nYear: {search_details.get('year')}\nStatus: {search_details.get('status')}\nGenre: {x}\nEpisodes: {search_details.get('episodes')}",
            file=search_details.get('image_url'),
            buttons=[Button.inline(
                "Download", data=f"Download:{id}:{search_details.get('episodes')}")]
        )
    except:
        await bot.send_message(
            event.sender_id,
            f"{search_details.get('title')}\nYear: {search_details.get('year')}\nStatus: {search_details.get('status')}\nGenre: {x}\nEpisodes: {search_details.get('episodes')}",
            file=search_details.get('image_url'),
            buttons=[Button.inline(
                "Download", data=f"longdl:{split_id[1]}:{id[-25:]}:{search_details.get('episodes')}")]
        )

async def send_download_link(event, id, ep_num):
    links = gogo.get_episodes_link(animeid=id, episode_num=ep_num)
    result = format.format_download_results(links)
    await bot.send_message(
        event.sender_id,
        f"Download Links for episode {ep_num}\n{result}"
    )