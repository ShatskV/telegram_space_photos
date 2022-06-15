import argparse

import requests

from settings import SPACEX_API_URL, SPACEX_IMAGE_FILEPATH_TEMPLATE
from utils import get_and_save_image_to_disk


def get_spacex_links_images(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        answer = response.json()
    except (requests.HTTPError, ValueError) as e:
        print(f'SpaceX API error: {e}')
        return False, None
    answer = list(reversed(answer))
    for launch in answer:
        flickr_images = launch.get('links', {}).get('flickr_images', [])
        if flickr_images:
            return True, flickr_images
    else:
        return False, 'Sorry, no links found'


def parse_url_from_terminal():
    parser = argparse.ArgumentParser(
    description='Задайте ID полета ракеты SpaceX:'
                )
    parser.add_argument('flight_number', help="ID полета для скачивание фото", nargs='?', default=None)
    args = parser.parse_args()
    flight_number = args.flight_number
    return flight_number


def fetch_spacex_launch_images(api_url, image_filepath_template, flight_number=None):
    params = None
    if flight_number:
        params = {'flight_number': flight_number}
    is_successful, answer = get_spacex_links_images(api_url, params=params)
    if not is_successful:
        print('No images found')
        return
    for num, link in enumerate(answer):
        filepath_template = image_filepath_template.format(num)
        get_and_save_image_to_disk(link, filepath_template)


def fetch_spacex(flight_number=None):
    fetch_spacex_launch_images(SPACEX_API_URL, SPACEX_IMAGE_FILEPATH_TEMPLATE, flight_number)


if __name__ == '__main__':
    flight_number = parse_url_from_terminal()
    fetch_spacex(flight_number)
