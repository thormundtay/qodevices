#!/usr/bin/env python3
"""
Thorlabs ITC4001 Laser driver

Joel and Seth Poh, 2022.03.29 - overhauled laser driver control script
Thormund - 2022.11.11 - forked from python_general/devices to sort import
    errors, and cleanup methods, along with context management
"""

__all__ = ["thorlabsLaserDriver"]

import logging
from usbtmc.usbtmc import Instrument


class thorlabsLaserDriver(Instrument):

    def __init__(self, *args, **kwargs):
        """Generates instance of Thorlabs ITC laser driver.

        Documentation is as provided in www.thorlabs.com/software/MUC/4000_Series/Manual/Series4000_SPCI_Programmers_Reference_V3.2.pdf
        or newer.
        Class is build on usbtmc library from python-ivi/python-usbtmc
        repository.
        """
        super().__init__(*args, **kwargs)

    def __enter__(self):
        """dunder method for with statement"""
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        """dunder method for with statement"""
        logging.info("exc_type = ", exc_type)
        logging.info("exc_value = ", exc_value)
        logging.info("exc_traceback = ", exc_traceback)
        self.close()
        return True
        # return super().__exit__(exc_type, exc_value, exc_traceback)

    #### ld output control

    @property
    def outp(self):
        """
        returns the output state of the laser diode, off = 0 and on = 1
        """
        return self.ask("OUTP?")

    @outp.setter
    def outp(self, value):
        """
        sets the output state of the laser diode, off = 0 and on = 1
        """
        if value == 0 or value == 1:
            self.write(f"OUTP {value}")
        else:
            raise ValueError(f"Illegal value of {value} passed into argument.")

    @property
    def sour_func_mode(self):
        """
        returns laser diode source function, current = 0 and power = 1
        """
        return self.ask("SOUR:FUNC:MODE?")

    @sour_func_mode.setter
    def sour_func_mode(self, value):
        """
        sets laser diode source function, current = 0 and power = 1
        """
        if value == 0:
            self.write("SOUR:FUNC:MODE CURR ")
        elif value == 1:
            self.write("SOUR:FUNC:MODE POW")
        else:
            raise ValueError(f"Illegal value of {value} passed into argument.")

    @property
    def sour_curr_lim(self):
        """
        returns laser diode source limit current in amperes
        """
        return self.ask("SOUR:CURR:LIM?")

    @sour_curr_lim.setter
    def sour_curr_lim(self, value):
        """
        sets laser diode source limit current in amperes
        """
        self.write(f"SOUR:CURR:LIM {value}")

    @property
    def sour_curr(self):
        """
        returns laser diode current setpoint in amperes
        """
        return self.ask("SOUR:CURR?")

    @sour_curr.setter
    def sour_curr(self, value):
        """
        sets laser diode current setpoint in amperes
        """
        MAX_CURRENT = float(self.ask("SOUR:CURR:LIM?"))
        if value >= 0 and value <= MAX_CURRENT:
            self.write(f"SOUR:CURR {value}")
        else:
            raise ValueError(f"Illegal value of {value} passed into argument.")

    @property
    def meas_curr(self):
        """
        returns laser diode source current in amperes
        """
        return float(self.ask("MEAS:CURR?"))

    @property
    def meas_volt(self):
        """
        returns laser diode source voltage in volts
        """
        return float(self.ask("MEAS:VOLT?"))

    @property
    def meas_temp(self):
        """
        returns laser diode temp in degree celsius
        """
        return float(self.ask("MEAS:TEMP?"))

    #### tec output control
    @property
    def outp2(self):
        """
        returns the output state of the tec, off = 0 and on = 1
        """
        return self.ask("OUTP2?")

    @outp2.setter
    def outp2(self, value):
        """
        sets the output state of the tec, off = 0 and on = 1
        """
        if value == 0 or value == 1:
            self.write(f"OUTP2 {value}")
        else:
            raise ValueError(f"Illegal value of {value} passed into argument.")

    @property
    def sour2_func(self):
        """
        returns tec source function, temperature = 0 and current = 1
        """
        return self.ask("SOUR2:FUNC?")

    @sour2_func.setter
    def sour2_func(self, value):
        """
        sets tec function, temperature = 0 and current = 1
        """
        if value == 0:
            self.write("SOUR2:FUNC TEMP")
        elif value == 1:
            self.write("SOUR2:FUNC CURR")
        else:
            raise ValueError(f"Illegal value of {value} passed into argument.")

    @property
    def sour2_curr_lim(self):
        """
        returns tec source limit current in amperes
        """
        return self.ask("SOUR2:CURR:LIM?")

    @sour2_curr_lim.setter
    def sour2_curr_lim(self, value):
        """
        sets tec source limit current in amperes
        """
        self.write(f"SOUR2:CURR:LIM {value}")

    @property
    def sour2_curr(self):
        """
        returns tec source current setpoint in amperes
        """
        return self.ask("SOUR2:CURR?")

    @sour2_curr.setter
    def sour2_curr(self, value):
        """
        sets tec source current setpoint in amperes
        """
        MAX_CURRENT = self.ask("SOUR2:CURR:LIM?")
        if value >= 0 and value <= MAX_CURRENT:
            self.write(f"SOUR2:CURR {value}")
        else:
            raise ValueError(f"Illegal value of {value} passed into argument. \
                {MAX_CURRENT = }")

    @property
    def sour2_temp_lim_low(self):
        """
        returns min temperature setpoint allowed in degree celsius
        """
        return self.ask("SOUR2:TEMP:LIM:LOW?")

    @sour2_temp_lim_low.setter
    def sour2_temp_lim_low(self, value):
        """
        sets min temperature setpoint allowed in degree celsius
        """
        self.write(f"SOUR2:TEMP:LIM:LOW {value}")

    @property
    def sour2_temp_lim_high(self):
        """
        returns max temperature setpoint allowed in degree celsius
        """
        return self.ask("SOUR2:TEMP:LIM:HIGH?")

    @sour2_temp_lim_high.setter
    def sour2_temp_lim_high(self, value):
        """
        sets max temperature setpoint allowed in degree celsius
        """
        self.write(f"SOUR2:TEMP:LIM:HIGH {value}")

    @property
    def sour2_temp(self):
        """
        returns temperature setpoint in degree celsius
        """
        return self.ask("SOUR2:TEMP?")

    @sour2_temp.setter
    def sour2_temp(self, value):
        """
        sets temperature setpoint in degree celsius
        """
        MIN_TEMP = float(self.ask("SOUR2:TEMP:LIM:LOW?"))
        MAX_TEMP = float(self.ask("SOUR2:TEMP:LIM:HIGH?"))
        if value >= MIN_TEMP and value <= MAX_TEMP:
            self.write(f"SOUR2:TEMP {value}")
        else:
            print(f"{MIN_TEMP = }\n{MAX_TEMP = }")
            raise ValueError(f"Illegal value of {value} passed into argument.")

    @property
    def filt(self):
        """
        returns LD output noise filter status (1 for on, 0 for off)
        (LDC4005 ITC4001, ITC4002QCL, ITC4005, ITC4005QCL only)
        """
        return self.ask("FILT:STAT")

    @filt.setter
    def filt(self, value):
        """
        sets LD output noise filter
        """
        if value != 0 or value != 1:
            raise ValueError(f"Illegal value of {value} passed into argument.")
        if self.outp != 0:
            print("LD Output Noise reduction filter cannot be changed while \
                LD is not off!")
            return
        self.write(f"FILT:STAT {value}")

    #### device control #####

    @property
    def idn(self):
        """
        returns device identifier
        """
        return self.ask("*IDN?")
