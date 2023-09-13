import threading
from pythonosc import dispatcher, osc_server
import board
import busio
import digitalio
import adafruit_tlc5947
import time

# Define los pines conectados al TLC5947
SCK = board.SCK
MOSI = board.MOSI
LATCH = digitalio.DigitalInOut(board.D27)

# Inicializa el bus SPI.
spi = busio.SPI(clock=SCK, MOSI=MOSI)

# Inicializa el controlador TLC5947
tlc5947 = adafruit_tlc5947.TLC5947(spi, LATCH)
# Crea objetos PWMOut para los LEDs
led_uno = tlc5947.create_pwm_out(1)
led_dos = tlc5947.create_pwm_out(2)
led_tres = tlc5947.create_pwm_out(3)

# Función para controlar los LEDs
def controlar_leds():
    while True:
        # Tu lógica para controlar los LEDs aquí
        # Por ejemplo, puedes actualizar los valores de duty_cycle de los LEDs aquí
        time.sleep(0.01)  # Asegúrate de agregar un pequeño retraso para evitar que el hilo consuma demasiada CPU

# Función para manejar los mensajes OSC
def manejar_led(address, *args):
    if address == "/ch1":
        pwm_value_uno = int(mapear_valor(int(args[0]), 0, 100, 0, 65535))
        led_uno.duty_cycle = pwm_value_uno
    elif address == "/ch2":
        pwm_value_dos = int(mapear_valor(int(args[0]), 0, 100, 0, 65535))
        led_dos.duty_cycle = pwm_value_dos
    elif address == "/ch3":
        pwm_value_tres = int(mapear_valor(int(args[0]), 0, 100, 0, 65535))
        led_tres.duty_cycle = pwm_value_tres

# Función para mapear valores
def mapear_valor(valor, valor_minimo1, valor_maximo1, valor_minimo2, valor_maximo2):
    valor_mapeado = (valor - valor_minimo1) * (valor_maximo2 - valor_minimo2) / (valor_maximo1 - valor_minimo1) + valor_minimo2
    return valor_mapeado

# Crea un despachador de mensajes OSC
dispatcher = dispatcher.Dispatcher()

# Mapea las direcciones OSC a la función de manejo
direcciones_osc = ["/ch1", "/ch2", "/ch3"]
for direccion in direcciones_osc:
    dispatcher.map(direccion, manejar_led)

# Configura y corre el servidor OSC en un hilo separado
ip_escucha = "0.0.0.0"  # Escucha en todas las interfaces de red
puerto_escucha = 8000   # Puerto en el que escucha el servidor

servidor = osc_server.ThreadingOSCUDPServer((ip_escucha, puerto_escucha), dispatcher)
print(f"Escuchando en {ip_escucha}:{puerto_escucha}")

# Inicia el servidor en un hilo separado
servidor_thread = threading.Thread(target=servidor.serve_forever)
servidor_thread.start()

# Inicia el hilo para controlar los LEDs
leds_thread = threading.Thread(target=controlar_leds)
leds_thread.start()
