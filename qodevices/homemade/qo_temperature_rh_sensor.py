#!/usr/bin/env python3
"""
Temperature and rh sensor
https://qoptics.quantumlah.org/wiki/index.php/Temperature/RH_sensor

To Do:
-

Seth Poh, 2022.04.18 - created temperature and rh sensor control script
Thormund, 2022.11.18 - switched pyserial dependency, depreciating getresponse

"""
__all__ = ["qoTemperatureRhSensor"]

from ..baseclass.baseserial import serial_comm

class qoTemperatureRhSensor(serial_comm):
    """
    Temperature and rh sensor class
    """

    def __init__(self, device_path: str = '', timeout: float = 2) -> None:
        """
        Creates a qoTemperatureRhSensor instance.

        Input
        -----
        device_path (str): full path to the serial device as arguments
        timeout (float): Optional. serial device timeout in seconds
        """
        if not device_path:
            raise ValueError('No device path given')
        # Do not catch all errors in init method haphazardly
        super().__init__(device_path, timeout=2)

	###### properties ######

    ### thermistor bias status

    @property
    def status(self) -> bytes:
        """
        returns power state of laser diode
        """
        return self.ask('STATUS?')

    @status.setter
    def status(self, value: int) -> None:
        """
        sets power state thermister bias
        """
        if value == 0:
            self.write('OFF')
        elif value == 1:
            self.write('ON')
        else:
            raise ValueError(f"Illegal argument with {value = }")

    @property
    def itemp(self) -> float:
        """
        returns instantaneous temperature in degree celsius (format: xx.xxx)
        """
        return float(self.ask('ITEMP?'))

    @property
    def ntemp(self) -> float:
        """
        returns last periodically (100ms) read temperature in degree celsius (format: xx.xxx)
        """
        return float(self.ask('NTEMP?'))

    @property
    def temp(self) -> float:
        """
        returns a low-pass filtered average temperature over 3.2 sec in degree celsius (format: xx.xxx)

        """
        return float(self.ask('TEMP?'))

    @property
    def rh(self) -> float:
        """
        returns relative humidity in percent from the sht30 sensor (format: xx.xx)
        """
        return float(self.ask('RH?'))

    @property
    def ctemp(self) -> float:
        """
        returns Sensirion chip temperature in degree celsius (format: xx.xxx)
        """
        return float(self.ask('CTEMP?'))

    @property
    def weather(self) -> float:
        """
        Reports both avg temperature and rel humidity (format: xx.xxx xx.xx)
        """
        return self.ask('WEATHER?')

    @property
    def all(self) -> float:
        """
        Returns like WEATHER?, but additionally returns the RH chip temperature (format: xx.xxx xx.xx xx.xxx)
        """
        return self.ask('ALL?')

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
