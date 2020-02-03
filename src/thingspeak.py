try:
    from urllib.urequest import urlopen
except ImportError:
    from urllib.request import urlopen

from config import THINGSPEAK_API_KEY, THINGSPEAK_BASE_URL, THINGSPEAK_FIELDS_URL


def format_url(url, **kwargs):
    return url.format(**kwargs)


class Thingspeak:

    def __init__(self):
        self._thinkspeak_base_url = format_url(
            THINGSPEAK_BASE_URL,
            thingspeak_api_key=THINGSPEAK_API_KEY
        )

    def __repr__(self):
        return 'Thingspeak()'

    def update_channel(
            self,
            pm_1p0=-999,
            pm_2p5=-999,
            pm_10p0=-999,
            temp=-999,
            hum=-999,
            out_temp=-999,
            out_hum=-999,
            out_pressure=-999
    ):
        _url = format_url(
            THINGSPEAK_FIELDS_URL,
            pm_1p0=pm_1p0,
            pm_2p5=pm_2p5,
            pm_10p0=pm_10p0,
            temp=temp,
            hum=hum,
            out_temp=out_temp,
            out_hum=out_hum,
            out_pressure=out_pressure
        )
        full_url = self._thinkspeak_base_url + _url

        # TODO try with context manager
        try:
            urlopen(full_url)
        except Exception as e:
            print(e)
