import threading
from pythonosc import dispatcher, osc_server
import RPi.GPIO as GPIO

# Configurar pines GPIO para los LEDs
GPIO.setmode(GPIO.BCM)
LED_PIN_1 = 22  # Cambia el número de pin según tu configuración
LED_PIN_2 = 23  # Cambia el número de pin según tu configuración
LED_PIN_3 = 26  # Cambia el número de pin según tu configuración
GPIO.setup(LED_PIN_1, GPIO.OUT)
GPIO.setup(LED_PIN_2, GPIO.OUT)
GPIO.setup(LED_PIN_3, GPIO.OUT)

# Configurar PWM para el LED controlado por el canal /ch2
pwm = GPIO.PWM(LED_PIN_2, 100)  # Pin 22 con frecuencia de 100 Hz (puedes ajustarla según tu necesidad)
pwm.start(0)  # Iniciar PWM con ciclo de trabajo del 0%

# Define funciones para manejar los mensajes OSC y controlar los LEDs
def manejar_led(address, *args):
    print(f"Recibido mensaje desde {address}: {args}")
    pin = None
    if address == "/ch1":
        pin = LED_PIN_1
    elif address == "/ch2":
        # El valor flotante recibido controlará el ciclo de trabajo del PWM
        duty_cycle = float(args[0])
        pwm.ChangeDutyCycle(duty_cycle)
    elif address == "/ch3":
        pin = LED_PIN_3

    if pin is not None:
        if args[0] == 1:
            GPIO.output(pin, GPIO.HIGH)
        else:
            GPIO.output(pin, GPIO.LOW)

# Resto del código sin cambios

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
print(f"Escuchando en {ip_escucha}:{puerto_escucha}")

# Iniciar el servidor en un hilo separado
servidor_thread = threading.Thread(target=servidor.serve_forever)
servidor_thread.start()

# Esperar que el servidor termine (esto podría ser en otro hilo o proceso si es necesario)
servidor_thread.join()
