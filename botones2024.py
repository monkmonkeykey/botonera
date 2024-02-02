import threading
from pythonosc import dispatcher, osc_server
from pythonosc.udp_client import SimpleUDPClient
import time
import board
import neopixel
from gpiozero import Button
import Adafruit_GPIO.SPI as SPI
import Adafruit_MCP3008

# Configuración del servidor OSC
ip_escucha = "0.0.0.0"
puerto_escucha = 8000

servidor = osc_server.ThreadingOSCUDPServer((ip_escucha, puerto_escucha), dispatcher)
print(f"Escuchando en {ip_escucha}:{puerto_escucha}")
# Configuración del cliente OSC
cliente_osc = SimpleUDPClient("192.168.15.8", 10000)  # Cambia la dirección y el puerto según tus necesidades

# Configuración de hardware SPI y MCP3008
SPI_PORT = 0
SPI_DEVICE = 0
mcp = Adafruit_MCP3008.MCP3008(spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE))

# Configuración de botones y LEDs
BOTONES = [13, 26, 27, 21]
buttons = [Button(pin, pull_up=True) for pin in BOTONES]
pixels = neopixel.NeoPixel(board.D18, 8)

# Variables para el seguimiento del estado anterior de los botones
estado_anterior = [True] * len(BOTONES)

# Función para enviar un mensaje OSC
def enviar_mensaje_osc(address, *args):
    cliente_osc.send_message(address, args)

# Función para manejar los mensajes OSC
def manejar_led(address, *args):
    if address == "/ch1":
        r = mapear_valor(args[0], valor_minimo1, valor_maximo1, valor_minimo2, valor_maximo2)
        pixels[0] = (r, 0, 0)
        pixels.show()
    elif address == "/ch2":
        g = mapear_valor(args[0], valor_minimo1, valor_maximo1, valor_minimo2, valor_maximo2)
        pixels[1] = (0, g, 0)
        pixels.show()
    elif address == "/ch3":
        b = mapear_valor(args[0], valor_minimo1, valor_maximo1, valor_minimo2, valor_maximo2)
        pixels[2] = (0, 0, b)
        pixels.show()

# Función para controlar los LEDs
def controlar_leds():
    while True:
        # Tu lógica para controlar los LEDs aquí
        # Por ejemplo, puedes actualizar los valores de duty_cycle de los LEDs aquí
        time.sleep(0.01)  # Asegúrate de agregar un pequeño retraso para evitar que el hilo consuma demasiada CPU

# Función para mapear valores
def mapear_valor(valor, valor_minimo1, valor_maximo1, valor_minimo2, valor_maximo2):
    valor_mapeado = (valor - valor_minimo1) * (valor_maximo2 - valor_minimo2) / (valor_maximo1 - valor_minimo1) + valor_minimo2
    return valor_mapeado

# Bucle para leer el estado de los botones y enviar mensajes OSC cuando haya cambios
def leer_botones():
    try:
        while True:
            for i, button in enumerate(buttons):
                estado_boton = button.is_pressed
                # Verifica si ha habido un cambio en el estado del botón
                if estado_boton != estado_anterior[i]:
                    direccion_osc = f"/boton{i + 1}"
                    estado_anterior[i] = estado_boton
                    # Envía un mensaje OSC con el estado actual del botón
                    enviar_mensaje_osc(direccion_osc, int(estado_boton))
            enviar_mensaje_osc("/pot", int(mcp.read_adc(0)))
            time.sleep(0.01)  # Pequeña pausa para evitar lecturas repetidas

    except KeyboardInterrupt:
        pass

# Mapeo de direcciones OSC a la función de manejo
direcciones_osc = ["/ch1", "/ch2", "/ch3"]
for direccion in direcciones_osc:
    dispatcher.map(direccion, manejar_led)

# Inicia los hilos
servidor_thread = threading.Thread(target=servidor.serve_forever)
servidor_thread.start()

leds_thread = threading.Thread(target=controlar_leds)
leds_thread.start()

botones_thread = threading.Thread(target=leer_botones)
botones_thread.start()
