import argparse
import os

import requests

from settings import images_directory, logger
from utils import get_and_save_image_to_disk


def get_spacex_links_images(url, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    launches = response.json()
    launches = list(reversed(launches))
    for launch in launches:
        flickr_images = launch.get('links', {}).get('flickr_images', [])
        if flickr_images:
            return flickr_images


def parse_launch_id_from_terminal():
    parser = argparse.ArgumentParser(description='Задайте ID полета ракеты SpaceX:')
    parser.add_argument('flight_number', help="ID полета для скачивание фото", 
                        nargs='?', default=None)
    args = parser.parse_args()
    return args.flight_number


def fetch_spacex_last_published_images_from_launch(images_directory, flight_number=None):
    api_url = 'https://api.spacexdata.com/v3/launches'
    image_filename_template = 'space{}'
    params = {'flight_number': flight_number} if flight_number else None
    try:
        images_urls = get_spacex_links_images(api_url, params=params)
    except requests.ConnectionError as e:
        logger.error(f'url: {api_url} Connection error SpaceX: {e}')
        return
    except requests.HTTPError as e:
        logger.error(f'url: {api_url} HTTP error SpaceX: {e}')
        return

    for num, link in enumerate(images_urls, start=1):
        filepath_template = os.path.join(images_directory, image_filename_template.format(num))
        try:
            get_and_save_image_to_disk(link, filepath_template)
        except requests.ConnectionError as e:
            logger.error(f'url: {link} Connection error SpaceX: {e}')
        except requests.HTTPError as e:
            logger.error(f'url: {link} HTTP error SpaceX: {e}')
    if not images_urls:
        logger.error(f'url: {api_url} No SpaceX images found')


def main():
    flight_number = parse_launch_id_from_terminal()
    fetch_spacex_last_published_images_from_launch(images_directory, flight_number)


if __name__ == '__main__':
    main()
