# TODO split all classes into separate module
import ujson
from urllib import urequest


# TODO move to separate module
class Thingspeak:

    # TODO move to thinkspeak_config.json
    THINKSPEAK_URL = 'http://api.thingspeak.com/update?api_key={}&field1={}&field2={}&field3={}&field4={}&field5={}&field6={}&field7={}&field8={}'

    def __init__(self):
        super().__init__()

    # TODO first of all test with PMS7003 only
    def _send(self,
              pm_1p0=-999,
              pm_2p5=-999,
              pm_10p0=-999,
              temp=-999,
              hum=-999,
              out_temp=-999,
              out_hum=-999,
              out_pressure=-999):
        try:
            url = self.THINKSPEAK_URL.format(self.thinkspeak_api_key,
                                             pm_1p0,
                                             pm_2p5,
                                             pm_10p0,
                                             temp,
                                             hum,
                                             out_temp,
                                             out_hum,
                                             out_pressure)
            conn = urequest.urlopen(url)
            conn.read()
        except Exception as e:
            print(e)
        finally:
            conn.close()


# TODO move to separate module
class Weather_API:

    # TODO move to weather_config.json
    OWM_URL = "http://api.openweathermap.org/data/2.5/weather?id={city_id}&units=metric&APPID={owm_api_key}"

    def __init__(self, city_id=3094802):
        super().__init__()
        self.city_id = city_id
        self.OWM_URL = self.OWM_URL.format(city_id=self.city_id, owm_api_key=self.owm_api_key)

    def __repr__(self):
        return """City ID: {city_id}""".format(city_id=self.city_id)

    def __str__(self):
        return self.__repr__()

    def _get(self):
        try:
            conn = urequest.urlopen(self.OWM_URL)
            return ujson.load(conn)
        except Exception as e:
            print(e)
        finally:
            conn.close()

    def _get_weather(self):
        weather = self._get()
        try:
            readings = {
                "out_temp": weather['main']['temp'],
                "out_hum": weather['main']['humidity'],
                "out_pressure": weather['main']['pressure']
            }
            return readings
        except Exception as e:
            print(e)
            return {
                "out_temp": -999,
                "out_hum": -999,
                "out_pressure": -999
            }


class Weather(Weather_API):

    def __init__(self):
        super().__init__()
        for key, value in self._get_weather().items():
            setattr(self, key, value)

    def __repr__(self):
        return """Temp: {}\nHum: {}\nPressure: {}""".format(self.out_temp, self.out_hum, self.out_pressure)

    def __str__(self):
        return self.__repr__()
