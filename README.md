# ESP32 MicroPython setup
## Software
* Python 3 distribution (i.e. Miniconda/Anaconda) with following libraries:
    * esptool - `pip install esptool`
    * adafruit-ampy - `pip install adafruit-ampy`
* USB to UART drivers:
  * CH340 - [download](https://sparks.gogo.co.nz/ch340.html)
  * PL2303 - [download](http://www.prolific.com.tw/US/ShowProduct.aspx?pcid=41&showlevel=0041-0041)
  * CP210X - [download](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers)
* Latest ESP32 firmware - [download](http://micropython.org/download#esp32)

## Hardware
* ESP32 (i.e. DOIT ESP32 DevKit v1)
* Plantower PMS7003 air quality sensor
* USB-UART PL2303
* USB cable
* jumping wires
* breadboard

### Optionally
* temperature/humidity/pressure sensor (i.e. DS18B20, DHT11, BME280)
* RTC
* SSD1303 OLED display

## Preparing the board
### Check COM PORT
Let's plug ESP32 into computer and check whether everything was installed correctly and board is visible by our machine. Running following command in the terminal `ls /dev/tty*USB*` should return ESP32 COM PORT (i.e. `/dev/ttyUSB0` on Linux or `/dev/tty.SLAB_USBtoUART` on MacOS). If nothing shows up make sure you have installed software correctly.
### Erase flash
To make sure that everything is up to date we should erase flash on ESP32 running following command `python -m esptool --chip esp32 erase_flash`. It should automatically find COM PORT.
### Write latest firmware
When our flash was erased we can write latest firware to our board using command `python -m esptool --chip esp32 --port /dev/tty* write_flash -z 0x1000 path/to/esp32/firmware.bin`. Double check ***port*** and ***downloaded firmware path***.
`python -m esptool --chip esp32 --port /dev/ttyUSB0 write_flash -z 0x1000 /home/lukasz/Downloads/esp32-20180511-v1.9.4.bin`
`esptool.py --port /dev/ttyUSB0 --baud 115200 write_flash --flash_size=detect 0 /home/lukasz/Downloads/esp8266-20180511-v1.9.4.bin`
### Check REPL
`screen /dev/ttyUSB0 115200`
### Check files on bread
`ampy -p /dev/ttyUSB0 ls`
### Put file on board
`ampy --port=/dev/ttyUSB0 put file.py`
### Run file
`ampy --port=/dev/ttyUSB0 run file.py`

## Install micropython libraries
1. Connect to REPL
2. Connect to the Internet
`import upip`
`upip.install('micropython-urllib.urequest')`
