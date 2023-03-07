#!/usr/bin/env python3
"""
Anritsu Spectrum Analyzer MS2732B driver

Thormund - 2023 Initial version for interacting with Anritsu PM2732B RF
    Spectrum Analyzer. Adds basic methods such as specifying Centre Frequency,
    Bandwidth, Averaging of Traces, and file saving methods.
"""

__all__ = ["AnritsuMS2732BDriver"]

import logging
from usbtmc.usbtmc import Instrument
from pyvisa import ResourceManager
from pyvisa.errors import VisaIOError
from time import sleep


class AnritsuMS2732BDriver(Instrument):
    def __init__(self, *args, **kwargs):
        """Generates instance of Anritsu MS2732B driver.

        Documentation is as provided in https://dl.cdn-anritsu.com/en-us/test-measurement/files/Manuals/Programming-Manual/10580-00176.pdf # noqa: E501
        or newer.
        Class is build on usbtmc library from python-ivi/python-usbtmc
        repository.
        """
        super().__init__(*args, **kwargs)
        # self.my_resource.flush()  # Not implemented

        # TODO: Store into class or it might get purged
        self.trace_preamble = None

        # See write_to_device method.
        self.delayed_write = False
        self.write_queue = []

    # Typecasts all methods and properties of self.my_resource to self
    # def __getattr__(self, __name: str):
    #     if __name in ('_logging_extra', '_resource_name', '_session', 'visalib'):
    #         return getattr(self.my_resource, __name)
    #     else:
    #         raise AttributeError(f"{__name = }")

    # def __del__(self) -> None:
    #     if self.my_resource._session is not None:
    #         # self.my_resource.flush()
    #         self.my_resource.close()

    def write_to_device(self) -> None:
        # To avoid VISA hangs, we queue up visa write commands, before
        # writing all commands to the device in one fell swoop.
        cmd = ";".join(self.write_queue)
        self.write_queue = [] # refresh the queue

        raise NotImplementedError

    # def close(self):
    #     # Inherited from self.my_resource
    #     self.__del__()

    @property
    def idn(self) -> str:
        return self.ask('*IDN?')

    # FORMat Subsystem:
    @property
    def format(self) -> str:
        """Returns format of data returned from certain commands.

        ASCii format returns the data in comma-separated ASCII format. The
        units are the current instrument units. This format requires many more
        bytes so it will be the slowest format.

        INTeger 32 values are signed 32-bit integers in little-endian byte
        order. This format returns the data in 4-byte blocks. The units are
        always mdBm. For example, if the measured result was -12.345 dBm, that
        value would be sent as -12345.

        REAL,32 values are 32-bit floating point numbers conforming to the IEEE
        754 standard in little-endian byte order. This format returns the data
        in 4-byte binary format. The units are the current instrument units.

        Both INTeger,32 and REAL,32 formats return a definite block length.
        Each transfer begins with an ASCII header such as #42204. The first
        digit represents the number of following digits in the header (in this
        example, 4). The remainder of the header indicates the number of bytes
        that follow the header (in this example, 2204). You then divide the
        number of following bytes by the number of bytes in the data format
        you’ve chosen (4 for both INTeger,32 and REAL,32...so 2204/4) to get
        the number of data points (in this example, 551).
        """
        return self.ask(":FORMat:READings:DATA?")

    @format.setter
    def format(self, value: str) -> None:
        """Sets format of data returned from certain commands.

        ASCii format returns the data in comma-separated ASCII format. The
        units are the current instrument units. This format requires many more
        bytes so it will be the slowest format.

        INTeger 32 values are signed 32-bit integers in little-endian byte
        order. This format returns the data in 4-byte blocks. The units are
        always mdBm. For example, if the measured result was -12.345 dBm, that
        value would be sent as -12345.

        REAL,32 values are 32-bit floating point numbers conforming to the IEEE
        754 standard in little-endian byte order. This format returns the data
        in 4-byte binary format. The units are the current instrument units.

        Both INTeger,32 and REAL,32 formats return a definite block length.
        Each transfer begins with an ASCII header such as #42204. The first
        digit represents the number of following digits in the header (in this
        example, 4). The remainder of the header indicates the number of bytes
        that follow the header (in this example, 2204). You then divide the
        number of following bytes by the number of bytes in the data format
        you’ve chosen (4 for both INTeger,32 and REAL,32...so 2204/4) to get
        the number of data points (in this example, 551).
        """
        if value not in (allowed_values := ('ASCii', 'INTeger,32', 'REAL,32',
                                            'ASC', 'INT', 'REAL')):
            raise ValueError(f"Illegal value of {value} passed into argument.")
        value = allowed_values[allowed_values.index(value) % 3]
        self.write(f":FORMat:READings:DATA {value}")

    # MMEMory Subsystem
    @property
    def mmem_msis(self) -> str:
        """Returns the storage location.

        Storage location can be independent for remote and front panel
        operation. INTernal refers to internal memerory, and USB for USB
        flash drive.
        Source: https://dl.cdn-anritsu.com/en-us/test-measurement/ohs/10450-00050N/index.html#page/Programming/Ch_SCPI_All_Modes.4.4.html # noqa: E501
        """
        return self.ask(":MMEMory:MSIS?")

    @mmem_msis.setter
    def mmem_msis(self, value: str):
        """Gets the storage location.

        Storage location can be independent for remote and front panel
        operation. INTernal refers to internal memerory, and USB for USB
        flash drive.
        Source: https://dl.cdn-anritsu.com/en-us/test-measurement/ohs/10450-00050N/index.html#page/Programming/Ch_SCPI_All_Modes.4.4.html # noqa: E501
        """
        allowed_value = ('INT', 'USB', 'INTernal')
        if value not in allowed_value:
            raise ValueError(f"Illegal value of {value} passed into argument.")
        self.write(f":MMEMory:MSIS {value}")

    def mmem_stor_trac(self, trc: int=1, file_name: str=None):
        """Stores the trace in trace A into the file specified by file_name.

        Parameters
        ----------
        trc : int
            Documentation claims this to be unimplemented, and to send a
            0. I suspect the number corresponds to trc A/B/C. Send a 1
            for A.
        file_name : str
            name_of_file to be saved_as
            file_name should not contain a file extension

        """
        self.write(f":MMEMory:STORe:TRACe {trc},'{file_name}'")

    # TRACe subsystem
    @property
    def trac_pre(self):
        """Returns header/preamble information.

        Documentation claims to return to return header information for a
        specified trace. This is not found to be true.
        """
        if self.trace_preamble is None:
            # Compulsory arguments given in documentation after `?` symbol
            # creates error. This is likely because the RF Spec An does not
            # have it as an in-built command.

            # TODO: process into list and update if new values?
            self.trace_preamble = self.ask(':TRACe:PREamble?')
        else:
            temp = self.ask(':TRACe:PREamble?')
            logging.INFO('trac_pre called more than once!')
            logging.INFO(f"query(':TRACe:PREamble?') has yielded:\n{temp}")
            if len(temp) > 3:
                print()
        return self.trace_preamble

    @property
    def trac_data(self, trc_type: str) -> None:
        """Transfers trace data from instrument to controller.

        Parameters
        ----------
        trc_type : str
            Trace type. ACLR | SPECtrum | EMISsion | DEMod
        """
        # return self.ask(f':TRACe:DATA? {trc_type}')
        print('"trac" VISA command tested to be faulty (as of Firmware V4.3).')
        return None

    @trac_data.setter
    def trac_data(self, trc_type: str, cmd: str) -> None:
        """Transfers trace data from controlling program to instrument.

        Parameters
        ----------
        trc_type : str
            Trace type. ACLR | SPECtrum | EMISsion | DEMod
        cmd : str
            The command ("block") to send.
        """
        # allowed_values = ('ACLR', 'SPECtrum', 'EMISsion', 'DEMod')
        # if trc_type not in allowed_values:
        #     raise ValueError(f"Illegal value of {trc_type} passed into argument.")

        # # number of bytes in command
        # x = len(bytearray(cmd.encode()))
        # # number of digits in x
        # a = len(str(x))
        # # pipe command
        # self.write(f':TRACe:DATA {trc_type},(#{a}{x}{cmd})')

        print('"trac:data" VISA command tested to be faulty (as of Firmware V4.3).')
        return None

    # INITiate Subsystem
    @property
    def init_cont(self) -> str:
        """Specifies if sweep measurement is continuously triggered."""
        return self.ask(":INITiate:CONTinuous?")

    @init_cont.setter
    def init_cont(self, value) -> None:
        """Sets continuously trigger of sweep/measurement."""
        on_val = (1, "1", "On", "ON", True)
        off_val = (0, "0", "Off", "OFF", False)
        if value in on_val:
            self.write(f":INITiate:CONTinuous 1")
        elif value in off_val:
            self.write(f":INITiate:CONTinuous 0")
        else:
            raise ValueError(f"Illegal value of {value} passed into argument.")

    def init_imm(self) -> None:
        """Initiates a sweep/measurement.

        If :INITitate:CONTinuous is set to ON, this command is ignored.
        Use this command in combination with :STATus:OPERation? to
        synchronize the capture of one complete set of data. When this
        command is sent, the “sweep complete” bit of :STATus:OPERation?
        is set to 0, indicating that the measurement has not completed.
        The data collection is then triggered. The controlling program
        can poll :STATus:OPERation? to determine the status. When the
        “sweep complete” bit is set to 1, data is ready to be retrieved.
        """
        self.write(":INITiate")
        # print(":INIT:IMM called!")
        sleep(0.1)

    @property
    def init_tgen(self) -> str:
        pass

    @init_tgen.setter
    def init_tgen(self, value) -> None:
        pass

    # SENSe subsystem: Device-specific parameters
    # SENSe:AVERage subsystem contains commands related to the combination of
    # data from consecutive sweeps.
    @property
    def sens_aver_coun(self) -> str:
        """Gets the number of traces to average"""
        return self.ask(":SENSe:AVERage:COUNt?")

    @sens_aver_coun.setter
    def sens_aver_coun(self, value: int) -> None:
        """Sets the number of traces to average"""
        try:
            value = int(value)
        except ValueError:
            raise ValueError(f"Illegal value of {value} passed into argument.")
        if value < 2 or value > 65535:
            raise ValueError(f"Illegal value of {value} passed into argument.")
        self.write(f":SENSe:AVERage:COUNt {value}")

    @property
    def sens_aver_type(self) -> str:
        """Gets how successive traces are combined to produce resulting value."""
        return self.ask(":SENSe:AVERage:TYPE?")

    @sens_aver_type.setter
    def sens_aver_type(self, value: str) -> None:
        """Sets how successive traces are combined to produce resulting value.

        Parameters
        ----------
        value : str
            Averaging type. NONE | SCALar | MAXimum | MINimum
            None is equivalent to setting "Norm" on the front panel.
            Scalar is equivalent to setting "Avg" on the front panel.
        """
        allowed_vals = ("NONE", "SCALar", "MAXimum", "MINimum")
        if value not in allowed_vals:
            raise ValueError(f"Illegal value of {value} passed into argument.")
        self.write(f":SENSe:AVERage:TYPE {value}")

    # SENSe:ROSCillator Subsystem - MS269xA Models
    # @property
    # def sens_rosc_ext_freq(self):
    # """Gets External Reference Frequency.
    #
    # Source: https://dl.cdn-anritsu.com/en-au/test-measurement/files/Manuals/Operation-Manual/MS269xA/MS269xA_2830A_40A_50A_Mainframe_Remote_Manual_e_39_0.pdf # noqa: E501
    # """
    #     return self.ask(':SENSe:ROSCillator:EXTernal:FREQuency?')

    # SENSe:BANDwidth subsystem contains commands related to filter bandwidth
    # of the instrument
    @property
    def sens_band_res(self) -> str:
        """Get the current resolution bandwidth.

        Returns
        -------
        sense_bandwith_resolution : str
            The current resolution bandwidth.
        """
        return self.ask(":SENSe:BANDwidth:RESolution?")

    @sens_band_res.setter
    def sens_band_res(self, bandwidth: float) -> None:
        """Set the resolution bandwidth.

        Parameters
        ----------
        bandwidth : float
            The new resolution bandwidth. Bandwith has to be between
            0 Hz to 3 MHz in a 1:3 sequence.
        """
        allowed_values = [1*(10**i) for i in range(7)] \
            + [3*(10**i) for i in range(7)]
        if bandwidth not in allowed_values:
            raise ValueError("The bandwidth value must be between 0 Hz and 3 MHz in a 1:3 sequence.")
        self.write(f":SENSe:BANDwidth:RESolution {bandwidth}")

    @property
    def sens_band_res_auto(self) -> str:
        """Get the current state of the resolution bandwidth coupling.

        Returns
        -------
        str
            The current state of the resolution bandwidth coupling. Returns 'ON' or 'OFF'.
        """
        response = self.ask(":SENSe:BANDwidth:RESolution:AUTO?").strip()
        if response == '1' or response == 'ON':
            return 'ON'
        elif response == '0' or response == 'OFF':
            return 'OFF'
        else:
            raise ValueError(f"Invalid response from instrument: {response}.")

    @sens_band_res_auto.setter
    def sens_band_res_auto(self, state: str) -> None:
        """Set the state of the resolution bandwidth coupling.

        Parameters
        ----------
        state : str
            The state of the resolution bandwidth coupling. Valid values are 'ON', '1', 'OFF', or '0'.

        Raises
        ------
        ValueError
            If an invalid state is provided.
        """
        allowed_states = {'ON', '1', 'OFF', '0'}
        if state not in allowed_states:
            raise ValueError(f"Invalid state value: {state}. Valid states are {allowed_states}.")

        self.write(f":SENSe:BANDwidth:RESolution:AUTO {state}")

    @property
    def sens_band_res_rat(self) -> float:
        """Get the current ratio of the resolution bandwidth to the span.

        Returns
        -------
        float
            The current ratio of the resolution bandwidth to the span.
        """
        return float(self.ask(":SENSe:BANDwidth:RESolution:RATio?"))

    @sens_band_res_rat.setter
    def sens_band_res_rat(self, ratio: float) -> None:
        """Set the ratio of the resolution bandwidth to the span.

        Parameters
        ----------
        ratio : float
            The ratio of the resolution bandwidth to the span. Must be
            within the range of 0.00001 to 1.
        """
        if not (0.00001 <= ratio <= 1):
            raise ValueError(f"Ratio must be within the range of 0.00001 to 1. Value entered: {ratio}")

        self.write(f":SENSe:BANDwidth:RESolution:RATio {ratio}")

    # video bandwidth - not implemented

    # SENSe:CORRection Subsystem
    # This subsystem provides commands for losses or gains external to the
    # instrument.

    # input impedance - not implemented

    # SENSe:DETector Subsystem
    # This subsystem includes commands that affect acquisition data points on
    # the instrument.
    @property
    def sens_det_func(self) -> str:
        """Get the current detection method for calculating each display point.

        Returns
        -------
        str
            The current detection method. Can be one of 'POSitive',
            'RMS', 'NEGative', or 'SAMPle'.
        """
        return self.ask(":SENSe:DETector:FUNCtion?")

    @sens_det_func.setter
    def sens_det_func(self, func: str) -> None:
        """Set the detection method for calculating each display point.

        Parameters
        ----------
        func : str
            The detection method. Can be one of 'POSitive', 'RMS',
            'NEGative', or 'SAMPle'.
        """
        allowed_funcs = {'POSitive', 'RMS', 'NEGative', 'SAMPle'}
        if func not in allowed_funcs:
            raise ValueError(f"Invalid detection function: {func}. Valid functions are {allowed_funcs}.")
        self.write(f":SENSe:DETector:FUNCtion {func}")

    # SENSe:FREQuency Subsystem
    # This subsystem includes commands in this subsystem pertain to the
    # frequency settings of the instrument.
    @property
    def sens_freq_cent(self) -> str:
        """Get the current center frequency setting.

        Returns
        -------
        center_freq : float
            The current center frequency setting in Hz.
        """
        return self.ask(":SENSe:FREQuency:CENTer?")

    @sens_freq_cent.setter
    def sens_freq_cent(self, center_freq: float) -> None:
        """Set the center frequency setting.

        Parameters
        ----------
        center_freq : float
            The desired center frequency setting in Hz.
            Must be in the range of 10 Hz to 7.099999995 GHz.
        """
        if not 10 <= center_freq <= 7.099999995e9:
            raise ValueError(f"Invalid center frequency value: {center_freq}."
                            "Center frequency must be in the range of 10 Hz to 7.099999995 GHz.")
        self.write(f":SENSe:FREQuency:CENTer {center_freq} HZ")

    @property
    def sens_freq_span(self) -> str:
        """Get the current frequency span setting.

        Returns
        -------
        freq_span : str
            The current frequency span.
        """
        return self.ask(":SENSe:FREQuency:SPAN?")

    @sens_freq_span.setter
    def sens_freq_span(self, freq_span: float) -> None:
        """Set the frequency span.

        Parameters
        ----------
        freq_span : float
            The desired frequency span in Hz. Must be within the range
            of 0 Hz and 7.1 GHz.
        """
        if not 0 <= freq_span <= 7.1e9:
            raise ValueError(f"Invalid frequency span: {freq_span}."
                             "Frequency span must be between 0 Hz and 7.1 GHz.")
        self.write(f":SENSe:FREQuency:SPAN {freq_span} HZ")

    @property
    def sens_freq_span_full(self) -> None:
        """Set the frequency span to full span."""
        self.write(":SENSe:FREQuency:SPAN:FULL")

    @property
    def sens_freq_start(self) -> str:
        """Get the current start frequency.

        Returns
        -------
        str
            The current start frequency in Hz.
        """
        return self.ask(":SENSe:FREQuency:STARt?")

    @sens_freq_start.setter
    def sens_freq_start(self, start_freq: float) -> None:
        """Set the start frequency.

        Parameters
        ----------
        start_freq : float
            The desired start frequency in Hz. Must be within the valid range.
        """
        if not (0 <= start_freq <= 7.1e9):
            raise ValueError(f"Start frequency must be within the range of 10 Hz to 7.1 GHz. Received: {start_freq}")

        self.write(f":SENSe:FREQuency:STARt {start_freq} HZ")

    @property
    def sens_freq_stop(self) -> str:
        """Get the current stop frequency value.

        Returns
        -------
        freq_stop
            The current stop frequency in Hz.
        """
        return self.ask(":SENSe:FREQuency:STOP?")

    @sens_freq_stop.setter
    def sens_freq_stop(self, freq: float) -> None:
        """Set the stop frequency.

        Parameters
        ----------
        freq : float
            The stop frequency to set in Hz. The range is from 10 Hz to 7.1 GHz.
        """
        if not 10 <= freq <= 7.1e9:
            raise ValueError(f"Invalid frequency value: {freq}. The range is from 10 Hz to 7.1 GHz.")

        self.write(f":SENSe:FREQuency:STOP {freq}")

    # SENSe:POWer Subsystem
    # This subsystem relates to power amplitude parameters of the instrument.
    @property
    def sens_pow_rf_att(self) -> str:
        """Get the current input attenuation.

        Returns
        -------
        atten : str
            The current input attenuation in dB.
        """
        return self.ask(":SENSe:POWer:RF:ATTenuation?")

    @sens_pow_rf_att.setter
    def sens_pow_rf_att(self, atten: float) -> None:
        """Set the input attenuation.

        Parameters
        ----------
        atten : float
            The desired input attenuation in dB. Must be between 0 and 65 dB.
        """
        if not 0 <= atten <= 65:
            raise ValueError(f"Invalid attenuation value: {atten} dB. Attenuation must be between 0 and 65 dB.")
        self.write(f":SENSe:POWer:RF:ATTenuation {atten} dB")

    @property
    def sens_pow_rf_att_auto(self) -> bool:
        """Get the state of the input attenuation coupling.

        Returns
        -------
        state : bool
            The current state of the input attenuation coupling. Returns True for ON
            and False for OFF.
        """
        return self.ask(":SENSe:POWer:RF:ATTenuation:AUTO?")

    @sens_pow_rf_att_auto.setter
    def sens_pow_rf_att_auto(self, state: str) -> None:
        """Set the state of the input attenuation coupling.

        Parameters
        ----------
        state : str
            The state of the input attenuation coupling. Valid values are 'ON', '1',
            'OFF', or '0'.
        """
        allowed_states = {'ON', '1', 'OFF', '0'}
        if state not in allowed_states:
            raise ValueError(f"Invalid state value: {state}. Valid states are {allowed_states}.")

        self.write(f":SENSe:POWer:RF:ATTenuation:AUTO {state}")

    @property
    def sens_pow_rf_gain_stat(self) -> str:
        """Get the state of the preamp.

        Returns
        -------
        sens_pow_rf_gain_stat : str
            The current state of the preamp.
        """
        return self.ask(":SENSe:POWer:RF:GAIN:STATe?")

    @sens_pow_rf_gain_stat.setter
    def sens_pow_rf_gain_stat(self, state: str) -> None:
        """Set the state of the preamp.

        Parameters
        ----------
        state : str
            The state of the preamp. Valid values are 'ON', '1', 'OFF', or '0'.
        """
        allowed_states = {'ON', '1', 'OFF', '0'}
        if state not in allowed_states:
            raise ValueError(f"Invalid state value: {state}. Valid states are {allowed_states}.")

        self.write(f":SENSe:POWer:RF:GAIN:STATe {state}")

    # SENSe:SWEep Subsystem
    # This subsystem contains commands that affect the sweep generator of the
    # instrument.
    @property
    def sens_swe_time(self) -> str:
        """Get the minimum sweep time.

        Returns
        -------
        float
            The minimum sweep time in seconds.
        """
        return self.ask(":SENSe:SWEep:TIME?")

    @sens_swe_time.setter
    def sens_swe_time(self, time: float) -> None:
        """Set the minimum sweep time.

        Parameters
        ----------
        time : float
            The minimum sweep time in seconds. Must be in the range
            [10e-6, 600] seconds.
        """
        if not 10e-6 <= time <= 600:
            raise ValueError(f"Invalid sweep time: {time}. Must be in the range [10e-6, 600e6].")

        self.write(f":SENSe:SWEep:TIME {time} s")

    # SENSe:STATus Subsystem
    # This subsystem contains commands relating to the current operating state
    # of the instrument
    @property
    def stat_oper(self) -> int:
        """Get information about the current status of the instrument.

        Returns
        -------
        stat_oper : int
            The decimal representation of the bit-wise OR of the enabled bits.
            int(0, 2) - When command INIT:IMM is sent to trigger a sweep.
            int(00000000_1000000, 2) - When sweep is complete/
            For other bits, please refer to documentation.
        """
        return int(self.ask(":STATus:OPERation?"))
