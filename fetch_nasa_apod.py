import requests

from settings import (NASA_API_ROUTE_APOD, NASA_API_URL_BASE,
                      NASA_IMAGE_APOD_FILEPATH_TEMPLATE, nasa_token)
from utils import get_and_save_image_to_disk


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


def fetch_nasa_apod():
    nasa_apod_url = NASA_API_URL_BASE.format(route=NASA_API_ROUTE_APOD)
    fetch_nasa_apod_pictures(nasa_apod_url, nasa_token, NASA_IMAGE_APOD_FILEPATH_TEMPLATE)


if __name__ == '__main__':
    fetch_nasa_apod()
