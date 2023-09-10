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

# Define pins connected to the TLC5947
SCK = board.SCK
MOSI = board.MOSI
LATCH = digitalio.DigitalInOut(board.D27)

# Initialize SPI bus.
spi = busio.SPI(clock=SCK, MOSI=MOSI)

# Initialize TLC5947
tlc5947 = adafruit_tlc5947.TLC5947(spi, LATCH)

# Configura el cliente OSC
client = SimpleUDPClient("192.168.15.6", 10000)  # Cambia la dirección y el puerto según tus necesidades

# Configurar pines GPIO para los LEDs
GPIO.setmode(GPIO.BCM)
LED_PIN_1 = 22  # Cambia el número de pin según tu configuración
LED_PIN_2 = 23  # Cambia el número de pin según tu configuración
LED_PIN_3 = 26  # Cambia el número de pin según tu configuración
GPIO.setup(LED_PIN_1, GPIO.OUT)
GPIO.setup(LED_PIN_2, GPIO.OUT)
GPIO.setup(LED_PIN_3, GPIO.OUT)

red = tlc5947.create_pwm_out(0)
green = tlc5947.create_pwm_out(1)
blue = tlc5947.create_pwm_out(2)


# Configurar PWM para el LED controlado por el canal /ch2
pwm = GPIO.PWM(LED_PIN_2, 100)  # Pin 22 con frecuencia de 100 Hz (puedes ajustarla según tu necesidad)
pwm.start(0)  # Iniciar PWM con ciclo de trabajo del 0%

# Configura los pines GPIO de los botones
PINES_BOTONES = [17, 18, 24, 25, 5, 6, 16, 19]

GPIO.setmode(GPIO.BCM)

for pin in PINES_BOTONES:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define una función para enviar un mensaje OSC
def enviar_mensaje_osc(address, *args):
    client.send_message(address, args)

# Define funciones para manejar los mensajes OSC y controlar los LEDs
def manejar_led(address, *args):
    #print(f"Recibido mensaje desde {address}: {args}")
    pin = None
    if address == "/ch1":
        pin = LED_PIN_1
    elif address == "/ch2":
        # El valor flotante recibido controlará el ciclo de trabajo del PWM
        duty_cycle = float(args[0])
        pwm.duty_cycle(duty_cycle)
    elif address == "/ch3":
        pin = LED_PIN_3

    if pin is not None:
        if args[0] == 1:
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)

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
#print(f"Escuchando en {ip_escucha}:{puerto_escucha}")

# Define una función para leer el estado de los botones y enviar mensajes OSC cuando haya cambios
def leer_botones():
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

# Iniciar el servidor en un hilo separado
servidor_thread = threading.Thread(target=servidor.serve_forever)
servidor_thread.start()

# Iniciar la lectura de botones en otro hilo
botones_thread = threading.Thread(target=leer_botones)
botones_thread.start()

# Esperar que los hilos terminen (esto podría ser en otro hilo o proceso si es necesario)
servidor_thread.join()
botones_thread.join()
