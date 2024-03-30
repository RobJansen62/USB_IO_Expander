#
# Title: USB IO Expander SPI Test program.
#
# Author: Rob Jansen, Copyright (c) 2024..2024, all rights reserved.
#
# Description: Python script for testing the USB IO Expander SPI functionality.
#              This program sets the output pins and read the latch register of the MCP23S08.
#
# Note: This SPI device has a slave address for reading and writing.
#
import sys
import time
from usb_io_expander import default_comport, get_default_comport, serial_init, serial_end, spi_init, \
                            spi_write, spi_read, set_pin_bit_direction, set_pin_bit_mode, pin_bit_write

spi_address_write = 0x40  # A0, A1 connected to GND.
spi_address_read = 0x41  # A0, A1 connected to GND.
spi_select = 3  # Pin 3 is pin C3 used for device select

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

    # Select SPI mode 00 and clock OSC/4 Note, does not work for higher lower speeds!
    if spi_init(0, 2):
        print("SPI initialized")
    else:
        print("Could not initialize SPI interface")
        sys.exit(1)

    # Device select is connected to pin 7 which is C3 which is pin 3. Set to digital output.
    if set_pin_bit_direction(spi_select, 0):
        print("Device select pin set to output")
    else:
        print("Could not set pin SS to output")
        sys.exit(1)

    # Device select must be a digital pin.
    if set_pin_bit_mode(spi_select, 0):
        print("Device select set to digital pin.")
    else:
        print("Could not set pin device select to digital pin.")
        sys.exit(1)

    pin_bit_write(spi_select, 0)  # Select device.
    # IODIR register, all pins Output.
    if spi_write([spi_address_write, 0x00, 0x00]):
        print("Port set to output")
    else:
        print("Could not set port to output.")
        sys.exit(1)
    pin_bit_write(spi_select, 1)  # Deselect device.

    pin_bit_write(spi_select, 0)  # Select device.
    # Port register, all pins HIGH.
    if spi_write([spi_address_write, 0x09, 0xFF]):
        print("All port pins set to HIGH.")
    else:
        print("Could not set all port pins to HIGH.")
        sys.exit(1)
    pin_bit_write(spi_select, 1)  # Deselect device.
    time.sleep(1)

    pin_bit_write(spi_select, 0)  # Select device.
    # Port register, all pins LOW.
    if spi_write([spi_address_write, 0x09, 0x00]):
        print("All port pins set to LOW.")
    else:
        print("Could not set all port pins to LOW.")
        sys.exit(1)
    pin_bit_write(spi_select, 1)  # Deselect device.
    time.sleep(1)

    print("Running tests, press <ctrl-c> to stop. ")
    # Set individual pins HIGH and LOW and read the latch register.
    while True:
        data = 0x01
        for x in range(8):
            pin_bit_write(spi_select, 0)  # Select device.
            if not spi_write([spi_address_write, 0x09, data]):  # Port register.
                print("Could not set port register.")
                sys.exit(1)
            pin_bit_write(spi_select, 1)  # Deselect device.
            data = data << 1

            # Read the latch.
            pin_bit_write(spi_select, 0)  # Select device.
            if not spi_write([spi_address_read, 0x0A]):  # Select Latch register for reading.
                print("Could not set latch register.")
                sys.exit(1)
            command_ok, spi_data = spi_read(1)  # And now read one byte (device select is still active).
            if command_ok:
                print("Latch data is: ", spi_data[0])
            pin_bit_write(spi_select, 1)  # Deselect device.
            time.sleep(0.5)

        data = 0x80
        for x in range(8):
            pin_bit_write(spi_select, 0)  # Select device.
            if not spi_write([spi_address_write, 0x09, data]):  # Port register.
                print("Could not set port register.")
                sys.exit(1)
            data = data >> 1
            pin_bit_write(spi_select, 1)  # Deselect device.

            # Read the latch.
            pin_bit_write(spi_select, 0)  # Select device.
            if not spi_write([spi_address_read, 0x0A]):  # Select Latch register for reading.
                print("Could not set latch register.")
                sys.exit(1)
            command_ok, spi_data = spi_read(1)  # And now read one byte (device select is still active).
            if command_ok:
                print("Latch data is: ", spi_data[0])
            pin_bit_write(spi_select, 1)  # Deselect device.
            time.sleep(0.5)

    serial_end()
    sys.exit(0)
