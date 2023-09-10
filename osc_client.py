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
dispatcher.map("ch1", manejar_mensaje_1)
dispatcher.map("ch2", manejar_mensaje_2)
dispatcher.map("ch3", manejar_mensaje_3)

# Configura y corre el servidor OSC
ip_escucha = "192.168.15.7"  # Escucha en todas las interfaces de red
puerto_escucha = 9000   # Puerto en el que escucha el servidor

servidor = osc_server.ThreadingOSCUDPServer((ip_escucha, puerto_escucha), dispatcher)
print(f"Escuchando en {ip_escucha}:{puerto_escucha}")

servidor.serve_forever()
