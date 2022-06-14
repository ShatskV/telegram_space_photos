import argparse
import os
from datetime import datetime
from pathlib import Path

import requests
from dotenv import load_dotenv

SPACEX_API_URL = 'https://api.spacexdata.com/v3/launches'
SPACEX_API_ROUTE_LATEST = '/latest'

SPACEX_IMAGE_FILEPATH_TEMPLATE = 'images/space{}'
NASA_IMAGE_APOD_FILEPATH_TEMPLATE = 'images/nasa_apod_{}'
NASA_IMAGE_EPIC_FILEPATH_TEMPLATE= 'images/nasa_epic_{}'


NASA_API_URL_BASE = 'https://api.nasa.gov{route}'
NASA_API_ROUTE_APOD = '/planetary/apod'
NASA_API_ROUTE_EPIC = '/EPIC/api/natural/images'
NASA_API_ROUTE_ARCHIVE = '/EPIC/archive/natural/{date}/png/{image_name}.png'


def get_image_from_url(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.HTTPError as e:
        return False, f'HTTP error: {e}'
    return True, response.content


def get_spacex_links_images(url):
    try:
        response = requests.get(url)
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


def get_nasa_apod_pictures_urls(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        answer = response.json()
    except (requests.HTTPError, ValueError) as e:
        print(f'Nasa apod API error: {e}')
        return False, None
    images_urls = []
    for picture_item in answer:
        url = picture_item.get('url')
        if url:
            images_urls.append(url)
    return True, images_urls


def get_nasa_epic_pictures_urls(url, params):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        answer = response.json()
    except (requests.HTTPError, ValueError) as e:
        print(f'Nasa EPIC API error: {e}')
        return False, None
    images_data = []
    for image in answer:
        name = image.get('image')
        date = image.get('identifier')
        
        if date and name:
            date = datetime.strptime(str(date)[:8], '%Y%m%d')
            date = date.strftime('%Y/%m/%d')
            images_data.append({'name':name,
                                'date': date})
    return True, images_data


def parse_terminal_commands():
    parser = argparse.ArgumentParser(description='Описание что делает программа:\n'
                                "Загрузка фото с выбранного ресурса")
    
    parser.add_argument("-a", "--api", choices=['spacex', 'apod', 'epic'], help="Выбор ресурса для скачивания фото "
                        "в папку 'images'", default="apod")
    
    args = parser.parse_args()
    return args


def fetch_nasa_epic_pictures(api_base_url, route_epic, route_archieve, token, image_filepath_template):
    api_epic_url = api_base_url.format(route=route_epic)
    params = {'api_key': token}
    is_successful, images_data = get_nasa_epic_pictures_urls(api_epic_url, params)

    if is_successful:
        api_archieve_url = NASA_API_URL_BASE.format(route=route_archieve)
        for num, image in enumerate(images_data, start=1):
            filepath_template = image_filepath_template.format(num)
            url = api_archieve_url.format(date=image['date'], image_name=image['name'])
            get_and_save_image_to_disk(url, filepath_template, params=params)

    else:
        print('No images found')


def fetch_nasa_apod_pictures(api_url, token, image_filepath_template, count=20):
    params = {'api_key': token,
              'count': count,
              'thumbs': True}
    is_successful, images_urls = get_nasa_apod_pictures_urls(api_url, params=params)
    if is_successful:
        for num, url in enumerate(images_urls, start=1):
            filepath_template = image_filepath_template.format(num)
            get_and_save_image_to_disk(url, filepath_template)
    else:
        print('No images found')
    

def get_and_save_image_to_disk(image_url, filepath_template, params=None):
    directory = Path(filepath_template).parent
    Path(directory).mkdir(parents=True, exist_ok=True)
    is_successful, answer = get_image_from_url(image_url, params)
    if is_successful:
        _, ext = os.path.splitext(image_url)
        if ext:
            filepath = filepath_template + ext
            with open(filepath, 'wb') as file:
                file.write(answer)
    else:
        print(answer)


def fetch_spacex_last_launch(base_url, latest_route, image_filepath_template):
    is_successful, answer = get_spacex_links_images(base_url)
    if not is_successful:
        is_successful, answer = get_spacex_links_images(base_url + latest_route)
        if not is_successful:
            print('No images found')
            return
    for num, link in enumerate(answer):
        filepath_template = image_filepath_template.format(num)
        get_and_save_image_to_disk(link, filepath_template)


def main():
    load_dotenv()
    nasa_token = os.getenv('NASA_TOKEN')
    nasa_apod_url = NASA_API_URL_BASE.format(route=NASA_API_ROUTE_APOD)
    args = parse_terminal_commands()
    api_choice = args.api
    if api_choice == 'spacex':
        fetch_spacex_last_launch(SPACEX_API_URL, SPACEX_API_ROUTE_LATEST, SPACEX_IMAGE_FILEPATH_TEMPLATE)
    elif api_choice == 'apod':
        fetch_nasa_apod_pictures(nasa_apod_url, nasa_token, NASA_IMAGE_APOD_FILEPATH_TEMPLATE)
    else:
        fetch_nasa_epic_pictures(NASA_API_URL_BASE, NASA_API_ROUTE_EPIC, NASA_API_ROUTE_ARCHIVE, nasa_token, NASA_IMAGE_EPIC_FILEPATH_TEMPLATE)
    

if __name__ == '__main__':
    main()
