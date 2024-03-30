#
# Title: USB IO Expander ADC Test program.
#
# Author: Rob Jansen, Copyright (c) 2024..2024, all rights reserved.
#
# Description: Python script for testing the USB IO Expander ADC functionality.
#              A potentiometer is connected to the selected ADC input and the ADC value is written.
#
#
import sys
import time
from usb_io_expander import default_comport, get_default_comport, serial_init, serial_end, dac_init, dac_enable, \
                            dac_disable, dac_write, adc_init, adc_enable, adc_disable, adc_read, adc_channel

# There are 5 ADC channels: 3, 4, 5, 6 and 7.
selected_adc = 4  # Used at initialization
changed_adc = 3   # Just used for testing the channel change.

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

    if adc_init(selected_adc):
        print("ADC initialized using channel ", selected_adc)
    else:
        print("Could not initialize ADC.")
        sys.exit(1)

    if adc_enable():
        print("ADC enabled.")
    else:
        print("Could not enable ADC")
        sys.exit(1)

    # Change the channel. This is just for testing.
    if not adc_channel(changed_adc):
        print("Could not select a new ADC channel.")
        exit(1)

    while True:
        # Read the ADC.
        command_ok, adc_data = adc_read()
        if command_ok:
            print("ADC Data is: ", (adc_data[0] * 256) + adc_data[1])
            time.sleep(1)
        else:
            print("Could not read ADC.")
            exit(1)

    serial_end()
    sys.exit(0)
