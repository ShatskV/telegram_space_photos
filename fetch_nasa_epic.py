import os
from datetime import datetime

import requests

from settings import images_directory, logger, nasa_token
from utils import get_and_save_image_to_disk


def get_nasa_epic_pictures_urls(url, params):
    response = requests.get(url, params=params)
    response.raise_for_status()
    images = response.json()
    image_names_and_dates = {}
    for image in images:
        name = image.get('image')
        date = image.get('date')
        
        if date and name:
            date = datetime.fromisoformat(date).strftime('%Y/%m/%d')
            image_names_and_dates[name] = date

    return image_names_and_dates


def fetch_nasa_epic_pictures(token, images_directory):
    api_base_url = 'https://api.nasa.gov{route}'
    route_epic = '/EPIC/api/natural/images'
    route_archieve = '/EPIC/archive/natural/{date}/png/{image_name}.png'
    image_filename_template = 'nasa_epic_{}'
    api_epic_url = api_base_url.format(route=route_epic)
    params = {'api_key': token}
    try:
        image_names_and_dates = get_nasa_epic_pictures_urls(api_epic_url, params)
    except requests.ConnectionError as e:
        logger.error(f'url: {api_epic_url} Connection NASA EPIC error: {e}')
        return
    except requests.HTTPError as e:
        logger.error(f'url: {api_epic_url} HTTP NASA EPIC error: {e}')
        return
    api_archieve_url = api_base_url.format(route=route_archieve)
    
    for num, (name, date) in enumerate(image_names_and_dates.items(), start=1):
        filepath_template = os.path.join(images_directory, image_filename_template.format(num))
        url = api_archieve_url.format(date=date, image_name=name)
        try:
            get_and_save_image_to_disk(url, filepath_template, params=params)
        except requests.ConnectionError as e:
            logger.error(f'url: {url} Connection NASA EPIC error: {e}')
        except requests.HTTPError as e:
            logger.error(f'url: {url} HTTP NASA EPIC error: {e}')
    if not image_names_and_dates:
        logger.error(f'url: {api_epic_url} No NASA EPIC images found')


def main():
    fetch_nasa_epic_pictures(nasa_token, images_directory)


if __name__ == '__main__':
    main()
