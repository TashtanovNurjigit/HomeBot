from aiogram import types
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, UserProfilePhotos
from aiogram.utils import executor
from Config import bot, dp
import logging
import re


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    me = await bot.get_me()
    await message.answer(f'Вас приветствует {me.first_name}')


@dp.message_handler(commands=['help'])
async def help(message: types.Message):
    await message.answer(f'Этот принимает команды: \n /my_info \n /download_photo \n /show_movies \n /send_my_info')


# my_info - выводит id, first_name, last_name
@dp.message_handler(commands=['my_info'])
async def my_info(message: types.Message):
    Id = message.from_user.id
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    await message.answer(f'Ваше имя: {first_name} \n Ваша фамилия: {last_name} \n Ваш ID: {Id}')


# download_photo - скачивает аватарку пользователя и   открывает этот файл
@dp.message_handler(commands=['download_photo'])
async def download_photo(message: types.Message):
    user_profile_photo: UserProfilePhotos = await bot.get_user_profile_photos(message.from_user.id)
    if len(user_profile_photo.photos[0]) > 0:
        file = await bot.get_file(user_profile_photo.photos[0][0].file_id)
        await bot.download_file(file.file_path, 'media/user profile photo.png')
        photo = open('media/user profile photo.png', 'rb')
        await bot.send_photo(message.chat.id, photo)
    else:
        await message.answer('У вас нет фото профиля')


# show_movies - бот отправляет список фильмов с их названиями и ссылкой на сайт с этими фильмами
@dp.message_handler(commands=['show_movies'])
async def show_movies(message: types.Message):
    await message.answer(f''
                         f'Мстители финал: \n https://kinokong.pro/34893-films-mstiteli-final-2019.html \n'
                         f'Твое имя: \n https://yummyanime.tv/86-tvoe-imja.html \n'
                         f'OreGairu: \n https://yummyanime.tv/211-kak-i-ozhidalos-moja-shkolnaja-romanticheskaja-zhizn-ne-udalas.html')


# send_my_info - пользователь пишет свое имя, фамилия, возраст, чем занимается и список любимых фильмов или сериалов и бот группирует
@dp.message_handler(commands=['send_my_info'])
async def send_my_info(message: types.Message):
    name = None
    surname = None
    age = None
    hobby = None
    favourite_film = None
    await message.answer(f''
                         f'Напишите о себе строго по следующему шаблону:\n'
                         f'1 Ваше имя\n'
                         f'2 Ваша фамилия\n'
                         f'3 Ваш возраст\n'
                         f'4 Чем вы занимаетесь(Хобби)\n'
                         f'5 Ваши любимые фильмы\n')

    @dp.message_handler()
    async def get_info(message: types.Message):
        info_user = message.text
        name = re.findall(r'1 \w+', info_user)
        surname = re.findall(r'2 \w+', info_user)
        age = re.findall(r'3 \w+', info_user)
        hobby = re.findall(r'4 \w+', info_user)
        favourite_film = re.findall(r'5 \w+', info_user)
        await message.answer(f''
                             f'Ваше имя: {name[0][2:]}\n'
                             f'Ваша фамилия: {surname[0][2:]}\n'
                             f'Ваш возраст: {age[0][2:]}\n'
                             f'Вы занимаетесь {hobby[0][2:]}\n'
                             f'Ваши любимые фильмы: {favourite_film[0][2:]}\n'
                             )


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, skip_updates=True)
