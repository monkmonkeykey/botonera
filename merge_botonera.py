import threading
from pythonosc import dispatcher, osc_server, udp_client
import time
import board
import neopixel
from gpiozero import Button
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Hardware SPI configuration:
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Configura el cliente OSC
osc_client = udp_client.SimpleUDPClient("192.168.15.8", 10000)  # Cambia la dirección y el puerto según tus necesidades

# Configura los pines GPIO de los botones
BUTTON_PINS = [13,26,27,21]
buttons = [Button(pin, pull_up=True) for pin in BUTTON_PINS]

# Configura los píxeles NeoPixel
pixels = neopixel.NeoPixel(board.D18, 8)

def mapear_valor(valor, valor_minimo1, valor_maximo1, valor_minimo2, valor_maximo2):
    valor_mapeado = (valor - valor_minimo1) * (valor_maximo2 - valor_minimo2) / (valor_maximo1 - valor_minimo1) + valor_minimo2
    return valor_mapeado

def controlar_leds():
    while True:
        # Tu lógica para controlar los LEDs aquí
        # Por ejemplo, puedes actualizar los valores de duty_cycle de los LEDs aquí
        time.sleep(0.01)  # Asegúrate de agregar un pequeño retraso para evitar que el hilo consuma demasiada CPU

def manejar_led(address, *args):
    if address == "/ch1":
        r = mapear_valor(args[0], 0, 1, 0, 255)
        pixels[0] = (r, r, r)
        pixels.show()
    elif address == "/ch2":
        g = mapear_valor(args[0], 0, 1, 0, 255)
        pixels[1] = (g, g, g)
        pixels.show()
    elif address == "/ch3":
        b = mapear_valor(args[0], 0, 1, 0, 255)
        pixels[2] = (b, b, b)
        pixels.show()

def enviar_mensaje_osc(address, *args):
    osc_client.send_message(address, args)

def leer_botones():
    estado_anterior = [True] * len(BUTTON_PINS)
    while True:
        for i, button in enumerate(buttons):
            estado_boton = button.is_pressed
            if estado_boton != estado_anterior[i]:
                direccion_osc = f"/boton{i + 1}"
                estado_anterior[i] = estado_boton
                enviar_mensaje_osc(direccion_osc, int(estado_boton))
        enviar_mensaje_osc("/pot", int(mcp.read_adc(0)))
        time.sleep(0.1)

# Crea un despachador de mensajes OSC
dispatcher = dispatcher.Dispatcher()
direcciones_osc = ["/ch1", "/ch2", "/ch3"]
for direccion in direcciones_osc:
    dispatcher.map(direccion, manejar_led)

# Configura y corre el servidor OSC en un hilo separado
ip_escucha = "0.0.0.0"  # Escucha en todas las interfaces de red
puerto_escucha = 8000   # Puerto en el que escucha el servidor
servidor = osc_server.ThreadingOSCUDPServer((ip_escucha, puerto_escucha), dispatcher)
print(f"Escuchando en {ip_escucha}:{puerto_escucha}")

# Inicia el servidor y los hilos en paralelo
servidor_thread = threading.Thread(target=servidor.serve_forever)
leds_thread = threading.Thread(target=controlar_leds)
botones_thread = threading.Thread(target=leer_botones)

servidor_thread.start()
leds_thread.start()
botones_thread.start()
