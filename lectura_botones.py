import board
import digitalio

# Configura el pin del botón como una entrada digital
pin_del_boton = digitalio.DigitalInOut(board.D17)  # Cambia D2 al número de pin que estés usando
pin_del_boton.direction = digitalio.Direction.INPUT
pin_del_boton.pull = digitalio.Pull.DOWN  # Opcional: configura la resistencia pull-down si es necesario

while True:
    # Lee el estado del botón
    estado_del_boton = pin_del_boton.value

    if estado_del_boton:
        print("El botón está presionado")
    else:
        print("El botón no está presionado")
