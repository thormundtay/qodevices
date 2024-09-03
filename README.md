# QO Devices
This repository is designed for Python 3.10+, to replace the `~/programs/python_general/devices` folder that was intended for Py 3.6 and built on an unknown/outdated instance of `usbtmc`.

## Installation
Dependencies:
1. Linux Packages
On OpenSUSE Leap, run  
```# zypper install python3-usb python3-pyserial```
2. Python Packages
The version of usbtmc used by this package is **strictly** from [this usbtmc github repository](https://github.com/python-ivi/python-usbtmc).
Installation **in the appropriate version of python** (see pyenv/[venv](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/)) can be done via
```$ pip install https://github.com/user/repository/archive/branch.zip```
Edit the URL as appropriate. Do take note that the URL ends with a `.zip`.
pyserial utilised by this package is as provided pip.
**Alternatively**, the provided `requirements.txt` provides the necessary dependencies, and can be installed just by calling `pip install -r requirements.txt` (in the appropriate `$PWD`).  
In the event that the linux packages were not previously installed, installing python from source to allow the dependencies to populate the backend is necessary. For example on pyenv, this can easily be done by ```$ pyenv install 3.10.5``` for example.
3. Device permissions/udev
In contrast to the recommendations of `python-ivi/python-usbtmc`, please ensure that udev rules have `0666` instead of `0660` for permissions. Further details are as documented in Confluence.

This package:
```$ pip install -e <path/url>```
The `-e` flag ensures that the package is installed in "develop" mode, and will reference the file in its current location. Removing it will fail importing of the package.

For a stable version directly from github, please use  
```$ pip install git+ssh://git@github.com/the-fibre-lab/python_drivers.git``` or equivalently without SSH access,  
```$ pip install https://github.com/the-fibre-lab/python_drivers.git``` if the repository was public.

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
├── pyproject.toml <- **name as showing in pip is inherited from here!**
├── README.md
└── requirements.txt
```
To utilise in a python script (under the same python environment), an example script to demonstrate the import structure is as such
```python
from qodevices.thorlabs.thorlabs_laser_driver import thorlabsLaserDriver as ldc
from usbtmc import list_resources

# establish connection
itc = ldc(list_resources()[0])

# read temp
print(f"{itc.idn = }")
print(f"{itc.meas_temp = }")
```

## Managing IVI's backend - NI-Visa
To work with some other equipment in the lab, [NI's Visa](https://www.ni.com/en/support/downloads/drivers/download.ni-linux-device-drivers.html) was settled with.
Installation instructions are as provided [here](https://www.ni.com/docs/en-US/bundle/ni-platform-on-linux-desktop/page/installing-ni-products-opensuse.html).
The only relevant packages are probably `ni-visa` and `ni-visa-headers`. A
repository change might necessitate the use of `(sudo) zypper install --force
<packagename>`.

Note that different backends can be invoked from `pyvisa-shell` with the use of
the `-b` flag.
From within a python script, the environment variable `PYVISA_LIBRARY`. Note
that they may impact devices discoverability.

### Upgrading NI-Visa
1. Have the OpenSUSE local point to the new URL's. The files can be found under
   `/etc/zypp/repos.d/`, edit as accordingly to point to the URL. Please check
that version of OpenSUSE being used is supported!
2. As in accordance with the installation instructions, run `(sudo) dkms
   autoinstall`.
   a. If `dkms.conf` could not be found or similar, ensure that the older
      version of NI-Visa installation, along with build artefacts have been
      removed.
   b. Places to check would include `/var/lib/dkms/` and `/lib/modules`, please
      remove **only** the outdated version from the relevant NIPalk/NIKal/...
      folder.
   Do not forget to reboot after the dkms install!
