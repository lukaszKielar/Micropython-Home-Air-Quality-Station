try:
    from urllib.urequest import urlopen
    import ujson
except ImportError:
    from urllib.request import urlopen
    import json as ujson

from config import OWM_API_KEY, OWM_CITY_ID


def format_url(url, **kwargs):
    return url.format(**kwargs)


class WeatherApi:

    BASE_URL = 'http://api.openweathermap.org/data/2.5/weather?id={city_id}&units=metric&APPID={own_api_key}'

    def __init__(self, city_id=OWM_CITY_ID):
        self._city_id = city_id
        self._url = format_url(
            url=WeatherApi.BASE_URL,
            city_id=city_id,
            own_api_key=OWM_API_KEY
        )

    def __repr__(self):
        return 'WeatherApi(city_id={})'.format(self._city_id)

    def _get_data(self):
        request = urlopen(self._url)
        return ujson.load(request)

    def get_weather_data(self):
        try:
            data = self._get_data()['main']
        except Exception as e:
            print(e)
            data = {}
        return {
            "out_temp": data.get('temp', -999),
            "out_hum": data.get('humidity', -999),
            "out_pressure": data.get('pressure', -999),
        }
