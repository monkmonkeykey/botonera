import threading
from pythonosc import dispatcher, osc_server

# Define funciones para manejar los mensajes OSC
def manejar_mensaje_1(address, *args):
    print(f"Recibido mensaje desde {address}: {args}")

def manejar_mensaje_2(address, *args):
    print(f"Recibido mensaje desde {address}: {args}")

def manejar_mensaje_3(address, *args):
    print(f"Recibido mensaje desde {address}: {args}")

# Crea un despachador de mensajes OSC
dispatcher = dispatcher.Dispatcher()

# Asocia las direcciones OSC con las funciones de manejo
dispatcher.map("/ch1", manejar_mensaje_1)
dispatcher.map("/ch2", manejar_mensaje_2)
dispatcher.map("/ch3", manejar_mensaje_3)

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