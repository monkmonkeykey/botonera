import time
import board
import neopixel

numPixels = 8

# Definir el objeto NeoPixel
pixels = neopixel.NeoPixel(board.D18, numPixels, brightness=1.0, auto_write=False)

def set_pixel_color(pixel, color):
    # Guardar el brillo actual
    current_brightness = pixels.brightness

    # Establecer el color del píxel sin cambiar el brillo global
    pixels.brightness = 1.0  # Establecer temporalmente el brillo a 1.0 para asegurar un color completo
    pixels[pixel] = color
    pixels.show()

    # Restaurar el brillo original
    pixels.brightness = current_brightness

while True:
    # Definir un color (por ejemplo, rojo)
    color = (255, 0, 0)

    # Establecer el color del píxel 0
    set_pixel_color(0, color)

    # Establecer el color del píxel 1 sin afectar el brillo global
    set_pixel_color(1, (0, 255, 0))  # Por ejemplo, verde

    # Variar el brillo del color
    for b in range(256):
        pixels.brightness = b / 255.0
        pixels.show()
        time.sleep(0.01)

    time.sleep(1)  # Esperar un segundo antes de reiniciar el ciclo
