import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hbold
from aiogram import F
from aiogram.filters import CommandStart, Command

import yt_dlp
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

dp = Dispatcher()
bot = Bot(BOT_TOKEN, parse_mode=ParseMode.HTML)

@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(
        "👋 Привет! Я — MySaveBot\n"
        "📥 Скачиваю видео из:\n"
        "• YouTube (видео и Shorts)\n"
        "• TikTok (без водяных знаков)\n"
        "• Instagram (Reels, посты, сторис)\n"
        "🔗 Просто пришли ссылку — получи видео\n"
        "❓ Помощь: /help"
    )

@dp.message(Command("help"))
async def cmd_help(message: types.Message):
    await message.answer("Просто пришли мне ссылку на видео с YouTube, TikTok или Instagram.")

@dp.message(F.text.contains("http"))
async def download_video(message: types.Message):
    url = message.text.strip()
    await message.answer("⏳ Скачиваю...")

    try:
        ydl_opts = {
            'outtmpl': 'video.%(ext)s',
            'format': 'bestvideo+bestaudio/best',
            'merge_output_format': 'mp4'
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            if not filename.endswith('.mp4'):
                filename += '.mp4'

        video = FSInputFile(filename)
        await message.answer_video(video)
        os.remove(filename)

    except Exception as e:
        logging.exception(e)
        await message.answer("⚠️ Ошибка при скачивании. Проверь ссылку или попробуй позже.")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
