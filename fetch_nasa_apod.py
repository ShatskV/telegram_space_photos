import os

import requests

from settings import images_directory, logger, nasa_token
from utils import get_and_save_image_to_disk


def get_nasa_apod_pictures_urls(url, params):
    response = requests.get(url, params=params)
    response.raise_for_status()
    answer = response.json()
    images_urls = []
    for picture_item in answer:
        url = picture_item.get('url')
        if url:
            images_urls.append(url)
    return images_urls


def fetch_nasa_apod_pictures(token, images_directory, count=20):
    api_url_base = 'https://api.nasa.gov{route}'
    image_filename_template = 'nasa_apod_{}'
    params = {'api_key': token,
              'count': count,
              'thumbs': True}
    apod_route = '/planetary/apod'
    api_url = api_url_base.format(route=apod_route)
    try:
        images_urls = get_nasa_apod_pictures_urls(api_url, params=params)
    except requests.ConnectionError as e:
        logger.error(f'url: {api_url} Connection error NASA APOD: {e}')
        return
    except requests.HTTPError as e:
        logger.error(f'url: {api_url} HTTP error NASA APOD: {e}')
        return
   
    for num, url in enumerate(images_urls, start=1):
        filepath_template = os.path.join(images_directory, image_filename_template.format(num))
        try:
            get_and_save_image_to_disk(url, filepath_template)
        except requests.ConnectionError as e:
            logger.error(f'url: {url} Connection error NASA APOD: {e}')
        except requests.HTTPError as e:
            logger.error(f'url: {url} HTTP error NASA APOD: {e}')
        except requests.exceptions.MissingSchema as e:
            logger.error(f'url: {url} MissingSchema error NASA APOD, bad url: {e}') 
    if not images_urls:
        logger.error(f'url: {api_url} No NASA APOD found')


def main():
    fetch_nasa_apod_pictures(nasa_token, images_directory)


if __name__ == '__main__':
    main()
