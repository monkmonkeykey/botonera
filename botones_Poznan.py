# -*- coding: utf-8 -*-
from pythonosc.udp_client import SimpleUDPClient
from gpiozero import Button
import time
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Hardware SPI configuration:
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Configura el cliente OSC
client = SimpleUDPClient("192.168.1.38", 10000)  # Cambia la dirección y el puerto según tus necesidades

# Configura los pines GPIO de los botones
BOTONES = [13,26,27,21,4,19]

buttons = [Button(pin, pull_up=True) for pin in BOTONES]

# Define una función para enviar un mensaje OSC
def enviar_mensaje_osc(address, *args):
    client.send_message(address, args)

# Variables para el seguimiento del estado anterior de los botones
estado_anterior = [True] * len(BOTONES)

# Bucle para leer el estado de los botones y enviar mensajes OSC cuando haya cambios
try:
    while True:
        for i, button in enumerate(buttons):
            estado_boton = button.is_pressed
            # Verifica si ha habido un cambio en el estado del botón
            if estado_boton != estado_anterior[i]:
                direccion_osc = f"/boton{i + 1}"
                estado_anterior[i] = estado_boton

                # Envía un mensaje OSC con el estado actual del botón
                enviar_mensaje_osc(direccion_osc, int(estado_boton))
        enviar_mensaje_osc("/pot",int(mcp.read_adc(0)))
        time.sleep(0.01)  # Pequeña pausa para evitar lecturas repetidas

except KeyboardInterrupt:
    pass

# Limpia los recursos GPIO al salir
for button in buttons:
    button.close()
    