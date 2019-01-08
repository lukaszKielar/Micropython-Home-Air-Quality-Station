import time
import machine
import readings
from configuration import WIFI

wifi = WIFI()

while True:
    try:
        temp, hum = readings.readFromDHT()
        pm_1p0, pm_2p5, pm_10p0 = readings.readFromPMS()
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
