import board
import neopixel
import time

# Configuración de la tira de LED NeoPixel
pixel_pin = board.D13  # El pin GPIO al que está conectada la tira de LED
num_pixels = 8  # Número de LEDs en tu tira

# Inicializa la tira de LED
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.2, auto_write=False)

try:
    while True:
        # Cambia el color de todos los LEDs a rojo
        for i in range(num_pixels):
            pixels[i] = (255, 0, 0)  # Rojo
            pixels.show()
            time.sleep(0.1)

        # Espera un segundo
        time.sleep(1)

        # Cambia el color de todos los LEDs a verde
        for i in range(num_pixels):
            pixels[i] = (0, 255, 0)  # Verde
            pixels.show()
            time.sleep(0.1)

        # Espera un segundo
        time.sleep(1)

except KeyboardInterrupt:
    # Manejo de interrupción por teclado (Ctrl+C) para salir del bucle
    pass

finally:
    # Apaga la tira de LED cuando el programa termina
    pixels.fill((0, 0, 0))
    pixels.show()
