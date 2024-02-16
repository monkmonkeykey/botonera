import time
import board
import neopixel

# Definir el número de Neopixels en el módulo
num_pixels = 8

# Definir el pin al que está conectado el módulo
pin = board.D18

# Crear el objeto NeoPixel para el módulo completo
pixels = neopixel.NeoPixel(pin, num_pixels, brightness=1.0, auto_write=False)

# Bucle principal
while True:
    # Definir colores para cada LED de forma independiente
    for i in range(num_pixels):
        color = ((i * 30) % 256, (i * 50) % 256, (i * 70) % 256)
        pixels[i] = color
    
    # Variar el brillo de la cadena completa
    for b in range(256):
        pixels.brightness = int(b) / 255.0
        pixels.show()
        time.sleep(0.01)

    time.sleep(1)  # Esperar un segundo antes de reiniciar el ciclo
