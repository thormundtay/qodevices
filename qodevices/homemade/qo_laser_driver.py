#!/usr/bin/env python3
"""
Laser driver
http://qoptics.quantumlah.org/wiki/index.php/Laser_driver#Commands_and_requests

To Do:
- Implement error message handling
- Implement status return for temperature control loop on laser driver
- Implement error handing for peltier voltage changes when temperature control loop is on

Joel and Seth, 2022.03.24   - overhauled laser driver control script
                            - ported laser parameters to @property decorator
                            - ported getresponse function to seperated file
Thormund, 2022.11.18 - switched pyserial dependency, depreciating getresponse
                     - error message handling should follow as accordingly

"""
from ..baseclass.baseserial import serial_comm

##### limit constants #####

MIN_TEMP = -20.0
MAX_TEMP = 85.0

MIN_PELTIER = -3.0
MAX_PELTIER = 3.0

MAX_CURRENT_LIMIT = 188.0

MAX_CONSTPID = 10

class qoLaserDriver(serial_comm):
    """
    Laser driver class
    """

    def __init__(self, device_path: str = '', timeout: float = 2) -> None:
        """
        Creates a qoLaserDriver instance.

        Input
        -----
        device_path (str): full path to the serial device as arguments
        timeout (float): Optional. serial device timeout in seconds
        """
        if not device_path:
            raise ValueError('No device path given')
        try:
            super().__init__(self, device_path, timeout=2)
        except:
            print('The indicated device cannot be found')

    ###### properties ######

    ### laser diode status

    @property
    def status(self) -> bytes:
        """
        returns power state of laser diode
        """
        return self.ask('STATUS?')

    @status.setter
    def status(self, value: int) -> None:
        """
        sets power state of laser diode
        """
        if value == 0:
            self.write('OFF')
        elif value == 1:
            self.write('ON')
        else:
            raise ValueError(f"Illegal argument with {value = }")

    ### peltier voltage

    @property
    def peltier(self) -> float:
        """
        returns peltier voltage in mV
        """
        return float(self.ask('PELTIER?'))

    @peltier.setter
    def peltier(self, value: float) -> None:
        """
        sets peltier voltage in mV
        """
        if value < MIN_PELTIER or value > MAX_PELTIER:
            print('Peltier voltage setting out of range.')
        else:
            print('Temperature control loop turned off.')
            self.write('LOOP 0')
            self.write(f'PELTIER {value}')

    ### laser diode temperature

    @property
    def temperature(self) -> float:
        """
        returns laser diode temperature in degree celsius
        """
        return float(self.ask('TEMP?'))

    @temperature.setter
    def temperature(self, value: float):
        """
        sets laser diode temperature in degree celsius
        """
        if value < MIN_TEMP or value > MAX_TEMP:
            print(f"{MIN_TEMP = }\n{MAX_TEMP = }")
            raise ValueError(f'Temperature setting out of range. {value = }')
        else:
            self.write(f'TEMP {value}')

    ### laser diode current

    @property
    def current(self) -> float:
        """
        returns laser diode current in mA
        """
        return float(self.ask('CURRENT?'))

    @current.setter
    def current(self, value: float) -> None:
        """
        sets laser diode current in mA
        """
        MAX_CURRENT = float(self.ask('LIMIT?'))
        if value > MAX_CURRENT or value < 0:
            print(f"{MAX_CURRENT = }")
            raise ValueError(f'Current setting out of range.\n\
                {MAX_CURRENT = }, {value = }')
        else:
            self.write(f'CURRENT {value}')

    ### temperature control loop

    @property
    def loop(self) -> None:
        # Not implemented? - Thormund November 2022
        return

    @loop.setter
    def loop(self, value: int) -> None:
        """
        turns on or off temperature contorl loop
        """
        if value == 0 or value == 1:
            self.write(f'LOOP {value}')
        else:
            raise ValueError(f"Illegal argument with {value = }")

    ### pid constants

    @property
    def constp(self) -> float:
        """
        returns pid loop p constant in V/K
        """
        return float(self.ask('CONSTP?'))

    @constp.setter
    def constp(self, value: float) -> None:
        """
        sets pid loop p constant in V/K
        """
        if value > MAX_CONSTPID:
            raise ValueError(f'Constant setting out of range.\n\
                {MAX_CONSTPID = }, {value = }')
        else:
            self.write(f'CONSTP {value}')

    @property
    def consti(self) -> float:
        """
        returns pid loop i constant in V/Ks
        """
        return float(self.ask('CONSTI?'))

    @consti.setter
    def consti(self, value: float) -> None:
        """
        sets pid loop i constant in V/Ks
        """
        if value > MAX_CONSTPID:
            raise ValueError(f'Constant setting out of range.\n\
                {MAX_CONSTPID = }, {value = }')
        else:
            self.write(f'CONSTI {value}')

    @property
    def constd(self) -> float:
        """
        returns pid loop d constant in Vs/K
        """
        return float(self.ask('CONSTD?'))

    @constd.setter
    def constd(self, value: float) -> None:
        """
        sets pid loop d constant in Vs/K
        """
        if value > MAX_CONSTPID:
            print('Constant setting out of range.')
        else:
            self.write(f'CONSTD {value}')

    ### laser diode current limit

    @property
    def limit(self) -> float:
        """
        returns laser diode current limit in mA
        """
        return float(self.ask('LIMIT?'))

    @limit.setter
    def limit(self, value: float) -> None:
        """
        sets laser diode current limit in mA
        """
        if value > MAX_CURRENT_LIMIT:
            raise ValueError(f'Laser diode current limit setting out of range.\
                \n{MAX_CURRENT_LIMIT = }, {value = }')
        else:
            self.write(f'LIMIT {value}')

    ###### device control ######

    def idn(self) -> bytes:
        """
        returns device identifier
        """
        return self.ask('*IDN?')

    def reset(self) -> bytes:
        """
        reset device
        """
        self.write('*RST')

    def save(self) -> bytes:
        """
        save current settings to eeprom
        """
        return self.ask('SAVE')
