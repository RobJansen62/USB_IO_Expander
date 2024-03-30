#
# Title: USB IO Expander Pin Input Test program.
#
# Author: Rob Jansen, Copyright (c) 2023..2024, all rights reserved.
#
# Description: Python script for testing the USB IO Expander Pin output functionality.
#

import sys
import time
from usb_io_expander import default_comport, get_default_comport, serial_init, serial_end, pin_bit_direction, \
                            pin_bit_mode, pin_bit_pull_up, pin_bit_write, pin_byte_direction, pin_bit_read, \
                            pin_byte_read


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

    # Set all pins to input.
    if pin_byte_direction(0xFF):
        print("Pins set to input.")
    else:
        print("Could not set pins to input.")

    # Enable pull-up on pin 6 and 7. Other pins have no internal pull-up.
    if pin_bit_pull_up(6, 1):
        print("Pin 6 pull_up enabled.")
    else:
        print("Could not enable pin 6 pull-up.")
    if pin_bit_pull_up(7, 1):
        print("Pin 7 pull_up enabled.")
    else:
        print("Could not enable pin 6 pull-up.")

    # Pins 0, 1, 2, 3 and 6 can be set to analog, change them to digital (0).
    # Other pins are always digital. Just exit when an error occurs.
    if not pin_bit_mode(0, 0):
        print("Could not set pin 0 to digital.")
        exit(1)
    if not pin_bit_mode(1, 0):
        print("Could not set pin 1 to digital.")
        exit(1)
    if not pin_bit_mode(2, 0):
        print("Could not set pin 2 to digital.")
        exit(1)
    if not pin_bit_mode(3, 0):
        print("Could not set pin 3 to digital.")
        exit(1)
    if not pin_bit_mode(6, 0):
        print("Could not set pin 6 to digital.")
        exit(1)

    print("Running tests, press <ctrl-c> to stop. ")
    while True:
        # Get the status of all pins.
        command_ok, port_status = pin_byte_read()
        if command_ok:
            print("Port status is: {:02x}".format(port_status[0]))
        else:
            print("Could not obtain port status.")

        # Get the status of each individual pin.
        for pin in range(8):
            command_ok, pin_status = pin_bit_read(pin)
            if command_ok:
                print("Pin status is of pin {:g} is {:02X}".format(pin, pin_status[0]))
            else:
                print("Could not obtain pin status.")

        print("")
        time.sleep(1)

    serial_end()
    sys.exit(0)
