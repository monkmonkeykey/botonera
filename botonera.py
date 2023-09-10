from pythonosc.udp_client import SimpleUDPClient
import RPi.GPIO as GPIO
import time

# Configura el cliente OSC
client = SimpleUDPClient("192.168.15.7", 1000)  # Cambia la dirección y el puerto según tus necesidades

# Configura los pines GPIO de los botones
PINES_BOTONES = [17, 18, 24, 25 ,5, 6, 16, 19]

GPIO.setmode(GPIO.BCM)

for pin in PINES_BOTONES:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# Define una función para enviar un mensaje OSC
def enviar_mensaje_osc(address, *args):
    client.send_message(address, args)

# Bucle para leer el estado de los botones y enviar mensajes OSC
try:
    while True:
        for i, pin in enumerate(PINES_BOTONES):
            estado_boton = GPIO.input(pin)
            direccion_osc = f"/boton{i + 1}"

            # Envía mensajes OSC en función del estado del botón
            if estado_boton == 0:
                enviar_mensaje_osc(direccion_osc, 1)  # Botón presionado
            else:
                enviar_mensaje_osc(direccion_osc, 0)  # Botón liberado

        time.sleep(0.1)  # Pequeña pausa para evitar lecturas repetidas

except KeyboardInterrupt:
    GPIO.cleanup()
