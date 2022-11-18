# QO Devices
This repository is designed for Python 3.10+, to replace the `~/programs/python_general/devices` folder that was intended for Py 3.6 and built on an unknown/outdated instance of `usbtmc`.

## Installation
Dependencies:
1. Linux Packages
On OpenSUSE Leap, run
```# zypper install python3-usb```
2. Python Packages
The version of usbtmc used by this package is **strictly** from [this usbtmc github repository](https://github.com/python-ivi/python-usbtmc).
Installation **in the appropriate version of python** (see pyenv/[venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)) can be done via
```$ pip install https://github.com/user/repository/archive/branch.zip```
Edit the url as appropriate. Do take note that the url ends with a `.zip`.
pyserial utilised by this package is as provided pip.
**Alternatively**, the provided `requirements.txt` provides the necessary dependencies, and can be installed just by calling `pip install -r requirements.txt` (in the appropriate `$PWD`).
3. Device permissions/udev
In contrast to the recommendations of `python-ivi/python-usbtmc`, please ensure that udev rules have `0666` instead of `0660` for permissions. Further details are as documented in Confluence.

This package:
```$ pip install -e <path/url>```
The `-e` flag ensures that the package is installed in "develop" mode, and will reference the file in its current location. Removing it will fail importing ofthe package.

## Usage example
After installing, ensure that the package shows up under `pip list`. The package name should be `qodevices`.
The system tree should look something like
```
. <installation location>
├── qodevices <- **this is the package name!**
│   ├── baseclass
│   │   └── ...
│   ├── homemade
│   │   └── ...
│   ...
├── tests
│   └── ...
├── pyproject.toml
├── README.md
└── requirements.txt
```
To utilise in a python script (under the same python environment), an example script to examplify the import structure is as such
```python
from qodevices.thorlabs.thorlabs_laser_driver import thorlabsLaserDriver as ldc
from usbtmc import list_resources

# establish connection
itc = ldc(list_resources()[0])

# read temp
print(f"{itc.idn = }")
print(f"{itc.meas_temp = }")
```
