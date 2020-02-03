import time
import machine
from dht import DHT22

from weather_api import WeatherApi
from thingspeak import Thingspeak


if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print("Woke up from deep sleep")

thingspeak = Thingspeak()
weather_api = WeatherApi()
dht22 = DHT22(machine.Pin(4))

# create data dict for data
data = {}

try:
    # wait 5 seconds
    time.sleep(5)

    # get openweathermap data
    weather_data = weather_api.get_weather_data()
    data.update(weather_data)

    # get dht22 readings
    dht22.measure()
    dht22_data = {
        'temp': dht22.temperature(),
        'hum': dht22.humidity()
    }
    data.update(dht22_data)

    # put data to thingspeak channel
    thingspeak.update_channel(**data)
    print("Channel has been updated")
except KeyboardInterrupt:
    print("Exiting...")
except Exception as e:
    print(e)
    machine.reset()

time.sleep(5)
print("Putting device into deep sleep mode")
machine.deepsleep(10000)
