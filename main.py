import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import FSInputFile
from aiogram.utils import executor
from yt_dlp import YoutubeDL

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler()
async def download_handler(message: types.Message):
    url = message.text.strip()

    if "instagram.com" in url:
        await message.answer("🔍 Скачиваю фото с Instagram...")

        ydl_opts_preview = {
            'format': 'best',
            'outtmpl': 'preview.%(ext)s',
            'noplaylist': True,
            'quiet': True,
        }

        ydl_opts_max = {
            'format': 'best',
            'outtmpl': 'full_quality.%(ext)s',
            'noplaylist': True,
            'quiet': True,
        }

        try:
            # Скачиваем и отправляем превью
            with YoutubeDL(ydl_opts_preview) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                preview_file = ydl.prepare_filename(info_dict)

            await message.answer_photo(FSInputFile(preview_file))

            # Скачиваем и отправляем оригинал
            with YoutubeDL(ydl_opts_max) as ydl:
                info_dict = ydl.extract_info(url, download=True)
                full_file = ydl.prepare_filename(info_dict)

            await message.answer_document(FSInputFile(full_file), caption="Для любителей максимального качества 📷")

            os.remove(preview_file)
            os.remove(full_file)

        except Exception as e:
            await message.answer("❌ Ошибка при скачивании Instagram фото.")
            print(e)

    else:
        await message.answer("⚠️ Поддерживаются только ссылки на Instagram фото.")

if __name__ == "__main__":
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
