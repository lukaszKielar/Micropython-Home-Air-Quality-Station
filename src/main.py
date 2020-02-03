import time
from weather_api import WeatherApi
from thingspeak import Thingspeak


while True:
    thingspeak = Thingspeak()
    weather_api = WeatherApi()

    try:
        weather_data = weather_api.get_weather_data()
        thingspeak.update_channel(**weather_data)
    except KeyboardInterrupt:
        print('Exiting...')
        break
    # TODO use machine.reset()
    except Exception as e:
        print(e)
        break

    time.sleep(30)
