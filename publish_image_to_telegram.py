import os
from glob import glob
from random import choice

import telegram

from settings import bot_token, chat_id, images_directory


def send_bot_photo(token, chat_id, images_directory, rm=None):
    bot = telegram.Bot(token=token)
    
    photos_list = glob(images_directory + '*')
    pic_filename = choice(photos_list)
    bot.send_photo(chat_id=chat_id, photo=open(pic_filename, 'rb'))
    if rm and (os.path.isfile(pic_filename)):
        os.remove(pic_filename)


def send_photo_to_channel(rm=None):
    send_bot_photo(bot_token, chat_id, images_directory, rm)


if __name__ == '__main__':
    send_photo_to_channel()
