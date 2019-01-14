import network
import machine
import ujson


class WIFIConfig:

    config_path = 'config.json'

    def __init__(self):
        with open(self.config_path) as f:
            config = ujson.load(f)
        for key, value in config.items():
            setattr(self, key, value)

    def __repr__(self):
        return "SSID: {}".format(self.ssid)


class WIFI(WIFIConfig):

    def start(self):
        wifi = network.WLAN(network.STA_IF)
        wifi.active(True)
        wifi.connect(self.ssid, self.password)  # Connect to an AP
        while not wifi.isconnected():
            machine.idle()
        print("Successfully connected to {}".format(self.ssid))

    def sendToThingspeak(self, pm_1p0, pm_2p5, pm_10p0, temp, hum):
        from urllib import urequest
        url = 'http://api.thingspeak.com/update?api_key={}&field1={}&field2={}&field3={}&field4={}&field5={}'\
                .format(self.api_key, pm_1p0, pm_2p5, pm_10p0, temp, hum)
        conn = urequest.urlopen(url)
        conn.read()
        conn.close()
