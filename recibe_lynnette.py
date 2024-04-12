import threading
from pythonosc import dispatcher, osc_server
import time
import board
import neopixel

# Import SPI library (for hardware SPI) and MCP3008 library.
import Adafruit_GPIO.SPI as SPI
#import Adafruit_MCP3008



SPI_PORT   = 0
SPI_DEVICE = 0
#mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

pixels = neopixel.NeoPixel(board.D18, 8)



hora = 0
minuto = 0
def mapear_valor(valor, valor_minimo1, valor_maximo1, valor_minimo2, valor_maximo2):
    valor_mapeado = (valor - valor_minimo1) * (valor_maximo2 - valor_minimo2) / (valor_maximo1 - valor_minimo1) + valor_minimo2
    return valor_mapeado
valor = 0
valor_minimo1 = 0
valor_maximo1= 1
valor_minimo2 = 0
valor_maximo2 = 255


# Función para controlar los LEDs
def controlar_leds():
    while True:
        # Tu lógica para controlar los LEDs aquí
        # Por ejemplo, puedes actualizar los valores de duty_cycle de los LEDs aquí
        time.sleep(0.01)  # Asegúrate de agregar un pequeño retraso para evitar que el hilo consuma demasiada CPU

# Función para manejar los mensajes OSC
def manejar_led(address, *args):
    global hora
    global minuto
    if address == "/ch1":
        #print(args[0])
        r = mapear_valor((args[0]),valor_minimo1, valor_maximo1,valor_minimo2,valor_maximo2)
        print(r)
        pixels[0] = (r, r, r)
        pixels.show()
        pwm_value_uno = int(mapear_valor(int(args[0]), 0, 100, 0, 65535))
        led_uno.duty_cycle = pwm_value_uno
    elif address == "/ch2":
        #print(args[0])
   
        g = mapear_valor((args[0]),valor_minimo1, valor_maximo1,valor_minimo2,valor_maximo2)
        #print(r)
        ##pixels.show()
        #pwm_value_dos = int(mapear_valor(int(args[0]), 0, 100, 0, 65535))
        #led_dos.duty_cycle = pwm_value_dos
    elif address == "/ch3":
        #print(args[0])

        b = mapear_valor((args[0]),valor_minimo1, valor_maximo1,valor_minimo2,valor_maximo2)
        #print(r)
        #pixels[2] = (b, b, b)
        #pixels.show()
        #pwm_value_tres = int(mapear_valor(int(args[0]), 0, 100, 0, 65535))
        #led_tres.duty_cycle = pwm_value_tres
    elif address == "/h":
        r = mapear_valor((args[0]),valor_minimo1, valor_maximo1,valor_minimo2,valor_maximo2)
        print(r)
        pixels[0] = (r, r, r)
        pixels.show()
        pwm_value_uno = int(mapear_valor(int(args[0]), 0, 100, 0, 65535))
        led_uno.duty_cycle = pwm_value_uno
        hora = int(args[0])

        print("hora", hora)
    elif address == "/m":
     
        minuto = (int(args[0]))

        print("minuto", minuto)

# Función para mapear valores


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

# Inicia el hilo para controlar los LEDs
leds_thread = threading.Thread(target=controlar_leds)
leds_thread.start()
