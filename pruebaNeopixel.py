import time
import board
import neopixel
numPixels = 8
# Definir el objeto NeoPixel
pixels = neopixel.NeoPixel(board.D18, numPixels, brightness=1.0, auto_write=False)

def set_pixel_color(pixel, color):
    pixels[pixel] = color
    pixels.show()

while True:
    # Definir un color (por ejemplo, rojo)
    color = (255, 0, 0)

    # Establecer el color del píxel 0
    set_pixel_color(0, color)

    # Variar el brillo del color
    for b in range(256):
        pixels.brightness = b / 255.0
        pixels.show()
        time.sleep(0.01)

    time.sleep(1)  # Esperar un segundo antes de reiniciar el ciclo
