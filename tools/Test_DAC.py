#
# Title: USB IO Expander DAC Test program.
#
# Author: Rob Jansen, Copyright (c) 2024..2024, all rights reserved.
#
# Description: Python script for testing the USB IO Expander DAC functionality.
#              It sets the DAC to the minimum and maximum value and
#              writes 0..31 to the DAC until ctrl-c is pressed.
#
#
import sys
import time
from usb_io_expander import default_comport, get_default_comport, serial_init, serial_end, dac_init, dac_enable, \
                            dac_disable, dac_write

# There are two DACs, 1 and 2
selected_dac = 1

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

    if dac_init(selected_dac):
        print("DAC initialized")
    else:
        print("Could not initialize DAC")
        sys.exit(1)

    if dac_enable():
        print("DAC enabled.")
    else:
        print("Could not enable DAC")
        sys.exit(1)

    print("Starting DAC test, press <ctrl-c> to stop")
    while True:
        print("Setting DAC to minimum and maximum value.")
        if not dac_write(0):
            print("Could not set DAC minimum value.")
            sys.exit(1)
        time.sleep(5)

        if not dac_write(31):
            print("Could not set DAC maximum value.")
            sys.exit(1)
        time.sleep(5)

        print("Setting DAC values from 0..31.")
        for dac_value in range(32):
            if dac_write(dac_value):
                print("Dac value is: ", dac_value)
                time.sleep(0.5)
            else:
                sys.exit(1)

    serial_end()
    sys.exit(0)
