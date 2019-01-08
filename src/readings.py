from configuration import WIFI
from pms7003 import PMS7003
from dht import DHT11
import machine

wifi = WIFI()


# TODO finish class configuration
class Reading(PMS7003, DHT11):
    pass


def readFromDHT():
    dht = DHT11(machine.Pin(4))
    dht.measure()
    temp = dht.temperature()
    hum = dht.humidity()
    print("Temperature: ", temp)
    print("Humidity: ", hum)
    return temp, hum


def readFromPMS():
    pms = PMS7003()
    data = pms.read()
    pm_1p0 = data["PM1_0"]
    pm_2p5 = data["PM2_5"]
    pm_10p0 = data["PM10_0"]
    print("PM 1.0: ", pm_1p0)
    print("PM 2.5: ", pm_2p5)
    print("PM 10.0: ", pm_10p0)
    return pm_1p0, pm_2p5, pm_10p0


