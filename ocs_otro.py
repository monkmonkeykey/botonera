import liblo

# Función de callback para manejar los mensajes OSC recibidos en la ruta "/ruta1"
def callback_ruta1(path, args):
    print(f"Mensaje recibido en {path}: {args}")

# Función de callback para manejar los mensajes OSC recibidos en la ruta "/ruta2"
def callback_ruta2(path, args):
    print(f"Mensaje recibido en {path}: {args}")

# Función de callback para manejar los mensajes OSC recibidos en la ruta "/ruta3"
def callback_ruta3(path, args):
    print(f"Mensaje recibido en {path}: {args}")

# Crea un servidor OSC que escucha en el puerto 12345
server = liblo.Server(12345)

# Asocia las funciones de callback con las rutas OSC específicas
server.add_method("/ruta1", 'i', callback_ruta1)
server.add_method("/ruta2", 'f', callback_ruta2)
server.add_method("/ruta3", 's', callback_ruta3)

print("Esperando mensajes OSC en las rutas /ruta1, /ruta2 y /ruta3...")
while True:
    try:
        server.recv(100)  # Espera por mensajes OSC
    except liblo.ServerError as err:
        print(str(err))
