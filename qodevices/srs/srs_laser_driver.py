#!/usr/bin/env python3
"""
SRS Laser driver
- implements the temperature control part only

To Do:
- Implement laser driver part

Seth Poh, 2022.03.28 - overhauled srs laser driver control script for temperature part only
Thormund, 2022.11.18 - switched pyserial dependency, depreciating getresponse
"""
from ..baseclass.baseserial import serial_comm

class srsLaserDriver(serial_comm):
    """
    Laser driver class
    """

    def __init__(self, device_path: str = '', timeout: float = 2) -> None:
        """
        Creates a srsLaserDriver instance.

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

    ###### tec control ######

    #### tec limits

    @property
    def tilm(self):
        """
        returns tec current limit
        """
        return float(self.ask('TILM?'))

    @tilm.setter
    def tilm(self, value):
        """
        sets tec current limit
        """
        self.write(f'TILM {value}')

    @property
    def tvlm(self):
        """
        returns tec voltage limit
        """
        return float(self.ask('TVLM?'))

    @tvlm.setter
    def tvlm(self, value):
        """
        sets tec voltage limit
        """
        self.write(f'TVLM {value}')

    @property
    def tmin(self):
        """
        returns lower temperature limit in degree celsius
        """
        return float(self.ask('TMIN?'))

    @tmin.setter
    def tmin(self, value):
        """
        sets lower temperature limit in degree celsius
        """
        self.write(f'TMIN {value}')

    @property
    def tmax(self):
        """
        returns upper temperature limit in degree celsius
        """
        return float(self.ask('TMAX?'))

    @tmax.setter
    def tmax(self, value):
        """
        sets upper temperature limit in degree celsius
        """
        self.write(f'TMAX {value}')

    @property
    def trmn(self):
        """
        returns lower resistance limit in ohm
        """
        return float(self.ask('TRMN?'))

    @trmn.setter
    def trmn(self, value):
        """
        sets lower resistance limit in ohm
        """
        self.write(f'TRMN {value}')

    @property
    def trmx(self):
        """
        returns upper resistance limit in ohm
        """
        return float(self.ask('TRMX?'))

    @trmx.setter
    def trmx(self, value):
        """
        sets upper resistance limit in ohm
        """
        self.write(f'TRMX {value}')

    ##### tec setting #####

    @property
    def teon(self):
        """
        returns tec current status, off = 0 and on = 1
        """
        return self.ask('TEON?')

    @teon.setter
    def teon(self, value):
        """
        returns tec current status, off = 0 and on = 1
        """
        if value == 0 or value == 1:
            self.write(f'TEON {value}')
        else:
            print('Illegal value.')

    @property
    def tcur(self):
        """
        returns tec current setpoint
        """
        return float(self.ask('TCUR?'))

    @tcur.setter
    def tcur(self, value):
        """
        sets tec current setpoint
        """
        self.write(f'TCUR {value}')

    @property
    def temp(self):
        """
        returns temperature setpoint
        """
        return float(self.ask('TEMP?'))

    @temp.setter
    def temp(self, value):
        """
        sets temperature setpoint
        """
        self.write(f'TEMP {value}')

    @property
    def trth(self):
        """
        returns resistance setpoint
        """
        return float(self.ask('TRTH?'))

    @trth.setter
    def trth(self, value):
        """
        sets resistance setpoint
        """
        self.write(f'TRTH {value}')

    ### tec monitor

    @property
    def tird(self):
        """
        returns tec current reading
        """
        return float(self.ask('TIRD?'))

    @property
    def tvrd(self):
        """
        returns tec voltage reading
        """
        return float(self.ask('TVRD?'))

    @property
    def traw(self):
        """
        returns raw thermometer reading
        """
        return float(self.ask('TRAW?'))

    @property
    def ttrd(self):
        """
        returns celsius thermometer reading
        """
        return float(self.ask('TTRD?'))

    @property
    def tsns(self):
        """
        returns termperature sensor status
        """
        return float(self.ask('TSNS?'))

    ##### tec configuration #####

    @property
    def tmod(self):
        """
        returns tec control mode, cc = 0 and ct = 1
        """
        return self.ask('TMOD?')

    @tmod.setter
    def tmod(self, value):
        """
        turns on and off tec control mode, cc = 0 and ct = 1
        """
        if value == 0 or value == 1:
            self.write(f'TMOD {value}')
        else:
            print('Illegal value.')

    @property
    def tmlk(self):
        """
        returns lock tec control mode when on, no = 0 and yes = 1
        """
        return self.ask('TMLK?')

    @tmlk.setter
    def tmlk(self, value):
        """
        turns on and off lock tec control mode when on, no = 0 and yes = 1
        """
        if value == 0 or value == 1:
            self.write(f'TMLK {value}')
        else:
            print('Illegal value.')

    @property
    def tune(self):
        """
        returns tec autotune status, off = 0, yes = 1,
        unstable = 2, success = 3, and failed = 4, and check_polarity = 5
        """
        return self.ask('TUNE?')

    @tune.setter
    def tune(self, value):
        """
        turns on and off autotune, on = 0 and yes = 1
        """
        if value == 0 or value == 1:
            self.write(f'TUNE {value}')
        else:
            print('Illegal value.')

    @property
    def tats(self):
        """
        returns tec autotune step size
        """
        return self.ask('TATS?')

    @tats.setter
    def tats(self, value):
        """
        sets tec autotune step size
        """
        self.write(f'TATS {value}')

    @property
    def tpgn(self):
        """
        returns tec control loop p gain
        """
        return self.ask('TPGN?')

    @tpgn.setter
    def tpgn(self, value):
        """
        sets tec control loop p gain
        """
        self.write(f'TPGN {value}')

    @property
    def tign(self):
        """
        returns tec control loop i gain
        """
        return self.ask('TIGN?')

    @tign.setter
    def tign(self, value):
        """
        sets tec control loop i gain
        """
        self.write(f'TIGN {value}')

    @property
    def tdgn(self):
        """
        returns tec control loop d gain
        """
        return self.ask('TDGN?')

    @tdgn.setter
    def tdgn(self, value):
        """
        sets tec control loop d gain
        """
        self.write(f'TDGN {value}')

    @property
    def tpol(self):
        """
        returns tec polarity reverse mode, no = 0, yes = 1
        """
        return self.ask('TPOL?')

    @tpol.setter
    def tpol(self, value):
        """
        sets tec polarity reverse mode, no = 0, yes = 1
        """
        if value == 0 or value == 1:
            self.write(f'TPOL {value}')
        else:
            print('Illegal value.')

    ##### tec sensor #####

    @property
    def tmdn(self):
        """
        returns temperature sensor model
        model beta 0, shh 1, none 2
        """
        return self.ask('TMDN?')

    @tmdn.setter
    def tmdn(self, value):
        """
        sets temperature sensor
        model beta 0, shh 1, none 2
        """
        if value == 0 or value == 1 or value == 2:
            self.write(f'TMDN {value}')
        else:
            print('Illegal value.')

    @property
    def tsha(self):
        """
        returns steinhart-hart coefficient a
        """
        return self.ask('TSHA?')

    @tsha.setter
    def tsha(self, value):
        """
        sets steinhart-hart coefficient a
        """
        self.write(f'TSHA {value}')

    @property
    def tshb(self):
        """
        returns steinhart-hart coefficient b
        """
        return self.ask('TSHB?')

    @tshb.setter
    def tshb(self, value):
        """
        sets steinhart-hart coefficient b
        """
        self.write(f'TSHB {value}')

    @property
    def tshc(self):
        """
        returns steinhart-hart coefficient c
        """
        return self.ask('TSHC?')

    @tshc.setter
    def tshc(self, value):
        """
        sets steinhart-hart coefficient c
        """
        self.write(f'TSHC {value}')

    @property
    def tntb(self):
        """
        returns beta model beta parameter
        """
        return self.ask('TNTB?')

    @tntb.setter
    def tntb(self, value):
        """
        sets beta model beta parameter
        """
        self.write(f'TNTB {value}')

    @property
    def tntr(self):
        """
        returns beta model r0 parameter
        """
        return self.ask('TNTR?')

    @tntr.setter
    def tntr(self, value):
        """
        sets beta model r0 parameter
        """
        self.write(f'TNTR {value}')

    @property
    def tntt(self):
        """
        returns beta model t0 parameter
        """
        return self.ask('TNTT?')

    @tntt.setter
    def tntt(self, value):
        """
        sets beta model t0 parameter
        """
        self.write(f'TNTT {value}')

    @property
    def trtr(self):
        """
        returns rtd linear model r0 parameter
        """
        return self.ask('TRTR?')

    @trtr.setter
    def trtr(self, value):
        """
        sets rtd linear model r0 parameter
        """
        self.write(f'TRTR {value}')

    @property
    def trta(self):
        """
        returns rtd linear model alpha parameter
        """
        return self.ask('TRTA?')

    @trta.setter
    def trta(self, value):
        """
        sets rtd linear model alpha parameter
        """
        self.write(f'TRTA {value}')

    @property
    def tlms(self):
        """
        returns lm335 slop parameter
        """
        return self.ask('TLMS?')

    @tlms.setter
    def tlms(self, value):
        """
        sets lm335 slop parameter
        """
        self.write(f'TLMS {value}')

    @property
    def tlmy(self):
        """
        returns lm335 offset parameter
        """
        return self.ask('TLMY?')

    @tlmy.setter
    def tlmy(self, value):
        """
        sets lm335 offset parameter
        """
        self.write(f'TLMY {value}')

    @property
    def tads(self):
        """
        returns ad590 slop parameter
        """
        return self.ask('TADS?')

    @tads.setter
    def tads(self, value):
        """
        sets ad590 slop parameter
        """
        self.write(f'TADS {value}')

    @property
    def tady(self):
        """
        returns ad590 offset parameter
        """
        return self.ask('TADY?')

    @tady.setter
    def tady(self, value):
        """
        sets ad590 offset parameter
        """
        self.write(f'TADY {value}')

    ##### tec trip-off #####

    @property
    def ttsf(self):
        """
        returns tec trip-off on thermometer fault status
        """
        return self.ask('TTSF?')

    @ttsf.setter
    def ttsf(self, value):
        """
        turns on and off tec trip-off on thermometer fault status
        """
        if value == 0 or value == 1:
            self.write(f'TTSF {value}')
        else:
            print('Illegal value.')

    @property
    def ttmx(self):
        """
        returns tec trip-off on max temperature status
        """
        return self.ask('TTMX?')

    @ttmx.setter
    def ttmx(self, value):
        """
        turns on and off tec trip-off on max temperature
        """
        if value == 0 or value == 1:
            self.write(f'TTMX {value}')
        else:
            print('Illegal value.')

    @property
    def ttmn(self):
        """
        returns tec trip-off on min temperature status
        """
        return self.ask('TTMN?')

    @ttmn.setter
    def ttmn(self, value):
        """
        turns on and off tec trip-off on min temperature
        """
        if value == 0 or value == 1:
            self.write(f'TTMN {value}')
        else:
            print('Illegal value.')

    @property
    def ttvl(self):
        """
        returns tec trip-off on voltage limit status
        """
        return self.ask('TTVL?')

    @ttvl.setter
    def ttvl(self, value):
        """
        turns on and off tec trip-off on voltage limit
        """
        if value == 0 or value == 1:
            self.write(f'TTVL {value}')
        else:
            print('Illegal value.')

    @property
    def ttil(self):
        """
        returns tec trip-off on current limit status
        """
        return self.ask('TTIL?')

    @ttil.setter
    def ttil(self, value):
        """
        turns on and off tec trip-off on current limit
        """
        if value == 0 or value == 1:
            self.write(f'TTIL {value}')
        else:
            print('Illegal value.')
