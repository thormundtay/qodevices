from os.path import join, dirname

def main():
    if input('Do you want to generate VISA driver from TMC? [Y/N] ').strip().upper() != 'Y':
        return
    
    dirname2 = lambda x: dirname(dirname(x))
    path_to_tmc = join(dirname2(__file__), 'anritsu/MS2732B_driver.py')
    path_to_visa = join(dirname2(__file__), 'anritsu/MS2732B_VISA_driver.py')
    path_to_visa_header = join(dirname(__file__), 'MS2732B_VISA_driver_header.txt')
    with open(path_to_tmc, 'r') as tmc_file:
        src = tmc_file.read()

    reference_line = "    def write_to_device(self) -> None:\n"
    idx = src.find(reference_line)
    if idx < 0:
        raise ValueError('write_to_device method missing?')
    
    with open(path_to_visa_header, 'r') as header_file:
        header = header_file.read()

    result = header + src[idx:]
    # print(result[:2400])

    with open(path_to_visa, 'w') as visa_file:
        visa_file.write(result)

    print("VISA file has been created!")
    

if __name__ == '__main__':
    main()
else:
    print("Do not import __generate_VISA_driver__...!")
    