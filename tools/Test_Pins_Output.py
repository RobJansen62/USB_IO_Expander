#
# Title: USB IO Expander Pin Output Test program.
#
# Author: Rob Jansen, Copyright (c) 2023..2024, all rights reserved.
#
# Description: Python script for testing the USB IO Expander Pin output functionality.
#              For this test, LEDs are connected to all 8 pins.
#

import sys
import time
from usb_io_expander import default_comport, get_default_comport, serial_init, serial_end, pin_bit_direction, \
                            pin_bit_write, pin_bit_pull_up, pin_byte_direction, pin_byte_write


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

    # Set all pins to output.
    if pin_byte_direction(0x00):
        print("Pins set to output.")
    else:
        print("Could not set pins to output.")

    print("Switching all pins to LOW.")
    # All pins low.
    if not pin_byte_write(0x00):
        print("Could not set all pins to LOW.")
    time.sleep(1)

    print("Running tests, press <ctrl-c> to stop.")
    while True:

        # All pins high.
        if not pin_byte_write(0xFF):
            print("Could not set all pins to HIGH.")
        time.sleep(1)

        # All pins low.
        if not pin_byte_write(0x00):
            print("Could not set all pins to LOW.")
        time.sleep(1)

        print("Switching individual pins to output,high and low.")
        for pin in range(8):
           pin_bit_write(pin, 1)
           time.sleep(0.5)
        for pin in range(8):
           pin_bit_write(pin, 0)
           time.sleep(0.5)

        # Force an error by using a non-existent pin.
        if not pin_bit_write(8, 0):
            print("Error since pin 8 does not exist.")

    serial_end()
    sys.exit(0)
