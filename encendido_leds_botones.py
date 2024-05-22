import RPi.GPIO as GPIO
import time

# Configurar el modo de numeración de los pines
GPIO.setmode(GPIO.BCM)

# Definir los pines GPIO para PWM
pwm_pins = [18, 19, 13, 12, 6, 26, 21]

# Configurar los pines como salidas
for pin in pwm_pins:
    GPIO.setup(pin, GPIO.OUT)

# Configurar PWM en los pines con una frecuencia de 1000 Hz
pwms = [GPIO.PWM(pin, 1000) for pin in pwm_pins]

# Iniciar PWM con un ciclo de trabajo del 0%
for pwm in pwms:
    pwm.start(0)

try:
    while True:
        for duty_cycle in range(0, 101, 1):
            for pwm in pwms:
                pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.01)
        for duty_cycle in range(100, -1, -1):
            for pwm in pwms:
                pwm.ChangeDutyCycle(duty_cycle)
            time.sleep(0.01)
except KeyboardInterrupt:
    pass

# Detener PWM y limpiar la configuración de GPIO
for pwm in pwms:
    pwm.stop()
GPIO.cleanup()
