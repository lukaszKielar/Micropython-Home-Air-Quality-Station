import time
import machine
from dht import DHT11
from pms7003 import PMS7003
from configuration import WIFI

wifi = WIFI()
dht = DHT11(machine.Pin(4))
pms = PMS7003()

reset_value = 0


def read_pm():
    """

    :return:
    """
    pm_data = pms.read()
    pm_1p0 = pm_data["PM1_0"]
    pm_2p5 = pm_data["PM2_5"]
    pm_10p0 = pm_data["PM10_0"]
    print("PM 1.0: ", pm_1p0, " ug/m3")
    print("PM 2.5: ", pm_2p5, " ug/m3")
    print("PM 10.0: ", pm_10p0, " ug/m3")
    return pm_1p0, pm_2p5, pm_10p0


while True:
    if reset_value == 12:
        machine.reset()
    try:
        dht.measure()
        temp = dht.temperature()
        print("Temperature: ", temp, "*C")
        hum = dht.humidity()
        print("Humidity: ", hum, "%")
        pm_1p0, pm_2p5, pm_10p0 = read_pm()
        try:
            wifi.sendToThingspeak(pm_1p0=pm_1p0, pm_2p5=pm_2p5, pm_10p0=pm_10p0, temp=temp, hum=hum)
        except Exception as e:
            print(e)
    except KeyboardInterrupt:
        print("Exiting...")
        break
    except Exception as e:
        print(e)
        machine.reset()
    reset_value += 1
    time.sleep(600)
