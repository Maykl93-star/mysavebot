import os
import logging
from aiogram import Bot, Dispatcher, types, executor
from yt_dlp import YoutubeDL
from aiohttp import ClientSession

BOT_TOKEN = os.getenv("BOT_TOKEN")
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

YDL_OPTIONS = {
    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    "outtmpl": "%(title)s.%(ext)s",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "merge_output_format": "mp4",
}


async def download_video(url: str, output_path: str = "video.mp4") -> str:
    with YoutubeDL(YDL_OPTIONS) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)


@dp.message_handler(commands=["start"])
async def start_cmd(message: types.Message):
    await message.reply("Привет! Отправь ссылку на видео с YouTube, TikTok или Instagram, и я скачаю его для тебя.")


@dp.message_handler()
async def handle_message(message: types.Message):
    url = message.text.strip()

    if not any(domain in url for domain in ["youtu", "tiktok.com", "instagram.com", "instagr.am"]):
        await message.reply("Пожалуйста, отправь ссылку на видео с YouTube, TikTok или Instagram.")
        return

    msg = await message.reply("⏬ Скачиваю видео... Подожди немного.")

    try:
        file_path = await download_video(url)
        with open(file_path, "rb") as video:
            await message.answer_video(video, caption="✅ Готово!")
        os.remove(file_path)
    except Exception as e:
        logging.exception("Ошибка при скачивании:")
        await msg.edit_text(f"❌ Не удалось скачать видео.\nОшибка: {str(e)}")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
