import threading
from pythonosc import dispatcher, osc_server
import time
import board
import neopixel
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

pixels = neopixel.NeoPixel(board.D18, 8)
pixel_lock = threading.Lock()  # Semáforo para sincronizar acceso a los NeoPixels

valor_minimo1 = 0
valor_maximo1= 1
valor_minimo2 = 0
valor_maximo2 = 255

def mapear_valor(valor, valor_minimo1, valor_maximo1, valor_minimo2, valor_maximo2):
    return (valor - valor_minimo1) * (valor_maximo2 - valor_minimo2) / (valor_maximo1 - valor_minimo1) + valor_minimo2

# Función para manejar los mensajes OSC
def manejar_led(address, *args):
    if address in ["/ch1", "/ch2", "/ch3"]:
        valor_mapeado = int(mapear_valor(args[0], valor_minimo1, valor_maximo1, valor_minimo2, valor_maximo2))
        with pixel_lock:
            pixels[0] = (valor_mapeado, valor_mapeado, valor_mapeado)
            pixels.show()

# Crea un despachador de mensajes OSC
dispatcher = dispatcher.Dispatcher()

# Mapea las direcciones OSC a la función de manejo
direcciones_osc = ["/ch1", "/ch2", "/ch3"]
for direccion in direcciones_osc:
    dispatcher.map(direccion, manejar_led)

# Configura y corre el servidor OSC en un hilo separado
ip_escucha = "0.0.0.0"  # Escucha en todas las interfaces de red
puerto_escucha = 9000   # Puerto en el que escucha el servidor

servidor = osc_server.ThreadingOSCUDPServer((ip_escucha, puerto_escucha), dispatcher)
print(f"Escuchando en {ip_escucha}:{puerto_escucha}")

# Inicia el servidor en un hilo separado
servidor_thread = threading.Thread(target=servidor.serve_forever)
servidor_thread.start()

# Mantén el programa en ejecución
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("Deteniendo el servidor OSC...")
    servidor.shutdown()
