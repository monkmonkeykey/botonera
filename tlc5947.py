# SPDX-FileCopyrightText: 2018 Tony DiCola for Adafruit Industries
# SPDX-License-Identifier: MIT

# Simple demo of controlling the TLC5947 12-bit 24-channel PWM controller.
# Will update channel values to different PWM duty cycles.
# Author: Tony DiCola

import board
import busio
import digitalio

import adafruit_tlc5947

# Define pins connected to the TLC5947
SCK = board.SCK
MOSI = board.MOSI
LATCH = digitalio.DigitalInOut(board.D27)

# Initialize SPI bus.
spi = busio.SPI(clock=SCK, MOSI=MOSI)

# Initialize TLC5947
tlc5947 = adafruit_tlc5947.TLC5947(spi, LATCH)
# You can optionally disable auto_write which allows you to control when
# channel state is written to the chip.  Normally auto_write is true and
# will automatically write out changes as soon as they happen to a channel, but
# if you need more control or atomic updates of multiple channels then disable
# and manually call write as shown below.
# tlc5947 = adafruit_tlc5947.TLC5947(spi, LATCH, auto_write=False)

# There are two ways to channel channel PWM values.  The first is by getting
# a PWMOut object that acts like the built-in PWMOut and can be used anywhere
# it is used in your code.  Change the duty_cycle property to a 16-bit value
# (note this is NOT the 12-bit value supported by the chip natively) and the
# PWM channel will be updated.

# With an RGB LED hooked up to pins 0, 1, and 2, cycle the red, green, and
# blue pins up and down:

red = tlc5947.create_pwm_out(0)
green = tlc5947.create_pwm_out(1)
blue = tlc5947.create_pwm_out(2)

red_brightness = 32766  # 50% de brillo
green_brightness = 16383  # 25% de brillo
blue_brightness = 49151  # 75% de brillo
intensity_level = 0
while True:
    # Variable para controlar el nivel de intensidad


# Incremento de 0 a 10
    for i in range(0, 49151 ,100):
        intensity_level = i
        green.duty_cycle = intensity_level
        print("Nivel de intensidad:", intensity_level)

    # Decremento de 10 a 0
    for i in range(49150, -1, -100):
        intensity_level = i
        green.duty_cycle = intensity_level
        print("Nivel de intensidad:", intensity_level)

# Note if auto_write was disabled you need to call write on the parent to
# make sure the value is written (this is not common, if disabling auto_write
# you probably want to use the direct 12-bit raw access instead shown below).
#            tlc5947.write()

# The other way to read and write channels is directly with each channel 12-bit
# value and an item accessor syntax.  Index into the TLC5947 with the channel
# number (0-23) and get or set its 12-bit value (0-4095).
# For example set channel 1 to 50% duty cycle.
# tlc5947[1] = 2048
# Or set channel 23 (first channel from the end) to 2/3 duty cycle.
# tlc5947[-1] = 2730
# Again be sure to call write if you disabled auto_write.
# tlc5947.write()
