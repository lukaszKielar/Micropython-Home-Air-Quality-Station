import machine
import ustruct
import time


class UartError(Exception):
    pass


# TODO add debug mode
class Pms7003:
    """
    More about passive mode here:
    https://github.com/teusH/MySense/blob/master/docs/pms7003.md
    https://patchwork.ozlabs.org/cover/1039261/
    https://joshefin.xyz/air-quality-with-raspberrypi-pms7003-and-java/
    """
    PMS_FRAME_LENGTH = 0
    PMS_PM1_0 = 1
    PMS_PM2_5 = 2
    PMS_PM10_0 = 3
    PMS_PM1_0_ATM = 4
    PMS_PM2_5_ATM = 5
    PMS_PM10_0_ATM = 6
    PMS_PCNT_0_3 = 7
    PMS_PCNT_0_5 = 8
    PMS_PCNT_1_0 = 9
    PMS_PCNT_2_5 = 10
    PMS_PCNT_5_0 = 11
    PMS_PCNT_10_0 = 12
    PMS_VERSION = 13
    PMS_ERROR = 14
    PMS_CHECKSUM = 15

    START_BYTE_1 = 0x42
    START_BYTE_2 = 0x4d
    ENTER_PASSIVE_MODE_REQUEST = bytearray([0x42, 0x4d, 0xe1, 0x00, 0x00, 0x01, 0x70])
    ENTER_PASSIVE_MODE_RESPONSE = bytearray([0x42, 0x4d, 0x00, 0x04, 0xe1, 0x00, 0x01, 0x74])
    SLEEP_REQUEST = bytearray([0x42, 0x4d, 0xe4, 0x00, 0x00, 0x01, 0x73])
    SLEEP_RESPONSE = bytearray([0x42, 0x4d, 0x00, 0x04, 0xe4, 0x00, 0x01, 0x77])
    WAKEUP_REQUEST = bytearray([0x42, 0x4d, 0xe4, 0x00, 0x01, 0x01, 0x74])  # NO response
    READ_IN_PASSIVE_REQUEST = bytearray([0x42, 0x4d, 0xe2, 0x00, 0x00, 0x01, 0x71])  # data as response

    def __init__(self, uart=2):
        self.uart = machine.UART(uart, baudrate=9600, bits=8, parity=None, stop=1)
        self._send_cmd(self.ENTER_PASSIVE_MODE_REQUEST, self.ENTER_PASSIVE_MODE_RESPONSE)

    def __repr__(self):
        return "Pms7003({})".format(self.uart)

    def _assert_byte(self, byte, expected):
        if byte is None or len(byte) < 1 or ord(byte) != expected:
            return False
        return True

    def _send_cmd(self, request, response):
        
        nr_of_written_bytes = self.uart.write(request)

        if nr_of_written_bytes != len(request):
            raise UartError('Failed to write to UART')
        
        if response:
            time.sleep(2)
            buffer = self.uart.read(len(response))

            if buffer != response:
                raise UartError(
                    'Wrong UART response, expecting: {}, getting: {}'.format(
                        response, buffer
                    )
                )

            # print('Response:', ''.join('0x{:02x} '.format(x) for x in buffer))

    def sleep(self):
        self._send_cmd(self.SLEEP_REQUEST, self.SLEEP_RESPONSE)

    def wakeup(self):
        self._send_cmd(self.WAKEUP_REQUEST, None)

    def read(self):
        self._send_cmd(self.READ_IN_PASSIVE_REQUEST, None)
        
        while True:
            first_byte = self.uart.read(1)
            if not self._assert_byte(first_byte, self.START_BYTE_1):
                # print('Bad first byte')
                continue
            second_byte = self.uart.read(1)
            if not self._assert_byte(second_byte, self.START_BYTE_2):
                # print('Bad second byte')
                continue
        
            # we are reading 30 bytes left
            read_bytes = self.uart.read(30)
            if len(read_bytes) < 30:
                continue

            data = ustruct.unpack('!HHHHHHHHHHHHHBBH', read_bytes)

            checksum = self.START_BYTE_1 + self.START_BYTE_2
            checksum += sum(read_bytes[:28])

            if checksum != data[self.PMS_CHECKSUM]:
                # print('Bad checksum')
                continue
                
            return {
                'FRAME_LENGTH': data[self.PMS_FRAME_LENGTH],
                'PM1_0': data[self.PMS_PM1_0],
                'PM2_5': data[self.PMS_PM2_5],
                'PM10_0': data[self.PMS_PM10_0],
                'PM1_0_ATM': data[self.PMS_PM1_0_ATM],
                'PM2_5_ATM': data[self.PMS_PM2_5_ATM],
                'PM10_0_ATM': data[self.PMS_PM10_0_ATM],
                'PCNT_0_3': data[self.PMS_PCNT_0_3],
                'PCNT_0_5': data[self.PMS_PCNT_0_5],
                'PCNT_1_0': data[self.PMS_PCNT_1_0],
                'PCNT_2_5': data[self.PMS_PCNT_2_5],
                'PCNT_5_0': data[self.PMS_PCNT_5_0],
                'PCNT_10_0': data[self.PMS_PCNT_10_0],
                'VERSION': data[self.PMS_VERSION],
                'ERROR': data[self.PMS_ERROR],
                'CHECKSUM': data[self.PMS_CHECKSUM],
            }
