import logging
import os
from aiogram import Bot, Dispatcher, executor, types
from yt_dlp import YoutubeDL

API_TOKEN = os.getenv("BOT_TOKEN")

# Включаем логирование
logging.basicConfig(level=logging.INFO)

# Инициализируем бота и диспетчер
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Настройки yt-dlp с поддержкой cookies.txt
ydl_opts = {
    'outtmpl': '%(title)s.%(ext)s',
    'format': 'bestvideo+bestaudio/best',
    'noplaylist': True,
    'cookiefile': 'cookies.txt',
    'quiet': True,
    'merge_output_format': 'mp4',
    'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
}

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("👋 Привет! Я — MySaveBot\n\n🎬 Скачиваю видео из:\n• YouTube\n• TikTok\n• Instagram\n\n🔗 Просто пришли ссылку — и получи видео!\n\n/help — инструкция")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    await message.reply(
        "📌 *Как пользоваться ботом:*
"
        "1. Скопируй ссылку на видео из YouTube, TikTok или Instagram
"
        "2. Отправь её мне сюда
"
        "3. Я пришлю тебе файл с видео или фото

"
        "🔍 *Максимальное качество:* я стараюсь скачивать видео и фото в самом высоком доступном качестве.
"
        "📸 Если доступен оригинал — отправлю его файлом.
"
        "💡 Если бот не отвечает — проверь ссылку или попробуй позже.",
        parse_mode="Markdown"
    )

@dp.message_handler()
async def download_video(message: types.Message):
    url = message.text.strip()
    await message.reply("🔄 Обрабатываю ссылку...")

    try:
        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
            filename = ydl.prepare_filename(info)
            ydl.download([url])
        with open(filename, 'rb') as video:
            await message.reply_document(video)
        os.remove(filename)
    except Exception as e:
        await message.reply(f"⚠️ Ошибка при скачивании: {e}")
