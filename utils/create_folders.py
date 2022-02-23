import pathlib
import pytz
from datetime import datetime, timezone

def date():
    tz = pytz.timezone('America/Mexico_City')
    mexico_now = datetime.now(tz)
    year = mexico_now.year
    month = mexico_now.month
    day = mexico_now.day
    hour = mexico_now.hour
    minute = mexico_now.minute
    return str(year) +'_'+ str(month) + '_'+ str(day) +'_'+ str(hour) + str(minute)

def create_path(path):
    PATH = path + '/'+ date()
    pathlib.Path(PATH).mkdir(parents=True, exist_ok=True)
    folders = ['/images','/output','/reports','/nets']
    for folder_name in folders:
        pathlib.Path(PATH + folder_name).mkdir(parents=True, exist_ok=True)
    return PATH
