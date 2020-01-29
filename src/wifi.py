import network
import machine
from .config import SSID, PASSWORD


class Wifi:

    def establish_connection(self):
        wifi = network.WLAN(network.STA_IF)
        wifi.active(True)
        wifi.connect(SSID, PASSWORD)
        while not wifi.isconnected():
            machine.idle()
        print("Successfully connected to {}".format(SSID))

    def __repr__(self):
        return "Wifi()"
