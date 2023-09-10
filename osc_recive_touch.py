import threading
from pythonosc import dispatcher, osc_server


# Configurar pines GPIO para los LEDs


# Define funciones para manejar los mensajes OSC y controlar los LEDs
def manejar_led(address, *args):
    print(f"Recibido mensaje desde {address}: {args}")
    pin = None
    if address == "/ch1":
        print(f"{address}: {args}")
    elif address == "/ch2":
        # El valor flotante recibido controlará el ciclo de trabajo del PWM
        print(f"{address}: {args}")
    elif address == "/ch3":
        print(f"{address}: {args}")
    if pin is not None:
        print("no pasa nada oiga")

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
