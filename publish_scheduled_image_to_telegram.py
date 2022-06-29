import time
import token
from glob import glob

from fetch_nasa_apod import fetch_nasa_apod_pictures
from fetch_nasa_epic import fetch_nasa_epic_pictures
from fetch_spacex_images import fetch_spacex_launch_images
from publish_image_to_telegram import send_bot_photo
from settings import (NASA_API_URL_BASE, NASA_IMAGE_APOD_FILEPATH_TEMPLATE,
                      NASA_IMAGE_EPIC_FILEPATH_TEMPLATE,
                      SPACEX_IMAGE_FILEPATH_TEMPLATE, bot_token, chat_id,
                      images_directory, message_interval, nasa_token)
from utils import rm_file


def main():
    images_directory_template = '{}*'
    while True:
        filepath = send_bot_photo(bot_token, chat_id, images_directory)
        rm_file(filepath)
        photos = glob(images_directory_template.format(images_directory))
        if not photos:
            fetch_nasa_apod_pictures(NASA_API_URL_BASE, nasa_token, NASA_IMAGE_APOD_FILEPATH_TEMPLATE)
            fetch_nasa_epic_pictures(NASA_API_URL_BASE, nasa_token, NASA_IMAGE_EPIC_FILEPATH_TEMPLATE)
            fetch_spacex_launch_images(SPACEX_IMAGE_FILEPATH_TEMPLATE)
        
        time.sleep(message_interval)


if __name__ == '__main__':
    main()
