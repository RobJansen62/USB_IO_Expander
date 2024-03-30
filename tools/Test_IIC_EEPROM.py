#
# Title: USB IO Expander IIC Test program.
#
# Author: Rob Jansen, Copyright (c) 2024..2024, all rights reserved.
#
# Description: Python script for testing the USB IO Expander IIC functionality. This program writes data to
#              an EEPROM, type AT24C32 and then reads the data back.
#
#
import sys
from usb_io_expander import default_comport, get_default_comport, serial_init, serial_end, iic_init, \
                            iic_write, iic_read

slave_address = 0xAE

# The EEPROM write data start with the sub address and the data to be written.
eeprom_write_data = [0x00, # Word high byte sub address
                     0x00, # Word low byte sub address
                     0x01, 0x02, 0x03, 0x04, 0x05, 0x06, 0x07, 0x08, 0x09, 0x0A] # Data

if __name__ == "__main__":
    # Main program starts here.
    comport = get_default_comport()
    print("Script for testing the USB IO Expander.")

    if len(sys.argv) == 2:
        comport = sys.argv[1]

    if comport == default_comport:
        print("An optional argument <comport> can be given for the serial connection to be used.")
        print("Currently using serial connection:", comport)
    else:
        print("Using serial connection:", comport)

    if not serial_init(comport):
        sys.exit(1)

    # Select 400 kHz IIC clock speed.
    if iic_init(4):
        print("IIC initialized")
    else:
        print("Could not initialize IIC interface")
        sys.exit(1)

    if iic_write(slave_address, eeprom_write_data):
        print("IIC data written.")
    else:
        print("Could not write IIC data.")
        sys.exit(1)

    if iic_write(slave_address, [0, 0]):  # Sub address is word.
        print("Resetting the sub address.")
    else:
        print("Could not write sub address.")
        sys.exit(1)

    command_ok, iic_data = iic_read(slave_address, 20)
    if command_ok:
        print("IIC data read.")
        for data in iic_data:
             hex_byte = ("{:02X}".format(data))
             print(hex_byte, end=' ')
        print()
    else:
        print("Could not read IIC data.")
        sys.exit(1)

        serial_end()
        sys.exit(0)
