import logging
import os

import requests

from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater

from dotenv import load_dotenv

load_dotenv()

# Подключаем логирование
# Значения параметра 'filemode':
# w - содержимое файла перезаписывается при каждом запуске программы;
# x - создать файл и записывать логи в него; если файл с таким именем уже существует — возникнет ошибка;
# s - дописывать новые логи в конец указанного файла.
logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='w',
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


SECRET_TOKEN = os.getenv('SECRET_TOKEN')
URL_CAT = 'https://api.thecatapi.com/v1/images/search'
URL_DOG = 'https://api.thedogapi.com/v1/images/search'


def get_new_image(command):
    """Функция получения URL рандомной картинки с api"""
    try:
        if command == '/newdog':
            response = requests.get(URL_DOG).json()
        else:
            response = requests.get(URL_CAT).json()
        random_animal = response[0].get('url')
        return random_animal
    except Exception as error:
        logging.error(f'API request fails! Mistake {error}')
        random_animal = requests.get('https://placebear.com/g/200/300.jpg')
        return random_animal


def new_animal(update, context):
    """Отправляем рандомную картинку с котиком/собачкой пользователю Telegram"""
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image(command=update['message']['text']))


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    button = ReplyKeyboardMarkup([['/newcat', '/newdog']], resize_keyboard=True)

    context.bot.send_message(
        chat_id=chat.id,
        text='Привет, {}. Посмотри, какого котика я тебе нашёл'.format(name),
        reply_markup=button
    )

    context.bot.send_photo(chat.id, get_new_image(command=update['message']['text']))


def main():
    updater = Updater(token=SECRET_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_animal))
    updater.dispatcher.add_handler(CommandHandler('newdog', new_animal))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
