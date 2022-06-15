import telegram
from dotenv import load_dotenv
import os
from glob import glob
from random import choice


def main():
    load_dotenv()
    bot_token = os.getenv('TELEGRAM_TOKEN')
    images_directory = os.getenv('IMAGES_DIRECTORY', 'images/')
    chat_id = os.getenv('TELEGRAM_CHANNEL_NAME')

    bot = telegram.Bot(token=bot_token)
    
    photos_list = glob(images_directory + '*')
    pic_filename = choice(photos_list)
    # bot.send_message(chat_id='@devman_bot_channel', text="I'm sorry Dave I'm afraid I can't do that.")
    bot.send_photo(chat_id=chat_id, photo=open(pic_filename, 'rb'))

if __name__ == '__main__':
    main()