import logging
import os
import re

from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, FSInputFile
from aiogram.enums import ParseMode
from aiogram.utils.markdown import hlink
from yt_dlp import YoutubeDL
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)
dp = Dispatcher()

INSTAGRAM_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}
COOKIES_FILE = "cookies.txt"

HELP_TEXT = (
    "📥 Просто пришли ссылку на видео:\n"
    "• YouTube (видео и Shorts)\n"
    "• TikTok (без водяных знаков)\n"
    "• Instagram (Reels, посты, сторис)\n\n"
    "🖼 Фото Instagram отправляется как файл — нажми по нему для максимального качества.\n\n"
    "❓ /help — помощь"
)

@dp.message(F.text == "/start")
@dp.message(F.text == "/help")
async def help_message(message: Message):
    await message.answer(HELP_TEXT)

@dp.message(F.text)
async def download_video(message: Message):
    url = message.text.strip()

    if not url.startswith(("http://", "https://")):
        await message.answer("Пожалуйста, отправь действительную ссылку на видео.")
        return

    temp_file = "video.mp4"
    ydl_opts = {
        "outtmpl": temp_file,
        "quiet": True,
        "no_warnings": True,
        "cookies": COOKIES_FILE,
        "http_headers": INSTAGRAM_HEADERS,
        "merge_output_format": "mp4",
    }

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            if "title" in info:
                title = info["title"]
            else:
                title = "video"
    except Exception as e:
        await message.answer("⚠️ Ошибка при загрузке. Возможно, ссылка недействительна или профиль закрыт.")
        print(e)
        return

    if os.path.exists(temp_file):
        video = FSInputFile(temp_file)
        await message.answer_video(video, caption=f"🎬 {title}")
        os.remove(temp_file)
    else:
        await message.answer("⚠️ Не удалось найти загруженное видео.")

if __name__ == "__main__":
    dp.run_polling(bot)
