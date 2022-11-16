# QO Devices
This repository is designed to replace the `~/programs/python_general/devices` folder that was intended for Py 3.6 and built on an unknown/outdated instance of `usbtmc`.

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
todo: pip install pyserial
3. Device permissions/udev  
In contrast to the recommendations of `python-ivi/python-usbtmc`, please ensure that udev rules have `0666` instead of `0660` for permissions. Further details are as documented in Confluence.

This package:  
```$ pip install -e <path/url>```  
The `-e` flag ensures that the package is installed in "develop" mode, and will reference the file in its current location. Removing it will fail the package

