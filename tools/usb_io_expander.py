#
# Title: USB IO Expander supporting functions.
#
# Author: Rob Jansen, Copyright (c) 2023..2024, all rights reserved.
#
# Description: Python script easy accessing functions of the USB IO Expander.
#              For serial communication the settings are:
#              -) 115.000 baud, 8 bits, no parity, 1 stopbit, rts/cts enabled,
#                 serial timeout is set to 30 seconds.
#                 Default port is com3 but an be overruled by the user.
#


import sys
import serial

# Default settings.
default_baudrate = 115200
default_comport = "com3"
ser = serial.Serial()

# Set the default comport. Default is com3 under Windows.
def get_default_comport():
    if sys.platform.startswith('linux'):
        return "/dev/ttyACM0"
    elif sys.platform.startswith('darwin'):
        return "/dev/ttyACM0"
    else:
        return default_comport

# Initialize and open the serial port. Returns True when successful.
def serial_init(which_port):
    ser.port = which_port
    ser.baudrate = default_baudrate
    ser.bytesize = 8
    ser.parity = 'N'
    ser.stopbits = 1
    ser.timeout = 3  # 3 seconds wait timeout for reading response. Programming may take some time.
    ser.xonxoff = 0
    ser.rtscts = 1  # RTS/CTS must be enabled!
    try:
        ser.open()
        if ser.is_open:
            port_is_open = True
        else:
            port_is_open = False
    except:
        port_is_open = False
    if port_is_open:
        return True
    else:
        print("Could not open serial port:",which_port)
        return False

# Close the serial port.
def serial_end():
    try:
        ser.close()
    except:
        pass

# Returns the decimal value of an hexadecimal ASCII character.
def convert_hex_ascii_to_decimal(value):
    if (value >= 48) and (value <= 57):
        return value - 48 # 0..9
    else:
        return value - 55 # A..F

# Returns True if the end of line is detected.
def is_end_of_line(character):
    if (character == 0x0A) or (character == 0x0D):
        return True
    else:
        return False

# Checks if the response is "0" (OK), if so TRUE is returned.
def response_ok():
    # Response format is: b'0\r\n'. 0 for OK or any other for not OK.
    response = ser.readline()
    if response == b'0\r\n':
        return True
    else:
        return False

# Read an answer containing hex data and return the data in a list and TRUE when OK.
def get_hex_data():
    hex_data = []
    data_ok = True
    # Now read the data.
    data_read = ser.readline()
    # The first character of a response always starts with '?' (63).
    if data_read[0] == 63:
        index = 1 # Skip the first character ('?').
        stop = False
        # Continue until all characters processed or in case of end of line reached.
        while (index < (len(data_read) - 1)) and not stop:
            data = data_read[index]
            if is_end_of_line(data):
                stop = True
            else:
                hex_high = convert_hex_ascii_to_decimal(data)
                index = index + 1
                data = data_read[index]
                if is_end_of_line(data):
                    stop = True
                else:
                    hex_low = convert_hex_ascii_to_decimal(data)
                    index = index + 1
                    hex_byte = (16 * hex_high) + hex_low
                    hex_data.append(hex_byte)
    else:
        data_ok = False # Answer did not start with '?'
    return data_ok, hex_data

# Set the given pin (0..7) to the given direction (0 = output, 1 = input)
def pin_bit_direction(pin, direction):
    serialcommand = '!PID{:02X}{:02X}\r\n'.format(pin, direction)
    ser.write(serialcommand.encode())
    return response_ok()

# Set the given pin (0, 1, 2, 3 or 6) to the given mode (0 = digital, 1 = analog)
def pin_bit_mode(pin, mode):
    serialcommand = '!PIM{:02X}{:02X}\r\n'.format(pin, mode)
    ser.write(serialcommand.encode())
    return response_ok()

# Set the given pin (6 or 7) to the given pull-up (0 = disabled, 1 = enabled)
def pin_bit_pull_up(pin, pull_up):
    serialcommand = '!PIP{:02X}{:02X}\r\n'.format(pin, pull_up)
    ser.write(serialcommand.encode())
    return response_ok()

# Set the given pin (0..7) to the given value (0 = low, 1 = high)
def pin_bit_write(pin, value):
    serialcommand = '!PIW{:02X}{:02X}\r\n'.format(pin, value)
    ser.write(serialcommand.encode())
    return response_ok()

# Set the all pins (0..7) of the given bits in the given direction (0 = output, 1 = input)
def pin_byte_direction(direction):
    serialcommand = '!PYD{:02X}\r\n'.format(direction)
    ser.write(serialcommand.encode())
    return response_ok()

# Set the all pins (0..7) to the given bits in the parameter value (0 = low, 1 = high)
def pin_byte_write(value):
    serialcommand = '!PYW{:02X} \r\n'.format(value)
    ser.write(serialcommand.encode())
    return response_ok()

# Return the status of the given pin (0 = low, 1 = high).
def pin_bit_read(pin):
    serialcommand = '!PIR{:02X}\r\n'.format(pin)
    ser.write(serialcommand.encode())
    pin_status = []  # Dummy in case of no response.
    if response_ok():
        # Get the returned data.
        return get_hex_data()
    else:
        return False, pin_status

# Return the status of the given port.
def pin_byte_read():
    serialcommand = '!PYR\r\n'
    ser.write(serialcommand.encode())
    port_status = [] # Dummy in case of no response.
    if response_ok():
        # Get the returned data.
        return get_hex_data()
    else:
        return False, port_status

