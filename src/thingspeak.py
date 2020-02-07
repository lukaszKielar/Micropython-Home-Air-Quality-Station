try:
    from urllib.urequest import urlopen
except ImportError:
    from urllib.request import urlopen

from config import THINGSPEAK_API_KEY


def format_url(url, **kwargs):
    return url.format(**kwargs)


class Thingspeak:

    BASE_URL = format_url(
        url='http://api.thingspeak.com/update?api_key={thingspeak_api_key}',
        thingspeak_api_key=THINGSPEAK_API_KEY
    )
    # TODO create a function that automatically creates such path
    #  create_fields_url
    FIELDS_URL = '&field1={pm_1p0}&field2={pm_2p5}&field3={pm_10p0}&field4={temp}&field5={hum}&field6={out_temp}&field7={out_hum}&field8={out_pressure}'

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
            url=Thingspeak.FIELDS_URL,
            pm_1p0=pm_1p0,
            pm_2p5=pm_2p5,
            pm_10p0=pm_10p0,
            temp=temp,
            hum=hum,
            out_temp=out_temp,
            out_hum=out_hum,
            out_pressure=out_pressure
        )
        full_url = Thingspeak.BASE_URL + _url

        # TODO try with context manager
        try:
            urlopen(full_url)
        except Exception as e:
            print(e)
