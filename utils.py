import os
from pathlib import Path

import requests

from settings import logger


def rm_file(filepath):
    if os.path.isfile(filepath):
        os.remove(filepath)


def get_image_from_url(url, params=None):
    response = requests.get(url, params=params)
    response.raise_for_status()
    return response.content


def make_filepath(url, filepath_template):
    _, ext = os.path.splitext(url)
    if not ext:
        return
    return filepath_template + ext
        


def get_and_save_image_to_disk(image_url, filepath_template, params=None):
    directory = Path(filepath_template).parent
    Path(directory).mkdir(parents=True, exist_ok=True)
    image = get_image_from_url(image_url, params)
    filepath = make_filepath(image_url, filepath_template)    
    if not filepath:
        logger.error(f'url: {image_url} This is not image url')
        return
    with open(filepath, 'wb') as file:
        file.write(image)

