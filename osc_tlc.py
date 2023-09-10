# -*- coding: utf-8 -*-
import threading
from pythonosc.udp_client import SimpleUDPClient
from pythonosc import dispatcher, osc_server
import RPi.GPIO as GPIO
import time
import board
import busio
import digitalio
import adafruit_tlc5947

# Configura el cliente OSC
client = SimpleUDPClient("192.168.15.6", 10000)  # Cambia la dirección y el puerto según tus necesidades

# Inicializa SPI bus para TLC5947
SCK = board.SCK
MOSI = board.MOSI
LATCH = digitalio.DigitalInOut(board.D27)
spi = busio.SPI(clock=SCK, MOSI=MOSI)

# Inicializa TLC5947
tlc5947 = adafruit_tlc5947.TLC5947(spi, LATCH)
red = tlc5947.create_pwm_out(0)
green = tlc5947.create_pwm_out(1)
blue = tlc5947.create_pwm_out(2)
nivel_iluminacion_red = 32767
nivel_iluminacion_green = 32767
nivel_iluminacion_blue = 32767
red.duty_cycle = nivel_iluminacion_red
green.duty_cycle = nivel_iluminacion_green
blue.duty_cycle = nivel_iluminacion_blue

# Configura los pines GPIO de los botones
PINES_BOTONES = [17, 18, 24, 25, 5, 6, 16, 19]

GPIO.setmode(GPIO.BCM)

for pin in PINES_BOTONES:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define una función para enviar un mensaje OSC
def enviar_mensaje_osc(address, *args):
    client.send_message(address, args)

# En la función manejar_led, envía mensajes OSC compatibles con el primer código
def manejar_led(address, *args):
    if address == "/ch1":
        estado_led = 1 if args[0] > 0 else 0
        red.duty_cycle = estado_led * nivel_iluminacion_red
    elif address == "/ch2":
        duty_cycle = float(args[0])
        blue.duty_cycle = int(duty_cycle * 65535)
    elif address == "/ch3":
        estado_led = 1 if args[0] > 0 else 0
        green.duty_cycle = estado_led * nivel_iluminacion_green

# Variables para el seguimiento del estado anterior de los botones
estado_anterior = [1] * len(PINES_BOTONES)

# Crea un despachador de mensajes OSC
dispatcher = dispatcher.Dispatcher()

# Mapea las direcciones OSC a la función de manejo
direcciones_osc = ["/ch1", "/ch2", "/ch3"]
for direccion in direcciones_osc:
    dispatcher.map(direccion, manejar_led)

# Configura y corre el servidor OSC en hilos separados
ip_escucha = "0.0.0.0"  # Escucha en todas las interfaces de red
puerto_escucha = 8000   # Puerto en el que escucha el servidor

servidor = osc_server.ThreadingOSCUDPServer((ip_escucha, puerto_escucha), dispatcher)

# Iniciar el servidor en un hilo separado
servidor_thread = threading.Thread(target=servidor.serve_forever)
servidor_thread.start()

# Resto del código como está
# ...

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
