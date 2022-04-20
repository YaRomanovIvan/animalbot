import requests
import logging
import os

from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup
from telegram.ext import CommandHandler, Updater


# Подключаем логирование
# Значения параметра 'filemode':
# w - содержимое файла перезаписывается при каждом запуске программы;
# x - создать файл и записывать логи в него; если файл с таким именем уже существует — возникнет ошибка;
# s - дописывать новые логи в конец указанного файла.
logging.basicConfig(
    level=logging.DEBUG,
    filename='main.log',
    filemode='w'
)

load_dotenv()
SECRET_TOKEN = os.getenv('SECRET_TOKEN')
URL_CAT = 'https://api.thecatapi.com/v1/images/search'
URL_DOG = 'https://api.thedogapi.com/v1/images/search'


def get_new_image(command):
    """Функция получения URL рандомной картинки с api"""
    if command == '/newdog':
        response = requests.get(URL_DOG).json()
    elif command == '/newcat':
        response = requests.get(URL_CAT).json()
    random_cat = response[0].get('url')
    return random_cat


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

    context.bot.send_photo(chat.id, get_new_image())


def main():
    updater = Updater(token=SECRET_TOKEN)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_animal))
    updater.dispatcher.add_handler(CommandHandler('newdog', new_animal))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
