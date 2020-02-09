# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
# import webrepl
# webrepl.start()
import gc
import network
import machine
from config import SSID, PASSWORD


def establish_connection():
    wifi = network.WLAN(network.STA_IF)
    wifi.active(True)
    wifi.connect(SSID, PASSWORD)
    while not wifi.isconnected():
        machine.idle()
    print("Successfully connected to {}".format(SSID))


establish_connection()
gc.collect()
