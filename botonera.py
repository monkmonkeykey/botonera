# -*- coding: utf-8 -*-
from pythonosc.udp_client import SimpleUDPClient
import RPi.GPIO as GPIO
import time

# Configura el cliente OSC
client = SimpleUDPClient("192.168.15.7", 10000)  # Cambia la dirección y el puerto según tus necesidades

# Configura los pines GPIO de los botones
PINES_BOTONES = [17, 18, 24, 25, 5, 6, 16, 19]

GPIO.setmode(GPIO.BCM)

for pin in PINES_BOTONES:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define una función para enviar un mensaje OSC
def enviar_mensaje_osc(address, *args):
    client.send_message(address, args)

# Variables para el seguimiento del estado anterior de los botones
estado_anterior = [1] * len(PINES_BOTONES)

# Bucle para leer el estado de los botones y enviar mensajes OSC cuando haya cambios
try:
    while True:
        for i, pin in enumerate(PINES_BOTONES):
            estado_boton = GPIO.input(pin)

            # Verifica si ha habido un cambio en el estado del botón
            if estado_boton != estado_anterior[i]:
                direccion_osc = f"/boton{i + 1}"
                estado_anterior[i] = estado_boton

                # Envía un mensaje OSC con el estado actual del botón
                enviar_mensaje_osc(direccion_osc, estado_boton)

        time.sleep(0.1)  # Pequeña pausa para evitar lecturas repetidas

except KeyboardInterrupt:
    GPIO.cleanup()
