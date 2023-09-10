import board
import busio
import adafruit_tlc5947

# Inicializa el bus SPI
spi = busio.SPI(board.SCK, MOSI=board.MOSI)

# Inicializa el controlador TLC5947
num_tlc5947 = 1  # Un solo TLC5947
num_leds = num_tlc5947 * 24  # Cada TLC5947 tiene 24 salidas
tlc5947 = adafruit_tlc5947.TLC5947(spi, num_leds)

# Define una función para establecer el estado de un LED específico
def set_led(led_index, value):
    if led_index < num_leds:
        tlc5947[led_index] = value
        tlc5947.write()

# Define una función para controlar tres LEDs
def controlar_tres_leds(intensidad_led1, intensidad_led2, intensidad_led3):
    # Asigna intensidades a los LEDs
    set_led(0, intensidad_led1)
    set_led(1, intensidad_led2)
    set_led(2, intensidad_led3)

    # Actualiza el estado de los LEDs
    tlc5947.write()

# Uso de la función para encender los LEDs
controlar_tres_leds(32768, 49152, 16384)  # Intensidades en función de tus preferencias

# Espera unos segundos
import time
time.sleep(2)

# Apagar los LEDs
controlar_tres_leds(0, 0, 0)
