from datetime import datetime

import requests

from settings import (NASA_API_ROUTE_ARCHIVE, NASA_API_ROUTE_EPIC,
                      NASA_API_URL_BASE, NASA_IMAGE_EPIC_FILEPATH_TEMPLATE,
                      nasa_token)
from utils import get_and_save_image_to_disk


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


def fetch_nasa_epic():
    fetch_nasa_epic_pictures(NASA_API_URL_BASE, NASA_API_ROUTE_EPIC, NASA_API_ROUTE_ARCHIVE, nasa_token, NASA_IMAGE_EPIC_FILEPATH_TEMPLATE)


if __name__ == '__main__':
    fetch_nasa_epic()
