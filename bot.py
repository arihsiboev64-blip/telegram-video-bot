import asyncio
import os
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import yt_dlp

# Твой новый токен
TOKEN = '8880577681:AAGbcwumErHePOll0rIczTsqYnbY9iQqzhc'

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Функция для скачивания (настройка для работы с разными соцсетями)
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("👋 Привет! Я готов. Пришли мне ссылку на видео из Instagram, TikTok или YouTube.")

@dp.message(F.text.contains("http"))
async def process_link(message: types.Message):
    # Отправляем уведомление, что начали
    status_msg = await message.answer("⏳ Скачиваю видео, подожди пару секунд...")
    
    try:
        # Скачиваем в фоне
        await asyncio.to_thread(download_video, message.text)
        
        # Отправляем видео пользователю
        video = types.FSInputFile("video.mp4")
        await message.answer_video(video)
        
        # Удаляем временный файл
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")
            
        await status_msg.delete()
        
    except Exception as e:
        await message.answer(f"❌ Ошибка: не удалось скачать видео.\nПроверь ссылку. Детали: {e}")
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")

async def main():
    print("Бот успешно запущен и ждет ссылок!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())