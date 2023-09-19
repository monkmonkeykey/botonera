import board
import neopixel
pixels = neopixel.NeoPixel(board.D13, 8)
pixels[0] = (255, 0, 0)
pixels[1] = (0, 255, 0)