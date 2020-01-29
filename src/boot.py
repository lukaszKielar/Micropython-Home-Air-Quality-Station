# This file is executed on every boot (including wake-boot from deepsleep)
# import esp
# esp.osdebug(None)
# import webrepl
# webrepl.start()
import gc
from .wifi import Wifi


Wifi().establish_connection()
gc.collect()
