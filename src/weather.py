try:
    from urllib.urequest import urlopen
    import ujson
except ImportError:
    from urllib.request import urlopen
    import json as ujson

from config import OWM_API_KEY, OWM_CITY_ID, OWM_URL


def format_url(url, **kwargs):
    return url.format(**kwargs)


class WeatherApi:

    def __init__(self, city_id=OWM_CITY_ID):
        self._city_id = city_id
        self._url = format_url(OWM_URL, city_id=city_id, own_api_key=OWM_API_KEY)

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
