import sys
from datetime import datetime

import requests

from settings import (NASA_API_URL_BASE, NASA_IMAGE_EPIC_FILEPATH_TEMPLATE,
                      logger, nasa_token)
from utils import get_and_save_image_to_disk


def get_nasa_epic_pictures_urls(url, params):
    response = requests.get(url, params=params)
    response.raise_for_status()
    images = response.json()
    images_data = []
    for image in images:
        name = image.get('image')
        date = image.get('date')
        
        if date and name:
            date = datetime.fromisoformat(date).strftime('%Y/%m/%d')
            images_data.append({'name': name,
                                'date': date})
    return images_data


def fetch_nasa_epic_pictures(api_base_url, token, image_filepath_template):
    route_epic = '/EPIC/api/natural/images'
    route_archieve = '/EPIC/archive/natural/{date}/png/{image_name}.png'
    api_epic_url = api_base_url.format(route=route_epic)
    params = {'api_key': token}
    try:
        images_data = get_nasa_epic_pictures_urls(api_epic_url, params)
    except requests.ConnectionError as e:
        logger.error(f'url: {api_epic_url} Connection NASA EPIC error: {e}')
        return
    except requests.HTTPError as e:
        logger.error(f'url: {api_epic_url} HTTP NASA EPIC error: {e}')
        return
    api_archieve_url = api_base_url.format(route=route_archieve)
    
    for num, image in enumerate(images_data, start=1):
        filepath_template = image_filepath_template.format(num)
        url = api_archieve_url.format(date=image['date'], image_name=image['name'])
        try:
            get_and_save_image_to_disk(url, filepath_template, params=params)
        except requests.ConnectionError as e:
            logger.error(f'url: {url} Connection NASA EPIC error: {e}')
        except requests.HTTPError as e:
            logger.error(f'url: {url} HTTP NASA EPIC error: {e}')
    if not images_data:
        logger.error(f'url: {api_epic_url} No NASA EPIC images found')


def main():
    fetch_nasa_epic_pictures(NASA_API_URL_BASE, nasa_token, NASA_IMAGE_EPIC_FILEPATH_TEMPLATE)


if __name__ == '__main__':
    main()
