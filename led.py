import RPi.GPIO as GPIO
import time
import threading

# Configura la numeración del GPIO
GPIO.setmode(GPIO.BCM)

# Define el número del puerto GPIO que se usará
puerto_gpio = 23

# Configura el puerto GPIO como salida
GPIO.setup(puerto_gpio, GPIO.OUT)

# Función para encender y apagar el LED
def control_led():
    try:
        while True:
            # Enciende el LED
            GPIO.output(puerto_gpio, GPIO.HIGH)
            print("LED encendido")
    
            # Espera durante 5 segundos
            time.sleep(5)
    
            # Apaga el LED
            GPIO.output(puerto_gpio, GPIO.LOW)
            print("LED apagado")
    
            # Espera durante 5 segundos antes de repetir
            time.sleep(5)
    
    except KeyboardInterrupt:
        pass

# Crear un hilo para controlar el LED
led_thread = threading.Thread(target=control_led)

try:
    # Iniciar el hilo
    led_thread.start()
    
    # Aquí puedes agregar el resto de tu código sin que se vea afectado por los lapsos de tiempo del LED
    
    # Ejemplo: Puedes realizar otras tareas aquí mientras el LED se enciende y apaga en segundo plano.
    while True:
        pass

except KeyboardInterrupt:
    pass

finally:
    # Detener el hilo y limpiar los recursos del GPIO
    GPIO.cleanup()