# Initialize the IIC interface with the given bus speed (1 = 100kHz, 4 = 400 kHz).
# Returns TRUE when successful.
def iic_init(bus_speed):
    serialcommand = '!IICI{:02X}\r\n'.format(bus_speed)
    ser.write(serialcommand.encode())
    return response_ok()

# Write the given IIC data to an IIC device.
# Returns TRUE when successful.
def iic_write(slave_address, iic_write_data=[]):
    serialcommand = '!IICW{:02X}'.format(slave_address)
    ser.write(serialcommand.encode())
    # Now send all data to write in hexadecimal notation.
    for data in iic_write_data:
        hex_byte = ("{:02X}".format(data))
        ser.write(hex_byte.encode())
    serialcommand = '\r\n'
    ser.write(serialcommand.encode())
    return response_ok()

# Read IIC data from an IIC device.
# Returns TRUE and the data read when successful.
def iic_read(slave_address, nr_of_bytes):
    serialcommand = '!IICR{:02X}{:02X}\r\n'.format(slave_address, nr_of_bytes)
    ser.write(serialcommand.encode())
    iic_read_data = [] # Dummy in case of no response.
    if response_ok():
        # Get the returned data.
        return get_hex_data()
    else:
        return False, iic_read_data

# Initialize the DAC wit the given channel (1 or 2).
# Returns TRUE when successful.
def dac_init(channel):
    serialcommand = '!DACI{:02X}\r\n'.format(channel)
    ser.write(serialcommand.encode())
    return response_ok()

# Enable the DAC.
# Returns TRUE when successful.
def dac_enable():
    ser.write(b'!DACE\r\n')
    return response_ok()

# Disable the DAC.
# Returns TRUE when successful.
def dac_disable():
    ser.write(b'!DACD\r\n')
    return response_ok()

# Set the DAC to the given value (0..31).
# Returns TRUE when successful.
def dac_write(value):
    serialcommand = '!DACW{:02X}\r\n'.format(value)
    ser.write(serialcommand.encode())
    return response_ok()

# Initialize the SPI interface with the given mode and speed.
# Returns TRUE when successful.
def spi_init(mode, speed):
    serialcommand = '!SPII{:02X}{:02X}\r\n'.format(mode, speed)
    ser.write(serialcommand.encode())
    return response_ok()

# Write the given SPI data. Returns TRUE when successful.
def spi_write(spi_write_data=[]):
    serialcommand = '!SPIW'
    ser.write(serialcommand.encode())
    # Now send all data to write in hexadecimal notation.
    for data in spi_write_data:
        hex_byte = ("{:02X}".format(data))
        ser.write(hex_byte.encode())
    serialcommand = '\r\n'
    ser.write(serialcommand.encode())
    return response_ok()

# Write the SPI data for the given number of bytes.
# Returns TRUE when successful.
def spi_read(nr_of_bytes):
    serialcommand = '!SPIR{:02X}\r\n'.format(nr_of_bytes)
    ser.write(serialcommand.encode())
    spi_read_data = []  # Dummy in case of no response.
    if response_ok():
        # Get the returned data.
        return get_hex_data()
    else:
        return False, spi_read_data
    return response_ok()

# Initialize the ADC with the given channel (3, 4, 5, 6, or 7).
# Returns TRUE when successful.
def adc_init(channel):
    serialcommand = '!ADCI{:02X}\r\n'.format(channel)
    ser.write(serialcommand.encode())
    return response_ok()

# Enable the adc.
# Returns TRUE when successful.
def adc_enable():
    ser.write(b'!ADCE\r\n')
    return response_ok()

# Disable the ADC.
# Returns TRUE when successful.
def adc_disable():
    ser.write(b'!ADCD\r\n')
    return response_ok()

# Select an ADC channel. ADC must be initialized.
def adc_channel(channel):
    serialcommand = '!ADCC{:02X}\r\n'.format(channel)
    ser.write(serialcommand.encode())
    return response_ok()

# Get the ADC value.
# Returns TRUE when successful.
def adc_read():
    ser.write(b'!ADCR\r\n')
    adc_data = []  # Dummy in case of no response.
    if response_ok():
        # Get the returned data.
        return get_hex_data()
    else:
        return False, adc_data

# Initialize the PWM wit the given channel (1 or 2).
# Returns TRUE when successful.
def pwm_init(channel):
    serialcommand = '!PWMI{:02X}\r\n'.format(channel)
    ser.write(serialcommand.encode())
    return response_ok()

# Enable the given PWM channel.
# Returns TRUE when successful.
def pwm_enable(channel):
    serialcommand = '!PWME{:02X}\r\n'.format(channel)
    ser.write(serialcommand.encode())
    return response_ok()

# Disable the given PWM channel.
# Returns TRUE when successful.
def pwm_disable(channel):
    serialcommand = '!PWMD{:02X}\r\n'.format(channel)
    ser.write(serialcommand.encode())
    return response_ok()

# Set the PWM frequency
# Returns TRUE when successful.
def pwm_frequency(frequency):
    serialcommand = '!PWMF{:04X}\r\n'.format(frequency)
    ser.write(serialcommand.encode())
    return response_ok()

# Set the PWM duty cycle for the given channel
# Returns TRUE when successful.
def pwm_duty_cyle(channel, duty_cycle):
    serialcommand = '!PWMC{:02X}{:02X}\r\n'.format(channel, duty_cycle)
    ser.write(serialcommand.encode())
    return response_ok()
