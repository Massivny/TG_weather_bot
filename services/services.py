import logging, re, requests
from aiogram.types import Message, Location
from database.models import users_db

logger = logging.getLogger(__name__)

def get_coords(msg: Message) -> dict[str: float]:
    if msg.location != None:
        longitude = msg.location.longitude
        latitude = msg.location.latitude
    else:
        match = re.search(r'([-+]?\d{1,2}\.\d+),\s*([-+]?\d{1,3}\.\d+)', msg.text)
        longitude = match.group(2)[:-2]
        latitude = match.group(1)[:-2]
    return {'latitude': latitude, 'longitude': longitude}

def get_request(id: int, loc: str) -> str:
    latitude = users_db[id][loc]['latitude']
    longitude = users_db[id][loc]['longitude']

    updates: dict = requests.get(
        f'https://api.tomorrow.io/v4/weather/forecast?location={latitude},{longitude}&apikey=XVP8767CKD5FSpgcfKxveBYNDYjswBEJ'
    ).json()

    if updates:
        ret: str = (
            f'Temperature - {updates['timelines']['minutely'][0]['values']['temperature']}°C\n'
            f'Apparent temperature - {updates['timelines']['minutely'][0]['values']['temperatureApparent']}°C\n'
            f'Atmospheric pressure - {float(updates['timelines']['minutely'][0]['values']['pressureSurfaceLevel'] * 0.75006):.2f} mmHg\n'
            f'Wind speed - {updates['timelines']['minutely'][0]['values']['windSpeed']} km\\h\n'
            f'Precipitation probability - {updates['timelines']['minutely'][0]['values']['precipitationProbability']}%\n'
        )
        return ret
    else:
        return 'Can\'t get weather update right now!\n Try later or contact support: @massivny'
    
    #updates: dict = requests.get(f'https://api.tomorrow.io/v4/weather/forecast?location={latitude},{longitude}&apikey=XVP8767CKD5FSpgcfKxveBYNDYjswBEJ').json()
    #return str(updates['timelines']['minutely'][0]['values'])