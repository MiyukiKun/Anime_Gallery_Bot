from telethon import Button
from config import bot
from Helper import formating_results as format
from database import ConfigDB
from API.gogoanimeapi import Gogo
cdb = ConfigDB()

async def send_details(event, id):
    data = cdb.find({"_id":"GogoAnime"})
    gogo = Gogo(
        gogoanime_token=data["gogoanime"],
        auth_token=data["auth"],
        host=data["url"]
    )
    if 'split:' in id:
        split_id = id.split(":")
        x = gogo.get_search_results(split_id[1])
        (_, ids) = format.format_search_results(x)
        for i in ids:
            if i[-25:] == split_id[2]:
                id = i
                break

    search_details = gogo.get_anime_details(id)
    genre = search_details.get('genre')
    
    await event.edit('Search Results:')
    try:
        await bot.send_message(
            event.chat_id,
            f"{search_details.get('title')}\nYear: {search_details.get('year')}\nStatus: {search_details.get('status')}\nGenre: {genre}\nEpisodes: {search_details.get('episodes')}\nAnimeId: `{id}`",
            file=search_details.get('image_url', None),
            buttons=[Button.inline(
                "Download", data=f"Download:{id}:{search_details.get('episodes')}")]
        )

    except:
        await bot.send_message(
            event.chat_id,
            f"{search_details.get('title')}\nYear: {search_details.get('year')}\nStatus: {search_details.get('status')}\nGenre: {genre}\nEpisodes: {search_details.get('episodes')}\nAnimeId: `{id}`",
            file=search_details.get('image_url', None),
            buttons=[Button.inline(
                "Download", data=f"longdl:{split_id[1]}:{id[-25:]}:{search_details.get('episodes')}")]
        )
            
async def send_download_link(event, id, ep_num):
    data = cdb.find({"_id":"GogoAnime"})
    gogo = Gogo(
        gogoanime_token=data["gogoanime"],
        auth_token=data["auth"],
        host=data["url"]
    )
    l1 = gogo.get_episodes_link(animeid=id, episode_num=ep_num)
    l2 = gogo.get_stream_link(animeid=id, episode_num=ep_num)
    r1 = format.format_download_results(l1)
    r2 = format.format_download_results(l2)
    await bot.send_message(
        event.chat_id,
        f"Download Links for episode {ep_num}\n{r1}\n\nStreamable Links:\n{r2}"
    )
        
    return True
