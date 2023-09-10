import threading
from pythonosc import dispatcher, osc_server
import board
import busio
import digitalio
import adafruit_tlc5947


# Define los pines conectados al TLC5947
SCK = board.SCK
MOSI = board.MOSI
LATCH = digitalio.DigitalInOut(board.D27)

# Inicializa el bus SPI.
spi = busio.SPI(clock=SCK, MOSI=MOSI)

# Inicializa el controlador TLC5947
tlc5947 = adafruit_tlc5947.TLC5947(spi, LATCH)
# Crea un objeto PWMOut para el LED (en este ejemplo, el LED está conectado al canal 0)
led = tlc5947.create_pwm_out(1)


# Define funciones para manejar los mensajes OSC y controlar los LEDs
def manejar_led(address, *args):
    
    if address == "/ch1":
            print(args[0])
    elif address == "/ch2":
        pwm_value = mapear_valor(int(args[0]),0,100,0,65535)
        led.duty_cycle = pwm_value
        
    elif address == "/ch3":
        print(args[0])
#tlc5947.write()
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

def mapear_valor(valor, valor_minimo1, valor_maximo1, valor_minimo2, valor_maximo2):
    valor_mapeado = (valor - valor_minimo1) * (valor_maximo2 - valor_minimo2) / (valor_maximo1 - valor_minimo1) + valor_minimo2
    return valor_mapeado
