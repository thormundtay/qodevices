#!/usr/bin/env python3
"""
Thorlabs PAX1000 Polarimeter driver

Thormund - 2023 Initial version for interacting with Thorlabs Polarimeter
    Includes stokes vector and polarisation calculation in class property
"""

__all__ = ["thorlabsPolarimeterDriver"]

from usbtmc.usbtmc import Instrument
from time import sleep
from numpy import sin, cos


class thorlabsPolarimeterDriver(Instrument):
    def __init__(self, *args, **kwargs):
        """Generates instance of Thorlabs Polarimeter driver.

        Documentation is as provided in https://www.thorlabs.com/drawings/8512900868b3b5c8-13B2EB4C-9369-765B-B4E7D54A9C22E936/PAX1000IR1-WriteYourOwnApplication.pdf # noqa: E501
        or newer.
        Class is build on usbtmc library from python-ivi/python-usbtmc
        repository.
        """
        super().__init__(*args, **kwargs)

    # convenience commands
    def initialize(self):
        """High level implementation to get PAX started.

        Values provided in this func might not necessarily be what you want.
        """
        self.sens_calc_mode(9)
        print("PAX has been set to averaging mode 9")
        self.inp_rot_stat(1)
        print("PAX waveplates are now set to rotating")
        sleep(0.5)
        assert self.sens_calc_mode == "9"
        assert self.inp_rot_stat

    def get_stokes(self) -> tuple(float):
        """High level implementation to get Stokes vector parameters.

        Returns (Ptotal, Normalized S1, S2, S3)
        """
        (
            rev,
            timestamp,
            paxOpMode,
            paxFlags,
            paxTIARange,
            adcMin,
            adcMax,
            revTime,
            misAdj,
            theta,
            eta,
            DOP,
            Ptotal,
        ) = map(float, self.sens_data_lat.rstrip("\n").split(","))
        return (
            Ptotal,
            cos(2 * theta) * cos(2 * eta),
            sin(2 * theta) * cos(2 * eta),
            sin(2 * eta),
        )

    # visa commands, as given by manual

    @property
    def sens_calc_mode(self) -> str:
        return self.query("SENSe:CALCulate:MODe?")

    @sens_calc_mode.setter
    def sens_calc_mode(self, value):
        """Sets averaging mode"""
        try:
            value = int(value)
        except ValueError:
            pass
        allowed_values = list(range(1, 10)) + [
            i + j for i in ["H", "F", "D"] for j in ["512", "1024", "2048"]
        ]
        if value not in allowed_values:
            raise ValueError(f"Illegal value of {value} passed into argument.")
        self.write(f"SENSe:CALCulate:MODe {value}")

    @property
    def sens_corr_wav(self):
        """Returns wavelength in meters"""
        pass  # Not implemented here at the moment

    @sens_corr_wav.setter
    def sens_corr_wav(self, value):
        """Sets wavelength in meters"""
        pass  # Not implemented here at the moment

    @property
    def sens_pow_rang_upp(self):
        """Returns the most positive signal level in Watt the sensor input
        can handle in the active transimpedance amplifier configuration with
        any polarization state."""
        pass  # Not implemented here at the moment

    @sens_pow_rang_upp.setter
    def sens_pow_rang_upp(self, value):
        """Specify the most positive signal level expected of sensor input."""
        pass  # Not implemented here at the moment

    @property
    def sens_pow_rang_auto(self):
        """Returns the auto ranging."""
        pass  # Not implemented here at the moment

    @sens_pow_rang_auto.setter
    def sens_pow_rang_auto(self, value):
        """Sets the RANGe to the value determined to give the most dynamic
        range without overloading."""
        allowed_values = (0, 1, 2, "OFF", "ON", "ONCE", "0", "1", "2")
        if value not in allowed_values:
            raise ValueError(f"Illegal value of {value} passed into argument.")
        pass  # Not implemented here at the moment

    @property
    def sens_pow_rang_ind(self, value=None) -> str:
        """Returns the currently active power range index."""
        if value is not None:
            if value not in ("MIN", "MAX"):
                raise ValueError(
                    f"Illegal value of {value} passed into argument."
                )
            return self.query(f"SENSe:POWer:RANGe:INDex? {value}")
        else:
            return self.query("SENSe:POWer:RANGe:INDex?")

    @sens_pow_rang_ind.setter
    def sens_pow_rang_ind(self, value):
        """Sets the power range with specified index, with 1 being least
        sensitive, and 16 being the most sensitive."""
        allowed_values = (
            list(range(1, 17)) + list(map(str, range(1, 17))) + ["MIN", "MAX"]
        )
        if value not in allowed_values:
            raise ValueError(f"Illegal value of {value} passed into argument.")
        pass  # Not implemented here at the moment

    @property
    def sens_pow_rang_nom(self) -> str:
        """Returns the most positive signal level in Watt the specified
        power range index can handle with any polarization state. If no
        index is specified the parameter defaults to the currently
        active index and the command is identical to SENS:POW:RANG:UPP?"""
        pass  # Not implemented here at the moment

    # @property
    def sens_data_lat(self) -> str:
        """Returns the latest completed primary measurement data set

        rev, timestamp, paxOpMode, paxFlags, paxTIARange, adcMin, adcMax,
        revTime, misAdj, theta, eta, DOP, Ptotal
        """
        return self.query("SENS:DATA:LATest?")

    @property
    def inp_rot_stat(self) -> bool:
        """Returns waveplate motor state"""
        return bool(int(self.query("INPut:ROTation:STATe?")))

    @inp_rot_stat.setter
    def inp_rot_stat(self, value):
        """Sets waveplate rotation"""
        t_values = (1, "On", True, "1")
        f_values = (0, "Off", False, "0")
        if (value not in t_values) or value not in (f_values):
            raise ValueError(f"Illegal value of {value} passed into argument.")

        if value in f_values:
            self.write("INPut:ROTation:STATe 0")
        elif value in t_values:
            self.write("INPut:ROTation:STATe 1")

    @property
    def inp_rot_vel(self) -> float:
        """Returns the waveplate rotation velocity in Hz."""
        return float(self.query("INPut:ROTation:VELocity?"))

    @inp_rot_vel.setter
    def inp_rot_vel(self, value):
        """Set the waveplates rotation velocity in Hz.

        Note: The value range depends on the selected measurement mode
        and the power supply state. Changing these conditions will
        coerce the set value to the new limits.
        """
        try:
            value = float(value)
        except ValueError:
            pass  # do nothing

        if not isinstance(value, float) and value not in ("MIN", "MAX", "DEF"):
            raise ValueError(
                f"Illegal value of {value} passed into argument.\
                \nOnly floats, float-like strings and 'MIN', 'MAX', 'DEF' are \
                allowed."
            )

        self.write(f"INPut:ROTation:VELocity {value}")

    # @property
    def inp_rot_vel_lim(self) -> str:
        """Returns the maximum waveplate rotation velocity in Hz with
        and without an external power supply."""
        return self.query("INPut:ROTation:VELocity?")
