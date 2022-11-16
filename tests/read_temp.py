from sys import version_info
# this file is for the debugging of 3.6 in contrast to 3.10

def devices_devel_read(num):
    if version_info.minor != 10:
        print("Please run Python 3.10 for this function.")
        return
    from qodevices.thorlabs.thorlabs_laser_driver import thorlabsLaserDriver as ldc
    from usbtmc import list_resources
    if False:
        print(help(ldc))

    # establish connection
    print(f"{list_resources() = }")
    for rsc in list_resources():
        itc = None
        if 'M' in rsc:
            print(f"{rsc = }")
            itc = ldc(rsc)
            # rm = pyvisa.ResourceManager()
            # itc = rm.open_resource(rsc)
            break

    if itc == None:
        print("Connection could not be established!")
        return
    
    # read temp
    print(f"{itc.idn = }")
    match num:
        case 0:
            for i in range(120):
                _ = itc.meas_curr
                if not i:
                    print(f"{itc.meas_curr = }")
        case 1:
            for i in range(15):
                print(f"{itc.meas_curr = }")
        case _:
            print("Unknown num given")
    itc.close() # in case
    return

def devices_devel_context_read():
    if version_info.minor < 10:
        print("Please run Python 3.10 for this function.")
        return
    from qodevices.thorlabs.thorlabs_laser_driver import managed_thorlabsLaserDriver as ldc
    from usbtmc import list_resources
 
   # establish connection
    print(f"{list_resources() = }")
    for rsct in list_resources():
        rsc = None
        if 'M' in rsct:
            rsc = rsct
            print(f"{rsc = }")
	    # rm = pyvisa.ResourceManager()
            # itc = rm.open_resource(rsc)
            break

    if rsc == None:
        print("Connection could not be established!")
        return
    
    # read temp
    with ldc(rsc) as itc:
        print(f"{itc.idn = }")
        for i in range(120):
            _ = itc.meas_temp
            if not i:
                print(f"{itc.meas_temp = }")
    return 

if __name__ == '__main__':
    # new_usbtmc()
    # new_usbtmc_context()
    # devices_devel_read(1)
    devices_devel_context_read()
