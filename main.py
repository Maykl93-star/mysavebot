import os
import asyncio
import yt_dlp
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.enums import ParseMode
from aiogram.filters import Command
from aiogram.utils.markdown import hbold
from aiogram import F
from aiogram.types import Message

from dotenv import load_dotenv
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_cmd(message: Message):
    await message.answer("👋 Привет! Я — MySaveBot\nПросто пришли мне ссылку на видео с YouTube, TikTok или Instagram.\n\nКоманда помощи: /help")

@dp.message(Command("help"))
async def help_cmd(message: Message):
    text = (
        f"📌 Как пользоваться ботом:\n\n"
        f"1. Скопируй ссылку на видео из YouTube, TikTok или Instagram\n"
        f"2. Отправь эту ссылку в чат\n"
        f"3. Получи файл в лучшем доступном качестве 🎬\n\n"
        f"⚙️ Поддерживаются:\n"
        f"• YouTube (видео и Shorts)\n"
        f"• TikTok (без водяных знаков)\n"
        f"• Instagram (Reels, посты, сторис)\n\n"
        f"Если что-то не работает — попробуй снова или напиши поддержку."
    )
    await message.answer(text)

@dp.message(F.text.startswith("http"))
async def download_video(message: types.Message):
    url = message.text.strip()

    msg = await message.reply("🔄 Загружаю...")

    ydl_opts = {
        'outtmpl': 'downloads/%(title).70s.%(ext)s',
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'quiet': True,
        'noplaylist': True,
    }

    os.makedirs("downloads", exist_ok=True)

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        video = FSInputFile(filename)
        await message.reply_video(video, caption=f"{hbold('✅ Готово!')} Ваше видео сохранено в максимальном качестве.")

        await msg.delete()
        os.remove(filename)

    except Exception as e:
        await msg.edit_text(f"❌ Ошибка при загрузке:\n{e}")

if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.INFO)
    asyncio.run(dp.start_polling(bot))
