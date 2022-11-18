#!/usr/bin/env python3
"""
Optical Power Meter Driver
http://https://qoptics.quantumlah.org/wiki/index.php/Digital_Powermeter

To Do:
- Implement FLOW and STOP

Seth Poh, 2022.04.05   - overhauled optical power meter driver script
Thormund, 2022.11.18   - switched pyserial dependencies, added type hinting
"""
from ..baseclass.baseserial import serial_comm

class qoDigitalPowerMeter(serial_comm):
    """
    Digital powermeter class
    """

    def __init__(self, device_path: str = '', timeout: float = 2) -> None:
        """
        Creates a qoDigitalPowerMeter instance.

        Input
        -----
        device_path (str): full path to the serial device as arguments
        timeout (float): Optional. serial device timeout in seconds
        """
        if not device_path:
            raise ValueError('No device path given')
        try:
            super().__init__(device_path, timeout)
        except:
            print('The indicated device cannot be found')

    ### properties

    @property
    def range(self) -> int:
        """
        returns shunt resistor index, 1 to 5
        """
        return int(self.ask('RANGE?'))

    @range.setter
    def range(self, value: int) -> None:
        """
        sets shunt resistor, 1 to 5
        """
        if isinstance(value, int) and 1 <= value <= 5:
            self.write(f'RANGE {value}')
        else:
            print('Illegal value.')

    ### peltier voltage

    @property
    def volt(self) -> float:
        """
        returns voltage across sense resistor in V
        """
        return float(self.ask('VOLT?'))

    @property
    def raw(self) -> bytes:
        """
        returns voltage across sense resistor in raw units
        """
        return self.ask('RAW?')

    @property
    def allin(self) -> bytes:
        """
        returns all 8 input voltages and temperature
        """
        return self.ask('ALLIN?')

    ### device control

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
