import board
import busio
import digitalio
import adafruit_tlc5947

# Define los pines conectados al TLC5947
SCK = board.SCK
MOSI = board.MOSI
LATCH = digitalio.DigitalInOut(board.D5)

# Inicializa el bus SPI.
spi = busio.SPI(clock=SCK, MOSI=MOSI)

# Inicializa el controlador TLC5947
tlc5947 = adafruit_tlc5947.TLC5947(spi, LATCH)

# Crea un objeto PWMOut para el LED (en este ejemplo, el LED está conectado al canal 0)
led = tlc5947.create_pwm_out(0)

# Define el valor de ciclo de trabajo PWM deseado (0 a 65535, donde 0 es apagado y 65535 es encendido)
pwm_value = 32767  # Ejemplo: establece el LED al 50% de brillo

# Establece el valor de ciclo de trabajo PWM para el LED
led.duty_cycle = pwm_value

# Llama al método write para aplicar el cambio
tlc5947.write()
