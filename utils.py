import os
from pathlib import Path

import requests


def get_image_from_url(url, params=None):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
    except requests.HTTPError as e:
        return False, f'HTTP error: {e}'
    return True, response.content


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
