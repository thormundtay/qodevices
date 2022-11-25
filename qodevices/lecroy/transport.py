"""
LeCroyDSO initializers

Thormund 25 Nov 2022 - Add functions for ease of connecting to DSO via USBTMC
"""
__all__ = [
        "get_oscilloscope_addr",
        "connect_dso"
    ]

from pyvisa import ResourceManager
from lecroydso import LeCroyVISA, LeCroyDSO
from lecroydso.errors import DSOConnectionError

def get_oscilloscope_addr() -> list:
    """
    Returns possible list of pyvisa resource addresses that contain Lecroy 
    Oscilloscopes.
    """
    def filter_by_id(x: str):
        # Example: 'USB0::1535::4131::3505N05494::0::INSTR' 
        # USB[board]::manufacturer ID::model code::serial number
        # [::USB interface number][::INSTR]
        # Hardcoded Manufacturer ID: 1535
        if x.split("::")[1] == '1535':
            return True
        return False
    return list(filter(filter_by_id, ResourceManager().list_resources()))

def connect_dso(resource_address: str, log: bool=False) -> LeCroyDSO:
    """Instance of communication interface to a LeCroy Oscilloscope."""
    try:
        return LeCroyDSO(LeCroyVISA(resource_address), log)
    except DSOConnectionError:
        print('Oscilliscope could not be connected to.')
        return

if __name__ == '__main__':
    print(f"{get_oscilloscope_addr() = }")
    