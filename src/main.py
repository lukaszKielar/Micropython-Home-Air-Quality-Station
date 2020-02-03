import time
import machine

from weather_api import WeatherApi
from thingspeak import Thingspeak


if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print("Woke up from deep sleep")

thingspeak = Thingspeak()
weather_api = WeatherApi()

try:
    weather_data = weather_api.get_weather_data()
    thingspeak.update_channel(**weather_data)
    print("Channel has been updated")
except KeyboardInterrupt:
    print("Exiting...")
except Exception as e:
    print(e)
    machine.reset()

time.sleep(5)
print("Putting device into deep sleep mode")
machine.deepsleep(10000)
