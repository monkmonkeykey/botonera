import time
import board
import neopixel

numPixels = 8

# Definir el objeto NeoPixel
pixels = neopixel.NeoPixel(board.D18, numPixels, brightness=1.0, auto_write=False)

def set_pixel_color(pixel, color, brightness=1.0):
    # Establecer el color del píxel con el brillo proporcionado
    pixels[pixel] = (int(color[0] * brightness), int(color[1] * brightness), int(color[2] * brightness))
    pixels.show()

while True:
    # Definir un color (por ejemplo, rojo)
    color = (255, 0, 0)

    # Establecer el color y brillo del píxel 0
    set_pixel_color(0, color, brightness=1.0)

    # Establecer el color y brillo del píxel 1
    set_pixel_color(1, (0, 255, 0), brightness=0.5)  # Por ejemplo, verde con la mitad del brillo

    # Variar el brillo de cada píxel independientemente
    for pixel in range(numPixels):
        set_pixel_color(pixel, color, brightness=(pixel + 1) / numPixels)
        pixels.show()
        time.sleep(0.1)

    time.sleep(1)  # Esperar un segundo antes de reiniciar el ciclo
