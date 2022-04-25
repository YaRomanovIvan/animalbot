import logging
import os

import requests

from exceptions import TokenException
from telegram import ReplyKeyboardMarkup
from telegram.ext import Updater, CommandHandler
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    filename='main.log',
    filemode='w',
    format='%(asctime)s - %(levelname)s - %(message)s - %(name)s'
)

secret_token = os.getenv('SECRET_TOKEN')
URL_ANIMAL = {
    '/newcat': 'https://api.thecatapi.com/v1/images/search',
    '/newdog': 'https://api.thedogapi.com/v1/images/search',
}


def check_secret_token():
    """Проверка наличия секретного токена"""
    if not secret_token:
        logging.critical(f'ОШИБКА ТОКЕНА! Вы не указали токен!')
        raise TokenException('Вы не указали токен!')
    logging.info('Токен указан!')


def bot_send_message(context, chat, name):
    """Функция 'привет' от бота при команде start"""
    button = ReplyKeyboardMarkup(
        [['/newcat', '/newdog']],
        resize_keyboard=True
    )
    messages = [
        'Привет, {}. Я бот, который может присылать тебе разные картинки!'.format(name),
        'Я могу прислать тебе картинки собачек и котеек!',
        'Потрясающе не правда-ли?)',
        'Попробуй нажать на кнопку и убедись в этом!'
    ]
    for message in messages:
        context.bot.send_message(
            chat_id=chat,
            text=message,
            reply_markup=button
        )
    logging.info('Сообщения бота при /start успешно отправлены')


def get_new_image(url):
    """Получение нового изображения. Ф-ия принимает текст сообщения из чата и вызывает URL API по ключу."""
    try:
        response = requests.get(URL_ANIMAL[url])
        random_animal = response.json()[0].get('url')
        logging.info('Новое изображение отправлено!')
        return random_animal
    except Exception as error:
        logging.error(f'Ошибка API при отправке изображения! {error}')
        response = requests.get('https://randomfox.ca/floof/').json()
        return response['image']


def new_animal(update, context):
    """Отправляем рандомную картинку с котиком/собачкой пользователю Telegram"""
    chat = update.effective_chat
    context.bot.send_photo(chat.id, get_new_image(update.message.text))


def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    bot_send_message(context, chat.id, name)
    logging.info('Чат успешно запущен')


def main():
    check_secret_token()
    updater = Updater(token=secret_token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    updater.dispatcher.add_handler(CommandHandler('newcat', new_animal))
    updater.dispatcher.add_handler(CommandHandler('newdog', new_animal))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
