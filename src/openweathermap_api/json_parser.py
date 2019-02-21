from typing import Dict, Any

import os
import json
import time
from datetime import datetime
import requests
from openweathermap_api.settings import OWM_API_KEY, THINGSPEAK_API_KEY

OK_CODE = 200


class Weather_API:

    OWM_URL = "http://api.openweathermap.org/data/2.5/weather?id={city_id}&units=metric&APPID={OWM_API_KEY}"
    THINKSPEAK_URL = "http://api.thingspeak.com/update?api_key={THINGSPEAK_API_KEY}&field6={temp}&field7={hum}&field8={pressure}"
    temp = -7777
    hum = -7777
    pressure = -7777

    def __init__(self, city_id: int = 3094802) -> None:
        self.city_id = city_id
        self.OWM_URL = self.OWM_URL.format(city_id=self.city_id,
                                           OWM_API_KEY=OWM_API_KEY)

    def __str__(self) -> str:
        return """City ID: {city_id}""".format(city_id=self.city_id)

    def _get(self) -> Dict[str, Any]:
        return requests.get(self.OWM_URL).json()

    # TODO save only readings and timestamp
    def _save(self, output_folder: str = './data') -> None:
        filename = '{city_id}_{datetime}.json'.format(city_id=self.city_id,
                                                      datetime=datetime.now().strftime("%Y%m%d%H%M"))
        output_path = os.path.join(output_folder, filename)
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        with open(output_path, 'w') as f:
            json.dump(self._get(), f)

    def _open_json(self, json_path: str) -> None:
        with open(json_path, 'r') as f:
            return json.load(f)

    def _get_weather(self) -> Dict[str, int]:
        weather = self._get()
        readings = {
            "temp": weather['main']['temp'],
            "pressure": weather['main']['pressure'],
            "hum": weather['main']['humidity']
        }
        return readings

    def _send_to_thingspeak(self):
        try:
            url = self.THINKSPEAK_URL.format(THINGSPEAK_API_KEY=THINGSPEAK_API_KEY,
                                             temp=self.temp,
                                             hum=self.hum,
                                             pressure=self.pressure)
            conn = requests.post(url)
            if conn.status_code != OK_CODE:
                print("Cannot send the data. Errno: {}".format(conn.status_code))
            else:
                print("Data successfully pushed to the API.")
        except Exception as e:
            print(e)
        finally:
            conn.close()
            self._save()


class Weather(Weather_API):

    def __init__(self) -> None:
        super().__init__()
        for key, value in self._get_weather().items():
            setattr(self, key, value)

    def __str__(self) -> str:
        print(Weather_API().__str__())
        return """Temp: {}\nHum: {}\nPressure: {}""".format(self.temp, self.hum, self.pressure)


if __name__ == '__main__':
    api = Weather_API()
    print(api)
    while True:
        try:
            api = Weather()
            api._send_to_thingspeak()
        except Exception as e:
            print(e)
            break
        except KeyboardInterrupt:
            print("Keyboard interruption. Exiting...")
            break
        else:
            time.sleep(120)
