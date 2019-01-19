import time
import machine
from connect import WIFI
from pms7003 import PMS7003
from dht import DHT11

wifi = WIFI()
pms = PMS7003()

count = 0

while True:
    if count == 12:
        machine.reset()
    try:
        data = pms.read()
        pm_1p0 = data["PM1_0"]
        pm_2p5 = data["PM2_5"]
        pm_10p0 = data["PM10_0"]
        print("PM 1.0: ", pm_1p0)
        print("PM 2.5: ", pm_2p5)
        print("PM 10.0: ", pm_10p0)
        dht = DHT11(machine.Pin(4))
        dht.measure()
        temp = dht.temperature()
        hum = dht.humidity()
        print("Temperature: ", temp)
        print("Humidity: ", hum)
        try:
            wifi.sendToThingspeak(pm_1p0=pm_1p0, pm_2p5=pm_2p5, pm_10p0=pm_10p0, temp=temp, hum=hum)
        except Exception as e:
            print(e)
    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as e:
        machine.reset()
    count += 1
    time.sleep(600)
