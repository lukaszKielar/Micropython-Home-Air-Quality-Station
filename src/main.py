import time
import machine
from dht import DHT22

from pms7003 import PassivePms7003, UartError
from thingspeak import Thingspeak
from weather_api import WeatherApi


if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print("Woke up ESP32 from deep sleep")


dht22 = DHT22(machine.Pin(4))
pms7003 = PassivePms7003(uart=2)
thingspeak = Thingspeak()
weather_api = WeatherApi()

# create data dict for data
data = {}

try:
    # wake up pms7003
    print("Waking up pms7003 from sleep mode")
    pms7003.wakeup()

    # wait 60 seconds to stabilize airflow
    print("Sleep 60 seconds to stabilize airflow")
    time.sleep(60)

    # get openweathermap data
    print("Getting OWM data")
    data.update(weather_api.get_weather_data())

    # get dht22 readings
    print("Getting dht22 data")
    dht22.measure()
    data.update({
        'temp': dht22.temperature(),
        'hum': dht22.humidity()
    })

    # get pms7003 readings
    print("Getting pms7003 data")
    pms7003_data = pms7003.read()
    data.update({
        'pm_1p0': pms7003_data.get('PM1_0', -999),
        'pm_2p5': pms7003_data.get('PM2_5', -999),
        'pm_10p0': pms7003_data.get('PM10_0', -999),
    })

    # put pms7003 into sleep mode
    print("Putting pms7003 into sleep mode")
    # sleep method usually fails when it's executed after `wakeup()` method
    # in order to avoid issues we have to use try-except block
    try:
        pms7003.sleep()
    except UartError:
        print("Pms7003 sleep response failed, but device has been put into sleep mode")

    # put data to thingspeak channel
    print("Putting data to Thingspeak channel")
    thingspeak.update_channel(**data)
    print("Channel has been updated")

    print("Putting ESP32 into deep sleep mode for 10 minutes")
    machine.deepsleep(600_000)
except KeyboardInterrupt:
    print("Exiting...")
except Exception as e:
    print(e)
    machine.reset()
