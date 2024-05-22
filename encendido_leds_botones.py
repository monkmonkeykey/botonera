import threading
from pythonosc import dispatcher, osc_server
import time
import RPi.GPIO as GPIO

# Desactiva las advertencias de GPIO
GPIO.setwarnings(False)

# Configuración de los pines GPIO para los LEDs
LED_PIN_1 = 18  # Pin GPIO para LED 1
LED_PIN_2 = 23  # Pin GPIO para LED 2
LED_PIN_3 = 24  # Pin GPIO para LED 3
LED_PIN_4 = 12  # Pin GPIO para LED 4
LED_PIN_5 = 13  # Pin GPIO para LED 5
LED_PIN_6 = 19  # Pin GPIO para LED 6
LED_PIN_7 = 26  # Pin GPIO para LED 7

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_1, GPIO.OUT)
GPIO.setup(LED_PIN_2, GPIO.OUT)
GPIO.setup(LED_PIN_3, GPIO.OUT)
GPIO.setup(LED_PIN_4, GPIO.OUT)
GPIO.setup(LED_PIN_5, GPIO.OUT)
GPIO.setup(LED_PIN_6, GPIO.OUT)
GPIO.setup(LED_PIN_7, GPIO.OUT)

# Configuración de PWM para los LEDs
# Puedes probar diferentes frecuencias, aquí usamos 500 Hz
led1_pwm = GPIO.PWM(LED_PIN_1, 500)
led2_pwm = GPIO.PWM(LED_PIN_2, 500)
led3_pwm = GPIO.PWM(LED_PIN_3, 500)
led4_pwm = GPIO.PWM(LED_PIN_4, 500)
led5_pwm = GPIO.PWM(LED_PIN_5, 500)
led6_pwm = GPIO.PWM(LED_PIN_6, 500)
led7_pwm = GPIO.PWM(LED_PIN_7, 500)

led1_pwm.start(0)  # Inicia PWM con 0% de duty cycle
led2_pwm.start(0)
led3_pwm.start(0)
led4_pwm.start(0)
led5_pwm.start(0)
led6_pwm.start(0)
led7_pwm.start(0)

def mapear_valor(valor, valor_minimo1, valor_maximo1, valor_minimo2, valor_maximo2):
    valor_mapeado = (valor - valor_minimo1) * (valor_maximo2 - valor_minimo2) / (valor_maximo1 - valor_minimo1) + valor_minimo2
    return valor_mapeado

# Función para manejar los mensajes OSC
def manejar_led(address, *args):
    if address == "/ch1":
        valor_pwm = mapear_valor(float(args[0]), 0, 1, 0, 100)
        led1_pwm.ChangeDutyCycle(valor_pwm)
    elif address == "/ch2":
        valor_pwm = mapear_valor(float(args[0]), 0, 1, 0, 100)
        led2_pwm.ChangeDutyCycle(valor_pwm)
    elif address == "/ch3":
        valor_pwm = mapear_valor(float(args[0]), 0, 1, 0, 100)
        led3_pwm.ChangeDutyCycle(valor_pwm)
    elif address == "/ch4":
        valor_pwm = mapear_valor(float(args[0]), 0, 1, 0, 100)
        led4_pwm.ChangeDutyCycle(valor_pwm)
    elif address == "/ch5":
        valor_pwm = mapear_valor(float(args[0]), 0, 1, 0, 100)
        led5_pwm.ChangeDutyCycle(valor_pwm)
    elif address == "/ch6":
        valor_pwm = mapear_valor(float(args[0]), 0, 1, 0, 100)
        led6_pwm.ChangeDutyCycle(valor_pwm)
    elif address == "/ch7":
        valor_pwm = mapear_valor(float(args[0]), 0, 1, 0, 100)
        led7_pwm.ChangeDutyCycle(valor_pwm)
    elif address == "/h":
        print(args[0])
    elif address == "/m":
        print(args[0])

# Crea un despachador de mensajes OSC
dispatcher = dispatcher.Dispatcher()

# Mapea las direcciones OSC a la función de manejo
direcciones_osc = ["/ch1", "/ch2", "/ch3", "/ch4", "/ch5", "/ch6", "/ch7", "/h", "/m"]
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
