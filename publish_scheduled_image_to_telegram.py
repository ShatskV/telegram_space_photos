import time
from glob import glob

from fetch_nasa_apod import fetch_nasa_apod
from fetch_nasa_epic import fetch_nasa_epic
from fetch_spacex_images import fetch_spacex
from publish_image_to_telegram import send_photo_to_channel
from settings import images_directory, message_interval


def main():
    photos = glob(images_directory + '*')
    if not photos:
        fetch_nasa_apod()
    while True:
        send_photo_to_channel(rm=True)
        photos = glob(images_directory + '*')
        if not photos:
            fetch_nasa_apod()
            fetch_spacex()
            fetch_nasa_epic()
        
        time.sleep(message_interval)


if __name__ == '__main__':
    main()
