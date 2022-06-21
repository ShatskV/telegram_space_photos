import logging
import os
from logging.handlers import RotatingFileHandler

from dotenv import load_dotenv


load_dotenv()

bot_token = os.getenv('TELEGRAM_TOKEN')
images_directory = os.getenv('IMAGES_DIRECTORY', 'images/')
chat_id = os.getenv('TELEGRAM_CHANNEL_NAME')
nasa_token = os.getenv('NASA_TOKEN')
message_interval = int(os.getenv('MESSAGE_INTERVAL', 60*60*4))

logger = logging.getLogger('space_photo')
logger.setLevel(logging.ERROR)
log_formatter = logging.Formatter('%(asctime)s - %(filename)s %(funcName)s %(levelname)s: %(message)s')
log_handler = RotatingFileHandler('space_photos.log', maxBytes=1024*1024, backupCount=2)
log_handler.setFormatter(log_formatter)
logger.addHandler(log_handler)

SPACEX_IMAGE_FILEPATH_TEMPLATE = f'{images_directory}''space{}'

NASA_IMAGE_APOD_FILEPATH_TEMPLATE = f'{images_directory}''nasa_apod_{}'
NASA_IMAGE_EPIC_FILEPATH_TEMPLATE= f'{images_directory}''nasa_epic_{}'

NASA_API_URL_BASE = 'https://api.nasa.gov{route}'
