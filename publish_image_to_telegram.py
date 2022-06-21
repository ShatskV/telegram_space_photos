import os
from glob import glob
from random import choice
import argparse
import telegram

from settings import bot_token, chat_id, images_directory
from utils import rm_file


def parse_filepath_from_terminal():
    parser = argparse.ArgumentParser(description='Задайте путь файла:')
    parser.add_argument('filepath', help="Путь файла для отправки фото", 
                        nargs='?', default=None)
    args = parser.parse_args()
    return args.filepath


def send_bot_photo(token, chat_id, images_directory='images/', filepath=None):
    bot = telegram.Bot(token=token)
    if not filepath:
        photos_list = glob(images_directory + '*')
        filepath = choice(photos_list)
    bot.send_photo(chat_id=chat_id, photo=open(filepath, 'rb'))
    return filepath


def main():
    filepath = parse_filepath_from_terminal()
    filepath = send_bot_photo(bot_token, chat_id, images_directory, filepath=filepath)
    rm_file(filepath)


if __name__ == '__main__':
    main()
