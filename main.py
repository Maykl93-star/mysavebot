import os
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.utils import executor
import yt_dlp

# Настройки логирования
logging.basicConfig(level=logging.INFO)

# Токен Telegram-бота
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

# YDL Опции (лучшее качество без водяных знаков)
ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'quiet': True,
    'merge_output_format': 'mp4',
    'noplaylist': True
}

# Обработчик команд
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: Message):
    await message.reply("Привет! Отправь мне ссылку на видео с YouTube, Instagram или TikTok, и я скачаю его для тебя без водяных знаков в лучшем качестве.")

# Обработчик ссылок
@dp.message_handler(lambda message: any(domain in message.text for domain in ["youtu", "instagram", "tiktok"]))
async def download_video(message: Message):
    url = message.text.strip()
    await message.reply("🔄 Загружаю видео, подожди пару секунд...")

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            ydl.download([url])

        with open(filename, "rb") as video:
            await message.reply_document(video)

        os.remove(filename)

    except Exception as e:
        logging.exception("Ошибка при загрузке")
        await message.reply("❌ Ошибка при загрузке видео. Убедись, что ссылка рабочая.")

# Запуск
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
