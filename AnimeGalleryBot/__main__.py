from telethon import events
from AnimeGalleryBot import tg_client as bot
from AnimeGalleryBot import command_functions as cf
from AnimeGalleryBot import callback_functions as call

try:
    @bot.on(events.NewMessage(pattern="/start"))
    async def _(e):
        await cf.event_handler_start(e)

    @bot.on(events.NewMessage(pattern="/help"))
    async def _(e):
        await cf.event_handler_help(e)

    @bot.on(events.NewMessage(pattern="/latest"))
    async def _(e):
        await cf.event_handler_latest(e)

    @bot.on(events.NewMessage(pattern="/anime"))
    async def _(e):
        await cf.event_handler_anime(e)

    @bot.on(events.NewMessage(pattern="/source"))
    async def _(e):
        await cf.event_handler_source(e)
    
    @bot.on(events.CallbackQuery(pattern=b"lt:"))
    async def _(e):
        await call.callback_for_latest(e)
   
    @bot.on(events.CallbackQuery(pattern=b"Download"))
    async def _(e):
        await call.callback_for_download(e)

    @bot.on(events.CallbackQuery(pattern=b"longdl"))
    async def _(e):
        await call.callback_for_download_long(e)

    @bot.on(events.CallbackQuery(pattern=b"btz:"))
    async def _(e):
        await call.callback_for_choosebuttons(e)
    
    @bot.on(events.CallbackQuery(pattern=b"etz:"))
    async def _(e):
        await call.callback_for_choosebuttons1(e)

    @bot.on(events.CallbackQuery(pattern=b"ep:"))
    async def _(e):
        await call.callback_for_downlink(e)

    @bot.on(events.CallbackQuery(pattern=b"spp:"))
    async def _(e):
        await call.callback_for_downlink_long(e)

    @bot.on(events.CallbackQuery(pattern=b"split:"))
    async def _(e):
        await call.callback_for_details(e)

    @bot.on(events.CallbackQuery(pattern=b"dets:"))
    async def _(e):
        await call.callback_for_details_long(e)

except Exception as e:
    print(e)


bot.start()

bot.run_until_disconnected()