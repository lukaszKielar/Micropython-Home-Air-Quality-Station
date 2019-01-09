import time
import machine
from station import Station
from configuration import WIFI

wifi = WIFI()
station = Station()

while True:
    try:
        temp = station.read_temperature()
        hum = station.read_humidity()
        pm_1p0, pm_2p5, pm_10p0 = station.read_pm()
        try:
            wifi.sendToThingspeak(pm_1p0=pm_1p0, pm_2p5=pm_2p5, pm_10p0=pm_10p0, temp=temp, hum=hum)
        except Exception as e:
            print(e)
    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as e:
        machine.reset()
    time.sleep(600)
