import os
import dotenv
from telethon import TelegramClient
from pymongo import MongoClient
from API.gogoanimeapi import Gogo
from pymongo.collection import Collection

dotenv.load_dotenv(".env")

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')
db_url = os.environ.get('MONGO_DB_URL')
database_name = os.environ.get('DATABASE_NAME')
owner_id = int(os.environ.get('OWNER_ID'))
bot_username = os.environ.get('BOT_USERNAME')

bot = TelegramClient('bot', api_id, api_hash).start(bot_token=bot_token)
client = MongoClient(db_url, tls=True)
data = Collection(client[database_name], 'ConfigDB').find_one({"_id":"GogoAnime"})

gogo = Gogo(
        gogoanime_token=data["gogoanime"],
        auth_token=data["auth"],
        host=data["url"]
    )