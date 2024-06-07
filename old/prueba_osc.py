from pythonosc import dispatcher, osc_server
import board
import busio
import digitalio

import adafruit_tlc5947

SCK = board.SCK
MOSI = board.MOSI
LATCH = digitalio.DigitalInOut(board.D27)

# Initialize SPI bus.
spi = busio.SPI(clock=SCK, MOSI=MOSI)

# Initialize TLC5947
tlc5947 = adafruit_tlc5947.TLC5947(spi, LATCH)

led1 = tlc5947.create_pwm_out(0)
led2 = tlc5947.create_pwm_out(1)
led3 = tlc5947.create_pwm_out(2)

# Define funciones para manejar los mensajes OSC
def manejar_mensaje_1(address, *args):
    if address == "/ch1":
        led2.duty_cycle = int(args[0])
        tlc5947.write()

def manejar_mensaje_2(address, *args):
    print("No pasa nada oiga 2")

def manejar_mensaje_3(address, *args):
    print("No pasa nada oiga 3")

# Crea un despachador de mensajes OSC
dispatcher = dispatcher.Dispatcher()

# Asocia las direcciones OSC con las funciones de manejo
dispatcher.map("/ch1", manejar_mensaje_1)
dispatcher.map("/ch2", manejar_mensaje_2)
dispatcher.map("/ch3", manejar_mensaje_3)

# Configura y corre el servidor OSC en el hilo principal
ip_escucha = "0.0.0.0"  # Escucha en todas las interfaces de red
puerto_escucha = 8000   # Puerto en el que escucha el servidor

servidor = osc_server.ThreadingOSCUDPServer((ip_escucha, puerto_escucha), dispatcher)
print(f"Escuchando en {ip_escucha}:{puerto_escucha}")

# Iniciar el servidor en el hilo principal
servidor.serve_forever()
