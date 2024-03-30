# USB_IO_Expander
Controlling various hardware devices via the USB port.

# Introduction
The USB I/O Expander acts as a COM port and is controlled using commands and data in ASCII format. All data is transmitted as hexadecimal bytes except for the response that is returned by the USB I/O Expander after executing a command. A command is executed after detecting a carriage return or a line feed.

This device makes it possible to control various hardware devices providing the following features:
- Reading and writing eight I/O pins
- IIC interface for controlling IIC devices
- SPI interface for controlling SPI devices
- Digital to Analog Conversion (DAC) with 2 selectable analog outputs
- Analog to Digital Conversion (ADC) with 4 selectable analog inputs
- Two channel Pulse Width Modulation (PWM) signal generator

It uses a PIC16F1455 Microcontroller programmed using the JAL programming language.

# Hardware
Various hardware set-ups are shown that where used for testing the device.

# Documentation
A detailed manual is available describing how to operate the device. Also a powerpoint presentation is available that was created to demonstrate the device.

# Tools
A Python library is available including various Python script that demonstrate the functionality of the device.

