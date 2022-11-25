#!/usr/bin/env python3
"""
Basic serial communications class for all serial instruments

Builds on pip's pyserial library

Thormund 18 Nov 2022
"""
from serial import Serial

class serial_comm(Serial):
    """Basic class for serial communication"""
    def __init__(self, port, timeout: float = 2) -> None:
        # self.serial = self._open_port(port, timeout)
        super().__init__(port, timeout=timeout)
        self.write('a')  # flush io buffer
        self._serial_read()   # will read unknown command

    # def _open_port(self, port, timeout:float) -> Serial:
    #     ser = Serial(port, timeout)
    #     print('ser obtained')
    #     return ser

    def close_port(self) -> None:
        self.close()

    def write(self, string: str) -> None:
        """writes to serial device
        Input
        -----
        string: UTF-8 encoded string. converts to binary before writing.
        """
        super().write((string + '\n').encode())

    def _serial_read(self) -> bytes:
        """Reads from serial device"""
        # old get_response method using read(64) is unreliable
        return super().readline().strip()

    def ask(self, string: str) -> bytes:
        """Queries response after writing to device."""
        self.write(string)
        return self._serial_read()
