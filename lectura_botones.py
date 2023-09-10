import board
import digitalio
from pythonosc.udp_client import SimpleUDPClient
import time

# Configura el cliente OSC
client = SimpleUDPClient("192.168.15.7", 10000)  # Cambia la dirección y el puerto según tus necesidades

# Configura los pines de los botones como entradas digitales
pines_de_botones = [
    digitalio.DigitalInOut(board.D17),
    digitalio.DigitalInOut(board.D18),
    digitalio.DigitalInOut(board.D24),
    digitalio.DigitalInOut(board.D25),
    digitalio.DigitalInOut(board.D5),
    digitalio.DigitalInOut(board.D6),
    digitalio.DigitalInOut(board.D16),
    digitalio.DigitalInOut(board.D19),
]

# Configura la dirección de los pines como entrada y, opcionalmente, la resistencia pull-down
for pin in pines_de_botones:
    pin.direction = digitalio.Direction.INPUT
    pin.pull = digitalio.Pull.DOWN  # Opcional: configura la resistencia pull-down si es necesario

while True:
    for i, pin in enumerate(pines_de_botones):
        # Lee el estado de un botón específico
        estado_del_boton = pin.value

        # Imprime el estado del botón
        #print(f"Estado del botón {i + 1}: {estado_del_boton}")

        # Envia el estado del botón vía OSC
        client.send_message(f"/boton{i + 1}", estado_del_boton)

    # Espera un tiempo antes de volver a leer los botones
    time.sleep(0.1)  # Puedes ajustar el tiempo de espera según tus necesidades
