#
# Title: USB IO Expander IIC Test program.
#
# Author: Rob Jansen, Copyright (c) 2024..2024, all rights reserved.
#
# Description: Python script for testing the USB IO Expander IIC functionality.
#              This program sets the output pins and read the latch register of the MCP23S08.
#
import sys
import time
from usb_io_expander import default_comport,get_default_comport, serial_init, serial_end, iic_init, \
                            iic_write, iic_read

slave_address = 0x40  # A0, A1 and A2 connected to GND.

if __name__ == "__main__":
    # Main program starts here.
    comport = get_default_comport()
    print("Script for testing the USB IO Expander.")

    # If the argument count is 1 we assume the default port.
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
        exit(1)

    # IODIR register, all pins Output.
    if iic_write(slave_address, [0x00, 0x00]):
        print("Port set to output")
    else:
        print("Could not set port to output.")
        sys.exit(1)

    # Port register, all pins HIGH
    if iic_write(slave_address, [0x09, 0xFF]):
        print("All port pins set to HIGH.")
    else:
        print("Could not set all port pins to HIGH.")
        sys.exit(1)
    time.sleep(1)

    # Port register, all pins LOW.
    if iic_write(slave_address, [0x09, 0x00]):
        print("All port pins set to LOW.")
    else:
        print("Could not set all port pins to LOW.")
        sys.exit(1)
    time.sleep(1)

    print("Running tests, press <ctrl-c> to stop. ")
    # Set individual pins.
    while True:
        data = 0x01
        for x in range(8):
            if not iic_write(slave_address, [0x09, data]):  # Port register.
                print("Could not set port register.")
                sys.exit(1)
            data = data << 1

            # Read the latch.
            if not iic_write(slave_address, [0x0A]):  # Latch register.
                print("Could not set latch register.")
                sys.exit(1)
            command_ok, iic_data = iic_read(slave_address, 1)
            if command_ok:
                print("Latch data is: ", iic_data[0])
            time.sleep(0.5)

        data = 0x80
        for x in range(8):
            if not iic_write(slave_address, [0x09, data]):  # Port register.
                print("Could not set port register.")
                sys.exit(1)
            data = data >> 1

            # Read the latch.
            if not iic_write(slave_address, [0x0A]):  # Latch register.
                print("Could not set latch register.")
                sys.exit(1)
            command_ok, iic_data = iic_read(slave_address, 1)
            if command_ok:
                print("Latch data is: ", iic_data[0])
            time.sleep(0.5)

    serial_end()
    sys.exit(0)
