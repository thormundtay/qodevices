#!/usr/bin/env python3
"""
Strain gauge driver
https://qoptics.quantumlah.org/wiki/index.php/Strain_gauge_adapter

To Do:
-

Seth Poh, 2022.04.18 - created strain gauge driver control script
Thormund, 2022.11.18 - switched pyserial dependency, depreciating getresponse
"""
__all__ = ["qoStrainGaugeDriver"]

from ..baseclass.baseserial import serial_comm

##### limit constants #####

MAX_CONSTPID = 569.325056

class qoStrainGaugeDriver(serial_comm):
    """
    Strain gauge driver class
    """

    def __init__(self, device_path: str = '', timeout: float = 2) -> None:
        """
        Creates a qoStrainGaugeDriver instance.

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

    @property
    def status(self):
        """
        """
        pass

    @status.setter
    def status(self, value: int) -> None:
        """
        turns the analog part on or off, and performs DAC/ADC init.
        """
        if value == 0:
            self.write('OFF')
        elif value == 1:
            self.write('ON')
        else:
            raise ValueError(f"Illegal argument with {value = }")

    ### output

    @property
    def out_0(self) -> float:
        """
        returns output setpoint of output 0 (format: x.xxxxxx)
        """
        return float(self.ask('OUT? 0'))

    @out_0.setter
    def out_0(self, value: float) -> None:
        """
        sets output 0 to a given value (in volt) if the loop is off. (format: x.xxxxxx)
        """
        self.write(f'OUT 0 {value}')

    @property
    def out_1(self) -> float:
        """
        returns output setpoint of output 1 (format: x.xxxxxx)
        """
        return float(self.ask('OUT? 1'))

    @out_1.setter
    def out_1(self, value) -> None:
        """
        sets output 1 to a given value (in volt) if the loop is off. (format: x.xxxxxx)
        """
        self.write(f'OUT 1 {value}')

    @property
    def out_2(self) -> float:
        """
        returns output setpoint of output 2 (format: x.xxxxxx)
        """
        return float(self.ask('OUT? 2'))

    @out_2.setter
    def out_2(self, value) -> None:
        """
        sets output 2 to a given value (in volt) if the loop is off. (format: x.xxxxxx)
        """
        self.write(f'OUT 2 {value}')

    ### input

    @property
    def in_0(self) -> float:
        """
        returns the input of a channel 0. The value is 64/125 of the voltage after the instrumentation amplifier. (format: x.xxxxxx)
        """
        return float(self.ask('IN? 0'))

    @property
    def in_1(self) -> float:
        """
        returns the input of a channel 1. The value is 64/125 of the voltage after the instrumentation amplifier. (format: x.xxxxxx)
        """
        return float(self.ask('IN? 1'))

    @property
    def allin(self) -> bytes:
        """
        returns the input of channel 1 and 2. The value is 64/125 of the voltage after the instrumentation amplifier. (format: x.xxxxxx)
        """
        return self.ask('ALLIN?')

    ### control loop

    @property
    def set_0(self) -> float:
        """
        returns setpoint of channel 0 (format: x.xxxxxx)
        """
        return float(self.ask('SET? 0'))

    @set_0.setter
    def set_0(self, value: float) -> None:
        """
        setpoint of channel 0 (format: x.xxxxxx)
        """
        self.write(f'SET 0 {value}')

    @property
    def set_1(self) -> float:
        """
        returns setpoint of channel 1 (format: x.xxxxxx)
        """
        return float(self.ask('SET? 1'))

    @set_1.setter
    def set_1(self, value: float) -> None:
        """
        setpoint of channel 1 (format: x.xxxxxx)
        """
        self.write(f'SET 1 {value}')

    @property
    def loop_0(self):
        return

    @loop_0.setter
    def loop_0(self, value: int) -> None:
        """
        switches the control loop on or off, off = 0 and on = 1
        """
        if value == 0 or value == 1:
            self.write(f'LOOP 0 {value}')
        else:
            raise ValueError(f"Illegal argument with {value = }")

    @property
    def loop_1(self) -> None:
        # Not implemented? - Thormund, November 2022
        return

    @loop_1.setter
    def loop_1(self, value: float) -> None:
        """
        switches the control loop on or off, off = 0 and on = 1
        """
        if value == 0 or value == 1:
            self.write(f'LOOP 1 {value}')
        else:
            raise ValueError(f"Illegal argument with {value = }")

    ### pid constants

    @property
    def constp_0(self) -> float:
        """
        sets the p constant for the control loop
        """
        return float(self.ask('CONSTP? 0'))

    @constp_0.setter
    def constp_0(self, value: float) -> None:
        """
        returns the p constant for the control loop
        """
        if value > MAX_CONSTPID:
            raise ValueError(f'Constant setting out of range.\n\
                {MAX_CONSTPID = }, {value = }')
        else:
            self.write(f'CONSTP 0 {value}')

    @property
    def consti_0(self) -> float:
        """
        returns the i constant for the control loop
        """
        return float(self.ask('CONSTI? 0'))

    @consti_0.setter
    def consti_0(self, value: float) -> None:
        """
        sets the i constant for the control loop
        """
        if value > MAX_CONSTPID:
            raise ValueError(f'Constant setting out of range.\n\
                {MAX_CONSTPID = }, {value = }')
        else:
            self.write(f'CONSTI 0 {value}')

    @property
    def constd_0(self) -> float:
        """
        sets the d constant for the control loop
        """
        return float(self.ask('CONSTD? 0'))

    @constd_0.setter
    def constd_0(self, value: float) -> None:
        """
        sets the d constant for the control loop
        """
        if value > MAX_CONSTPID:
            raise ValueError(f'Constant setting out of range.\n\
                {MAX_CONSTPID = }, {value = }')
        else:
            self.write(f'CONSTD 0 {value}')

    @property
    def constp_1(self) -> float:
        """
        sets the p constant for the control loop
        """
        return float(self.ask('CONSTP? 1'))

    @constp_1.setter
    def constp_1(self, value: float) -> None:
        """
        returns the p constant for the control loop
        """
        if value > MAX_CONSTPID:
            raise ValueError(f'Constant setting out of range.\n\
                {MAX_CONSTPID = }, {value = }')
        else:
            self.write(f'CONSTP 1 {value}')

    @property
    def consti_1(self) -> float:
        """
        returns the i constant for the control loop
        """
        return float(self.ask('CONSTI? 1'))

    @consti_1.setter
    def consti_1(self, value: float) -> None:
        """
        sets the i constant for the control loop
        """
        if value > MAX_CONSTPID:
            raise ValueError(f'Constant setting out of range.\n\
                {MAX_CONSTPID = }, {value = }')
        else:
            self.write(f'CONSTI 1 {value}')

    @property
    def constd_1(self) -> float:
        """
        sets the d constant for the control loop
        """
        return float(self.ask('CONSTD? 1'))

    @constd_1.setter
    def constd_1(self, value: float) -> None:
        """
        sets the d constant for the control loop
        """
        if value > MAX_CONSTPID:
            raise ValueError(f'Constant setting out of range.\n\
                {MAX_CONSTPID = }, {value = }')
        else:
            self.write(f'CONSTD 1 {value}')

    ### errors

    @property
    def err_0(self) -> float:
        """
        returns the current difference between setpoint and input for channel 0 (format: x.xxxxxx)
        """
        return float(self.ask('ERR? 0'))

    @property
    def err_1(self) -> float:
        """
        returns the current difference between setpoint and input for channel 1 (format: x.xxxxxx)
        """
        return float(self.ask('ERR? 1'))

    ###### device control ######

    def idn(self):
        """
        returns device identifier
        """
        return self.ask('*IDN?')

    def reset(self):
        """
        reset device
        """
        self.write('*RST')
