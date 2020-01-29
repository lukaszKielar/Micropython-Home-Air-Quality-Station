# ESP32 MicroPython Home Air Quality Station

## Software

* Python 3 (i.e. Miniconda/Anaconda). I highly recommend creating new dedicated virtual environment for your project with following libraries:
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
* Jumping wires
* Breadboard

### Optionally

* Temperature/humidity/pressure sensor (i.e. DS18B20, DHT11, BME280)
* RTC
* SSD1303 OLED display

## Preparing the board

### Check COM PORT

Let's plug ESP32 into computer and check whether everything was installed correctly and board is visible by our machine. Running following command in the terminal `ls /dev/tty*USB*` should return ESP32 COM PORT (i.e. `/dev/ttyUSB0` on Linux or `/dev/tty.SLAB_USBtoUART` on MacOS). If nothing shows up make sure you have installed software correctly.

### Erase flash

To make sure that everything is up to date we should erase flash on ESP32 running following command:

```bash
python -m esptool --chip esp32 erase_flash
```

It should automatically find COM PORT.

### Write latest firmware

When our flash was erased we can write latest firware to our board using command. Double check ***port*** and ***path to the downloaded firmware file***.

```bash
python -m esptool --chip esp32 --port <port> write_flash -z 0x1000 <path/to/esp32/firmware.bin>
```

### Connect to the REPL

```bash
screen /dev/ttyUSB0 115200
```

### Check files on board

```bash
ampy --port /dev/ttyUSB0 ls
```

### Put a file on board

```bash
ampy --port /dev/ttyUSB0 put file.py
```

### Run file

```bash
ampy --port /dev/ttyUSB0 run file.py
```

## How to install micropython libraries on esp32

* Connect to the REPL.
* Connect to the Internet.
* Install desired package. For further details please visit official [micropython-lib](https://github.com/micropython/micropython-lib) repository.

```python
import upip
upip.install('micropython-urllib.urequest')
```
