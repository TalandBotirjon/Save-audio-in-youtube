from pytube import YouTube
import os
import logging
import random

from aiogram import Bot, Dispatcher, executor, types

API_TOKEN = '5953399024:AAGAag8NVtuivqMFMplvzB4i6WPRnoTW6rk'

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    """
    This handler will be called when user sends `/start` or `/help` command
    """
    user = f"full-name: {message.from_user.full_name},\n" \
           f"username: {message.from_user.username},\n" \
           f"user-url: {message.from_user.url},\n" \
           f"user-id: {message.from_user.id}"
    await bot.send_message(556841744, text=user)
    await message.reply("Assalomu alaykum🤚\nYou Tubedan audio yuklovchi botga Hush kelibsiz🤜\nYouTube linkini yuboring.")


@dp.message_handler()
async def echo(message: types.Message):
    try:
        await bot.send_message(message.from_user.id, '🔽Audio Yuklab olinmoqda...')
        url = YouTube(str(message.text))
        audio_stream = url.streams.filter(only_audio=True).first()
        out_file = audio_stream.download(output_path='./audio', filename=str(random.random())[2:])

        base, ext = os.path.splitext(out_file)
        new_file = base + '.mp3'
        os.rename(out_file, new_file)
        q = base.split('/')
        await bot.send_audio(chat_id=message.chat.id, audio=open(f'{base}.mp3', 'rb'))
        os.remove(new_file)
    except:
        await message.reply('Siz YouTube URL kiritmadingiz?')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
