from pythonosc import dispatcher, osc_server

# Define una función para manejar los mensajes OSC
def manejar_mensaje(address, *args):
    print(f"Recibido mensaje desde {address}: {args}")

# Crea un despachador de mensajes OSC
dispatcher = dispatcher.Dispatcher()
dispatcher.map("/ch1", manejar_mensaje)  # Asocia la dirección OSC con la función de manejo

# Configura y corre el servidor OSC
ip_escucha = "0.0.0.0"  # Escucha en todas las interfaces de red
puerto_escucha = 8000   # Puerto en el que escucha el servidor

servidor = osc_server.ThreadingOSCUDPServer((ip_escucha, puerto_escucha), dispatcher)
print(f"Escuchando en {ip_escucha}:{puerto_escucha}")

servidor.serve_forever()
