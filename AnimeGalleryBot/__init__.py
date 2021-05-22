from telethon import TelegramClient
import os

api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
bot_token = os.environ.get('BOT_TOKEN')

tg_client = TelegramClient('bot1', api_id, api_hash).start(bot_token=bot_token)
