import board
import digitalio

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
    # Lee el estado de cada botón y almacénalo en una lista
    estados_de_botones = [pin.value for pin in pines_de_botones]

    # Imprime los estados de los botones
    print("Estados de los botones:", estados_de_botones)
