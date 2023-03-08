import os

def main():
    if input('Do you want to generate VISA driver from TMC? [Y/N] ').strip().upper() != 'Y':
        return
    
    path_to_tmc = os.path.join(os.path.dirname(__file__), 'MS2732B_driver.py')
    path_to_visa = os.path.join(os.path.dirname(__file__), 'MS2732B_VISA_driver.py')
    path_to_visa_header = os.path.join(os.path.dirname(__file__), 'MS2732B_VISA_driver_header.txt')
    with open(path_to_tmc, 'r') as tmc_file:
        src = tmc_file.read()

    reference_line = "    def write_to_device(self) -> None:\n"
    idx = src.find(reference_line)
    if idx < 0:
        raise ValueError('write_to_device method missing?')
    
    with open(path_to_visa_header, 'r') as header_file:
        header = header_file.read()

    result = header + src[idx:]
    # print(result[:1950])

    with open(path_to_visa, 'w') as visa_file:
        visa_file.write(result)

    print("VISA file has been created!")
    

if __name__ == '__main__':
    main()
else:
    print("Do not import __generate_VISA_driver__...!")
    