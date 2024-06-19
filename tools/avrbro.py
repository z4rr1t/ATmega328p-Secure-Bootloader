import serial
import time
import struct
from crypt_utils import pack_data
from pwn import *
import sys

PRIVATE_KEY = "64F204D7018BCCAA61173EB6E1E8153E77B5C8A60E0B9CE8"

IS_READY = 0x00
OK_DEVICE_READY = 0x01

DO_RECEIVE_DATA = 0x02
DO_PROGRAM_FLASH = 0x03
DO_CHECK_DATA = 0x04

DO_UPDATE_PKEY = 0x05
DO_SELF_CHECK = 0x06

DO_RESET_SZ_COUNTER = 0x0E

ERR_SIZE_TOO_BIG = 0x07
ERR_SIZE_TOO_SMALL = 0x08

ERR_MALICIOUS_DATA = 0x09
ERR_NOT_IMPLEMENTED = 0x0A
OK_SAFE_DATA = 0x0B
OK_DATA_RECEIVED = 0x0C
OK_PROGRAM_FLASHED = 0x0D

MAX_DATA_SIZE = 256
MIN_DATA_SIZE = 49

class ArduinoSerial:
    def __init__(self, port, baudrate=9600, timeout=10):
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        time.sleep(2)

    def begin(self, baudrate):
        self.ser.baudrate = baudrate

    def available(self):
        return self.ser.in_waiting

    def read(self):
        return self.ser.read(1)

    def readBytes(self, size):
        return self.ser.read(size)
    
    def readByte(self):
        return ord(self.read())

    def readString(self):
        return self.ser.read(self.ser.in_waiting).decode('utf-8')

    def write(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.ser.write(data)

    def writeByte(self, byte):
        self.ser.write(bytes([byte]))

    def writeBytes(self, data):
        self.ser.write(data)

    def print(self, data):
        if isinstance(data, str):
            self.ser.write(data.encode('utf-8'))
        else:
            self.ser.write(str(data).encode('utf-8'))

    def println(self, data):
        if isinstance(data, str):
            self.ser.write((data + '\n').encode('utf-8'))
        else:
            self.ser.write((str(data) + '\n').encode('utf-8'))

    def close(self):
        self.ser.close()


class AVRBro:
    def __init__(self, serial):
        self.serial = serial

    
    def is_ready(self):
        self.serial.writeByte(IS_READY)
        return (self.serial.readByte() == OK_DEVICE_READY)


    def send_data(self, data):
        self.serial.writeByte(DO_RECEIVE_DATA)
        self.serial.writeBytes(struct.pack(">H", len(data))) # the size of data
        self.serial.writeBytes(data) # the data
        status = self.serial.readByte()

        return status

    def verify_data(self):
        self.serial.writeByte(DO_CHECK_DATA)
        status = self.serial.readByte()
        return status

    def flash(self, program_data):
        self.serial.writeByte(DO_PROGRAM_FLASH)
        self.serial.writeBytes(struct.pack(">H", len(program_data)))
        self.serial.writeBytes(program_data)
        status = self.serial.readByte()
        return status

if __name__ == "__main__":
    private_key = bytes.fromhex(PRIVATE_KEY)


    blink_test_program = [
        0x0C, 0x94, 0x34, 0x00, 0x0C, 0x94, 0x3E, 0x00, 0x0C, 0x94, 0x3E, 0x00,
        0x0C, 0x94, 0x3E, 0x00, 0x0C, 0x94, 0x3E, 0x00, 0x0C, 0x94, 0x3E, 0x00,
        0x0C, 0x94, 0x3E, 0x00, 0x0C, 0x94, 0x3E, 0x00, 0x0C, 0x94, 0x3E, 0x00,
        0x0C, 0x94, 0x3E, 0x00, 0x0C, 0x94, 0x3E, 0x00, 0x0C, 0x94, 0x3E, 0x00,
        0x0C, 0x94, 0x3E, 0x00, 0x0C, 0x94, 0x3E, 0x00, 0x0C, 0x94, 0x3E, 0x00,
        0x0C, 0x94, 0x3E, 0x00, 0x0C, 0x94, 0x3E, 0x00, 0x0C, 0x94, 0x3E, 0x00,
        0x0C, 0x94, 0x3E, 0x00, 0x0C, 0x94, 0x3E, 0x00, 0x0C, 0x94, 0x3E, 0x00,
        0x0C, 0x94, 0x3E, 0x00, 0x0C, 0x94, 0x3E, 0x00, 0x0C, 0x94, 0x3E, 0x00,
        0x0C, 0x94, 0x3E, 0x00, 0x0C, 0x94, 0x3E, 0x00, 0x11, 0x24, 0x1F, 0xBE,
        0xCF, 0xEF, 0xD8, 0xE0, 0xDE, 0xBF, 0xCD, 0xBF, 0x0E, 0x94, 0x40, 0x00,
        0x0C, 0x94, 0x4F, 0x00, 0x0C, 0x94, 0x00, 0x00, 0x25, 0x9A, 0x90, 0xE2,
        0x85, 0xB1, 0x89, 0x27, 0x85, 0xB9, 0x2F, 0xEF, 0x31, 0xEE, 0x84, 0xE0,
        0x21, 0x50, 0x30, 0x40, 0x80, 0x40, 0xE1, 0xF7, 0x00, 0xC0, 0x00, 0x00,
        0xF3, 0xCF, 0xF8, 0x94, 0xFF, 0xCF];

    serial = ArduinoSerial("/dev/ttyACM0")
    avrbro = AVRBro(serial)

    log.info("Checking if device is OK ...")
    if (avrbro.is_ready()):
        log.success("Device is ready!")


    # log.info("Sending random data ...")
    # data = pack_data(cyclic(128), private_key)
    # status = avrbro.send_data(data)

    # if (status == OK_DATA_RECEIVED):
    #     log.success("Data Received by device!")   
    # else:
    #     log.warn(f"something went wrong {status}")  

    # log.info("Verifiying random data ...")
    # status = avrbro.verify_data()
    # if (status == OK_SAFE_DATA):
    #     log.success(f"Data Verification is functional ... {status}")
    # else:
    #     log.warn(f"Data Verification is not functional ... {status}")


    print(avrbro.flash(blink_test_program))
    
    # while True:
    #     pass