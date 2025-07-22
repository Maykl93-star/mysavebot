
import os
from aiogram import Bot, Dispatcher, executor, types

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.answer("👋 Привет! Просто пришли ссылку с YouTube, TikTok или Instagram — и я пришлю тебе видео.")

@dp.message_handler()
async def handle_link(message: types.Message):
    url = message.text.strip()
    await message.answer(f"🔗 Обрабатываю ссылку: {url}\n(Здесь будет скачивание...)")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
