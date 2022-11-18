#!/usr/bin/env python3
"""
Basic serial communications class for all serial instruments

Builds on pip's pyserial library

Thormund 18 Nov 2022
"""
from serial import Serial

class serial_comm:
    """Basic class for serial communication"""
    def __init__(self, port, timeout: float = 2) -> None:
        self.serial = self._open_port(port, timeout)
        self.write('a')  # flush io buffer
        self.read()   # will read unknown command

    def _open_port(self, port, timeout:float) -> Serial:
        ser = Serial(port, timeout)
        return ser

    def close_port(self) -> None:
        self.serial.close()

    def write(self, string: str) -> None:
        """writes to serial device
        Input
        -----
        string: UTF-8 encoded string. converts to binary before writing.
        """
        self.serial.write((string + '\n').encode())

    def read(self) -> bytes:
        """Reads from serial device"""
        # old get_response method using read(64) is unreliable
        return self.serial.readline().strip()

    def ask(self, string: str) -> bytes:
        """Queries response after writing to device."""
        self.write(string)
        return self.read()
