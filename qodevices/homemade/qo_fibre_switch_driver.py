#!/usr/bin/env python3
"""
Fibre switch driver
https://qoptics.quantumlah.org/wiki/index.php/Triple_optical_switch

To Do:
-

Seth, 2022.03.29 - overhauled fibre driver control script
Thormund, 2022.11.18   - switched pyserial dependencies, added type hinting
"""
__all__ = ["qoFibreSwitchDriver"]

from ..baseclass.baseserial import serial_comm

##### limit constants #####

MAX_PULSE_DURATION = 255

class qoFibreSwitchDriver(serial_comm):
    """
    Fibre switch driver class
    """

    def __init__(self, device_path: str = '', timeout: float = 2) -> None:
        """
        Creates a qoFibreSwitchDriver instance.

        Input
        -----
        device_path (str): full path to the serial device as arguments
        timeout (float): Optional. serial device timeout in seconds
        """
        if not device_path:
            raise ValueError('No device path given')
        try:
            super().__init__(device_path, timeout=2)
        except:
            print('The indicated device cannot be found')

    ###### properties ######

    @property
    def single(self) -> int:
        """
        Returns position value of switch 1 (0 or 1),
        or error condition -1 for both closed, -2 for both open.
        """
        return int(self.ask('SINGLE?'))

    @single.setter
    def single(self, value: int) -> None:
        """
        sets switch 1 to value (0 or 1).
        """
        if value == 0 or value == 1:
            self.write(f'SINGLE {value}')
        else:
            print('Illegal value')

    @property
    def switch_1(self) -> int:
        """
        Returns position value of switch 1 (0 or 1),
        or error condition -1 for both closed, -2 for both open.
        """
        return int(self.ask('SWITCH? 1'))

    @switch_1.setter
    def switch_1(self, value: int) -> None:
        """
        sets channel 1 to value (0 or 1).
        """
        if value == 0 or value == 1:
            self.write(f'SWITCH 1 {value}')
        else:
            print('Illegal value')

    @property
    def switch_2(self) -> int:
        """
        Returns position value of switch 2 (0 or 1),
        or error condition -1 for both closed, -2 for both open.
        """
        return int(self.ask('SWITCH? 2'))

    @switch_2.setter
    def switch_2(self, value: int) -> None:
        """
        sets channel 2 to value (0 or 1).
        """
        if value == 0 or value == 1:
            self.write(f'SWITCH 2 {value}')
        else:
            print('Illegal value')

    @property
    def switch_3(self) -> int:
        """
        Returns position value of switch 3 (0 or 1),
        or error condition -1 for both closed, -2 for both open.
        """
        return int(self.ask('SWITCH? 3'))

    @switch_3.setter
    def switch_3(self, value: int) -> None:
        """
        sets channel 3 to value (0 or 1).
        """
        if value == 0 or value == 1:
            self.write(f'SWITCH 3 {value}')
        else:
            print('Illegal value')

    @property
    def millisec(self) -> float:
        """
        returns duration of switch pulse in milliseconds
        """
        return float(self.ask('MILLISEC?'))

    @millisec.setter
    def millisec(self, value) -> None:
        """
        sets duration of switch pulse in milliseconds
        """
        if value <= MAX_PULSE_DURATION:
            self.write(f'MILLISEC {value}')
        else:
            raise ValueError(f"Input argument of {value = } exceeds \
                MAX_PULSE_DURATION of {MAX_PULSE_DURATION}")

    @property
    def config(self) -> int:
        """
        returns drive coil polarity configuration
        """
        return int(self.ask('CONFIG?'))

    @config.setter
    def config(self, value: int) -> None:
        """
        Sets the drive coil polarity configuration of each switch.
        Bits 0..2 correspond to switches 1..3.
        """
        if value <= 7:
            self.write(f'CONFIG {value}\n')
        else:
            raise ValueError(f"Input argument of {value = } is invalid!")

    ###### device control ######

    def idn(self) -> bytes:
        """
        returns device identifier
        """
        return self.ask('*IDN?')

    def reset(self) -> None:
        """
        reset device
        """
        self.write('*RST')
