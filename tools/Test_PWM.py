#
# Title: USB IO Expander PWM Test program.
#
# Author: Rob Jansen, Copyright (c) 2024..2024, all rights reserved.
#
# Description: Python script for testing the USB IO Expander PWM functionality.
#
#
import sys
import time
from usb_io_expander import default_comport, get_default_comport, serial_init, serial_end, pwm_init, pwm_enable, \
                            pwm_disable, pwm_frequency, pwm_duty_cyle

minimum_frequency = 750
maximum_frequeny = 45000

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

    if pwm_init(1):
        print("PWM 1 initialized")
    else:
        print("Could not initialize PWM 1")
        sys.exit(1)

    if pwm_init(2):
        print("PWM 2 initialized")
    else:
        print("Could not initialize PWM 2")
        sys.exit(1)

    if pwm_enable(1):
        print("PWM 1 enabled.")
    else:
        print("Could not enable PWM 1")
        sys.exit(1)

    if pwm_enable(2):
        print("PWM 2 enabled.")
    else:
        print("Could not enable PWM 2")
        sys.exit(1)

    print("Changing PWM frequency and duty cycle press <ctrl-c> to stop .")
    frequency = minimum_frequency
    while True:
        # Frequency is the same for both PWM channels. Only duty cycle differs.
        if pwm_frequency(frequency):
            print("Frequency: ", frequency)
            for duty_cycle in range(101):  # 0..100

                # Duty cycle goes up for channel 1.
                if pwm_duty_cyle(1, duty_cycle):
                    print(".", end='')
                else:
                    print("Could not set duty cycle for channel 1:", duty_cycle)
                    sys.exit(1)

                # Duty cycle goes down for channel 2.
                if pwm_duty_cyle(2, 100 - duty_cycle):
                    print(".", end='')
                else:
                    print("Could not set duty cycle for channel 2:", duty_cycle)
                    sys.exit(1)

                time.sleep(0.1)
            print("One cycle done.")
            frequency = frequency + 250
            if frequency > maximum_frequeny:
                frequency = minimum_frequency
        else:
            print("Could not set duty frequency:", frequency)
            sys.exit(1)

    serial_end()
    sys.exit(0)
