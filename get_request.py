import requests
from datetime import timedelta, datetime


def get_data(date,lang,lat):
    response=requests.get(f'http://api.aladhan.com/v1/calendar?latitude={lat}&longitude={lang}&method=2&month={date[3:5]}&year={date[6:]}')
    data=response.json()
    db={lang+lat:{}}
    for i in data['data']:
        if int(i['date']['gregorian']['date'][:2])>=int(date[:2]):
            db[lang+lat][i['date']['gregorian']['date']]=i['timings']
            db[lang+lat][i['date']['gregorian']['date']]['hijriy']=i['date']['hijri']['date']
    db[lang+lat]['tz']=data['data'][0]['meta']['timezone']
    return db
