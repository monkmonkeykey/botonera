import RPi.GPIO as GPIO
import time
from pythonosc import dispatcher
from pythonosc import osc_server

# Configurar el modo de numeración de los pines
GPIO.setmode(GPIO.BCM)

# Definir los pines GPIO para PWM
pwm_pins = [18, 19, 13, 12, 6, 26, 21]

# Configurar los pines como salidas
for pin in pwm_pins:
    GPIO.setup(pin, GPIO.OUT)

# Configurar PWM en los pines con una frecuencia de 1000 Hz
pwms = [GPIO.PWM(pin, 1000) for pin in pwm_pins]

# Iniciar PWM con un ciclo de trabajo del 50%
for pwm in pwms:
    pwm.start(50)

def set_led_intensity(unused_addr, pin_index, intensity):
    """Función para ajustar la intensidad del LED."""
    if 0 <= pin_index < len(pwms):
        intensity = max(0, min(100, intensity))  # Asegurarse de que la intensidad esté entre 0 y 100
        pwms[pin_index].ChangeDutyCycle(intensity)
    print(f"Recibido: Pin {pin_index}, Intensidad {intensity}")

# Configurar el dispatcher para manejar los mensajes OSC
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/led", set_led_intensity)  # Asignar la dirección OSC /led a la función set_led_intensity

# Configurar el servidor OSC
ip = "0.0.0.0"  # Escuchar en todas las interfaces
port = 5005     # Puerto en el que se escucharán los mensajes OSC

server = osc_server.ThreadingOSCUDPServer((ip, port), dispatcher)

print(f"Servidor OSC escuchando en {ip}:{port}")
try:
    server.serve_forever()
except KeyboardInterrupt:
    pass

# Detener PWM y limpiar la configuración de GPIO al finalizar
for pwm in pwms:
    pwm.stop()
GPIO.cleanup()
