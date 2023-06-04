from Plugins.starter import Start
from Plugins.anime import Anime
from Plugins.manga import Manga
from Plugins.admin import Admin
from config import bot
import traceback

start = Start()
anime = Anime()
manga = Manga()
admin = Admin()

try:
    start
    anime
    manga
    admin
except:
    err_str = traceback.format_exc()
    print(err_str)

bot.start()

bot.run_until_disconnected()