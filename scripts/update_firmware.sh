#!/bin/bash
esptool.py --chip esp32 erase_flash
esptool.py --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 "esp32-20180511-v1.9.4.bin"