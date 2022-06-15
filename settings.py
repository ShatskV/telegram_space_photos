from dotenv import load_dotenv
import os

load_dotenv()

bot_token = os.getenv('TELEGRAM_TOKEN')
images_directory = os.getenv('IMAGES_DIRECTORY', 'images/')
chat_id = os.getenv('TELEGRAM_CHANNEL_NAME')
nasa_token = os.getenv('NASA_TOKEN')
message_interval = int(os.getenv('MESSAGE_INTERVAL', 60*60*4))

SPACEX_API_URL = 'https://api.spacexdata.com/v3/launches'

SPACEX_IMAGE_FILEPATH_TEMPLATE = f'{images_directory}''space{}'

NASA_IMAGE_APOD_FILEPATH_TEMPLATE = f'{images_directory}''nasa_apod_{}'
NASA_IMAGE_EPIC_FILEPATH_TEMPLATE= f'{images_directory}''nasa_epic_{}'

NASA_API_URL_BASE = 'https://api.nasa.gov{route}'
NASA_API_ROUTE_APOD = '/planetary/apod'
NASA_API_ROUTE_EPIC = '/EPIC/api/natural/images'
NASA_API_ROUTE_ARCHIVE = '/EPIC/archive/natural/{date}/png/{image_name}.png'