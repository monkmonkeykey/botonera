import RPi.GPIO as GPIO
import time
import threading
from pythonosc import dispatcher, osc_server

# Configuración de los pines GPIO para los LEDs RGB
led_pins = {"r": 18, "g": 19, "b": 20}  # Mapeo de colores a pines GPIO
for pin in led_pins.values():
    GPIO.setup(pin, GPIO.OUT)

# Configurar PWM en los pines
pwms = {color: GPIO.PWM(pin, 100) for color, pin in led_pins.items()}
for pwm in pwms.values():
    pwm.start(0)  # Iniciar con ciclo de trabajo del 0%

# Función para controlar los LEDs con PWM
def controlar_leds():
    global pwms
    while True:
        # Tu lógica para controlar los LEDs aquí
        # Por ejemplo, puedes actualizar los valores de duty_cycle de los LEDs aquí
        time.sleep(0.01)  # Asegúrate de agregar un pequeño retraso para evitar que el hilo consuma demasiada CPU

# Función para manejar los mensajes OSC
def manejar_led(address, *args):
    global pwms
    if address == "/ch1":
        pwm_value = int(args[0]) * 2.55  # Escalar el valor de 0-100 a 0-255
        pwms["r"].ChangeDutyCycle(pwm_value)
    elif address == "/ch2":
        pwm_value = int(args[0]) * 2.55
        pwms["g"].ChangeDutyCycle(pwm_value)
    elif address == "/ch3":
        pwm_value = int(args[0]) * 2.55
        pwms["b"].ChangeDutyCycle(pwm_value)
    elif address == "/h":
        # Tu lógica para manejar los datos de hora
        pass
    elif address == "/m":
        # Tu lógica para manejar los datos de minuto
        pass

# Crea un despachador de mensajes OSC
dispatcher = dispatcher.Dispatcher()

# Mapea las direcciones OSC a la función de manejo
direcciones_osc = ["/ch1", "/ch2", "/ch3", "/h", "/m"]
for direccion in direcciones_osc:
    dispatcher.map(direccion, manejar_led)

# Configura y corre el servidor OSC en un hilo separado
ip_escucha = "0.0.0.0"  # Escucha en todas las interfaces de red
puerto_escucha = 8000   # Puerto en el que escucha el servidor

servidor = osc_server.ThreadingOSCUDPServer((ip_escucha, puerto_escucha), dispatcher)
print(f"Escuchando en {ip_escucha}:{puerto_escucha}")

# Inicia el servidor en un hilo separado
servidor_thread = threading.Thread(target=servidor.serve_forever)
servidor_thread.start()

# Inicia el hilo para controlar los LEDs con PWM
leds_thread = threading.Thread(target=controlar_leds)
leds_thread.start()
