from configuration import WIFI
from pms7003 import PMS7003
from dht import DHT11
import machine

wifi = WIFI()

# TODO class should include PMS7003 changes
class Station(DHT11, PMS7003):
    """
    Example of usage:
    >>> station = Station(machine.Pin(4))
    >>> station.read_temperature()
        Temperature: 20*C
    >>> station.read_humidity()
        Humitidy: 80%
    >>> station.read_pm()
        "PM 1.0: 10 ug/m3")
        "PM 2.5: 33 ug/m3")
        "PM 10.0: 42 ug/m3")
    """
    def read_temperature(self):
        """

        :return:
        """
        self.measure()
        temp = self.temperature()
        print("Temperature: ", temp, "*C")
        return temp

    def read_humidity(self):
        """

        :return:
        """
        self.measure()
        hum = self.humidity()
        print("Humidity: ", hum, "%")
        return hum

    def read_pm(self):
        """

        :return:
        """
        pm_data = self.read()
        pm_1p0 = pm_data["PM1_0"]
        pm_2p5 = pm_data["PM2_5"]
        pm_10p0 = pm_data["PM10_0"]
        print("PM 1.0: ", pm_1p0, " ug/m3")
        print("PM 2.5: ", pm_2p5, " ug/m3")
        print("PM 10.0: ", pm_10p0, " ug/m3")
        return pm_1p0, pm_2p5, pm_10p0
