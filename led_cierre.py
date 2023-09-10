import RPi.GPIO as GPIO
import busio
import digitalio

import adafruit_tlc5947

# Configurar los números de pin GPIO
SCK_PIN = 11  # Cambia estos valores según tus conexiones
MOSI_PIN = 10  # Cambia estos valores según tus conexiones
LATCH_PIN = 27  # Cambia estos valores según tus conexiones

# Configurar pines GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(SCK_PIN, GPIO.OUT)
GPIO.setup(MOSI_PIN, GPIO.OUT)
GPIO.setup(LATCH_PIN, GPIO.OUT)

# Inicializar la interfaz SPI
spi = busio.SPI(clock=SCK_PIN, MOSI=MOSI_PIN)

# Inicializar TLC5947
tlc5947 = adafruit_tlc5947.TLC5947(spi, digitalio.DigitalInOut(LATCH_PIN))

# Crear objetos PWMOut para cada canal (LED)
red = tlc5947.create_pwm_out(0)
green = tlc5947.create_pwm_out(1)
blue = tlc5947.create_pwm_out(2)

# Definir el nivel de iluminación deseado para cada LED (0-65535)
nivel_iluminacion_red = 32767  # 50% de brillo (ajusta según tus necesidades)
nivel_iluminacion_green = 32767
nivel_iluminacion_blue = 32767

# Establecer el nivel de iluminación de los LEDs
red.duty_cycle = nivel_iluminacion_red
green.duty_cycle = nivel_iluminacion_green
blue.duty_cycle = nivel_iluminacion_blue

# El código continuará ejecutándose sin cambios en el nivel de brillo
while True:
    pass
