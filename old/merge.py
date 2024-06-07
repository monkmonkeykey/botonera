# -*- coding: utf-8 -*-
import time
import threading
from pythonosc.udp_client import SimpleUDPClient
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
from gpiozero import Button
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008
import board
import busio
import digitalio
import adafruit_tlc5947

# Configuración del SPI para el MCP3008
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Configura el cliente OSC
client = SimpleUDPClient("192.168.1.38", 10000)  # Cambia la dirección y el puerto según tus necesidades

# Configura los pines GPIO de los botones
BOTONES = [13, 26, 27, 21, 20, 16]
buttons = [Button(pin, pull_up=True) for pin in BOTONES]

# Variables para el seguimiento del estado anterior de los botones
estado_anterior = [True] * len(BOTONES)

# Inicialización de SPI y TLC5947
SCK = board.SCK
MOSI = board.MOSI
LATCH = digitalio.DigitalInOut(board.D5)  # Cambio de pin para evitar conflicto con GPIO 21
spi = busio.SPI(clock=SCK, MOSI=MOSI)
tlc5947 = adafruit_tlc5947.TLC5947(spi, LATCH)

# Valores máximos y mínimos de PWM
MAX_PWM = 30000
MIN_PWM = 0
NUM_LEDS = 10

# Crear PWMOut objects para cada LED
leds = [tlc5947.create_pwm_out(i) for i in range(NUM_LEDS)]

# Variable de volumen inicial
volume = 0.0
target_volume = 0.0

# Define una función para enviar un mensaje OSC
def enviar_mensaje_osc(address, *args):
    client.send_message(address, args)

# Define una función para manejar los mensajes OSC entrantes
def handle_volume(address, *args):
    global target_volume
    target_volume = max(0.0, min(1.0, args[0]))

# Crear un dispatcher para mapear direcciones OSC a funciones de callback
dispatcher = Dispatcher()
dispatcher.map("/volume", handle_volume)

# Crear un servidor OSC para recibir mensajes
server = ThreadingOSCUDPServer(("0.0.0.0", 9500), dispatcher)  # Ajusta IP y puerto según sea necesario

# Función para actualizar los LEDs según el volumen objetivo
def update_leds(target_volume):
    if target_volume == 0.0:
        for led in leds:
            led.duty_cycle = MIN_PWM
    else:
        num_leds_to_light = min(int(target_volume * NUM_LEDS), NUM_LEDS)
        for i in range(num_leds_to_light):
            leds[i].duty_cycle = MAX_PWM
        for i in range(num_leds_to_light, NUM_LEDS):
            led.duty_cycle = MIN_PWM
    tlc5947.write()

# Función para ejecutar el servidor OSC en un hilo separado
def run_server():
    server.serve_forever()

# Iniciar el servidor OSC en un hilo separado
server_thread = threading.Thread(target=run_server)
server_thread.start()

# Bucle principal para leer el estado de los botones, enviar mensajes OSC y actualizar los LEDs
try:
    while True:
        for i, button in enumerate(buttons):
            estado_boton = button.is_pressed
            if estado_boton != estado_anterior[i]:
                direccion_osc = f"/boton{i + 1}"
                estado_anterior[i] = estado_boton
                enviar_mensaje_osc(direccion_osc, int(estado_boton))

        # Leer y enviar los valores de los potenciómetros
        valor_pot1 = int(mcp.read_adc(0))
        valor_pot2 = int(mcp.read_adc(1))
        enviar_mensaje_osc("/pot1", valor_pot1)
        enviar_mensaje_osc("/pot2", valor_pot2)

        # Actualizar los LEDs según el volumen objetivo
        update_leds(target_volume)

        time.sleep(0.01)  # Pequeña pausa para evitar lecturas repetidas

except KeyboardInterrupt:
    # Apagar el servidor OSC y unirse al hilo del servidor
    server.shutdown()
    server_thread.join()

    # Limpiar los recursos GPIO al salir
    for button in buttons:
        button.close()
