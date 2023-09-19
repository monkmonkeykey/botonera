import board
import neopixel

pixel = neopixel.NeoPixel(board.D13, 1, pixel_order=neopixel.RGBW)
pixel[0] = (30, 0, 20, 10)