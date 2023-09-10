import board
import busio
import digitalio
from digitalio import DigitalInOut, Direction, Pull

import adafruit_tlc5947

# Configura el cliente OSC
client = SimpleUDPClient("192.168.15.6", 10000)  # Cambia la dirección y el puerto según tus necesidades

# Configurar pines GPIO para los LEDs
LED_PIN_1 = board.D22  # Cambia el número de pin según tu configuración
LED_PIN_2 = board.D23  # Cambia el número de pin según tu configuración
LED_PIN_3 = board.D26  # Cambia el número de pin según tu configuración

# Inicializa los pines GPIO de los LEDs
led1 = DigitalInOut(LED_PIN_1)
led1.direction = Direction.OUTPUT
led2 = DigitalInOut(LED_PIN_2)
led2.direction = Direction.OUTPUT
led3 = DigitalInOut(LED_PIN_3)
led3.direction = Direction.OUTPUT

# Configurar PWM para el LED controlado por el canal /ch2
pwm = board.D22  # Cambia el número de pin según tu configuración
pwm_out = DigitalInOut(pwm)
pwm_out.direction = Direction.OUTPUT
pwm_out.frequency = 100
pwm_out.duty_cycle = 0  # Iniciar PWM con ciclo de trabajo del 0%

# Configura los pines GPIO de los botones
PINES_BOTONES = [board.D17, board.D18, board.D24, board.D25, board.D5, board.D6, board.D16, board.D19]

# Inicializa los pines GPIO de los botones
buttons = [DigitalInOut(pin) for pin in PINES_BOTONES]
for button in buttons:
    button.direction = Direction.INPUT
    button.pull = Pull.UP

# Define una función para enviar un mensaje OSC
def enviar_mensaje_osc(address, *args):
    client.send_message(address, args)

# Define funciones para manejar los mensajes OSC y controlar los LEDs
def manejar_led(address, *args):
    #print(f"Recibido mensaje desde {address}: {args}")
    pin = None
    if address == "/ch1":
        pin = led1
    elif address == "/ch2":
        # El valor flotante recibido controlará el ciclo de trabajo del PWM
        duty_cycle = float(args[0])
        pwm_out.duty_cycle = int(duty_cycle * 65535)  # Escala el valor al rango 0-65535
    elif address == "/ch3":
        pin = led3

    if pin is not None:
        if args[0] == 1:
            pin.value = True
        else:
            pin.value = False

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
            for i, button in enumerate(buttons):
                estado_boton = not button.value  # Lee el estado y lo invierte (botón pull-up)

                # Verifica si ha habido un cambio en el estado del botón
                if estado_boton != estado_anterior[i]:
                    direccion_osc = f"/boton{i + 1}"
                    estado_anterior[i] = estado_boton

                    # Envía un mensaje OSC con el estado actual del botón
                    enviar_mensaje_osc(direccion_osc, estado_boton)

            time.sleep(0.1)  # Pequeña pausa para evitar lecturas repetidas

    except KeyboardInterrupt:
        pass  # Manejo de la excepción para una salida limpia

finally:
    GPIO.cleanup()  # Limpia los pines GPIO cuando se termina el programa