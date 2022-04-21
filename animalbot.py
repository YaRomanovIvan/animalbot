import logging
import os

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
URL_CAT = 'https://api.thecatapi.com/v1/images/search'
URL_DOG = 'https://api.thedogapi.com/v1/images/search'
URL_FOX = 'https://randomfox.ca/floof/'

def check_secret_token():
    if not secret_token:
        logging.critical(f'ОШИБКА ТОКЕНА! Вы не указали токен!')
        raise TokenException('Вы не указали токен!')
    logging.info('Токен указан!')


def bot_send_message(context, chat, name):
    button = ReplyKeyboardMarkup(
        [['/newcat', '/newdog', '/newfox']],
        resize_keyboard=True
    )
    messages = [
        'Привет, {}. Я бот, который может присылать тебе разные картинки!'.format(name),
        'Я могу прислать тебе картинки лисичек, собачек и котеек!',
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


def get_new_image():



def wake_up(update, context):
    chat = update.effective_chat
    name = update.message.chat.first_name
    bot_send_message(context, chat.id, name)
    logging.info('Чат успешно запущен')


def main():
    check_secret_token()
    updater = Updater(token=secret_token)
    updater.dispatcher.add_handler(CommandHandler('start', wake_up))
    # updater.dispatcher.add_handler(CommandHandler('new_cat'))
    # updater.dispatcher.add_handler(CommandHandler('new_dog'))
    # updater.dispatcher.add_handler(CommandHandler('new_fox'))

    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()