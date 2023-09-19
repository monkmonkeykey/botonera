import time
from rpi_ws281x import Adafruit_NeoPixel, Color

# Configuración de la tira de LED NeoPixel
LED_COUNT = 16  # Número de LEDs en tu tira
LED_PIN = 18    # El pin GPIO al que está conectada la tira de LED
LED_FREQ_HZ = 800000
LED_DMA = 10
LED_BRIGHTNESS = 255
LED_INVERT = False

# Inicializa la biblioteca NeoPixel
strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS)

# Inicializa la tira de LED (debes llamar a esto una vez antes de usar la tira)
strip.begin()

try:
    while True:
        # Cambia el color de todos los LEDs a rojo
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(255, 0, 0))
            strip.show()
            time.sleep(0.1)

        # Espera un segundo
        time.sleep(1)

        # Cambia el color de todos los LEDs a verde
        for i in range(LED_COUNT):
            strip.setPixelColor(i, Color(0, 255, 0))
            strip.show()
            time.sleep(0.1)

        # Espera un segundo
        time.sleep(1)

except KeyboardInterrupt:
    # Manejo de interrupción por teclado (Ctrl+C) para salir del bucle
    pass

# Apaga la tira de LED cuando el programa termina
strip.clear()
strip.show()
