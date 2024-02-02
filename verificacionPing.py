import subprocess

def verificar_ping(direccion):
    try:
        # Ejecuta el comando ping
        resultado = subprocess.run(['ping', '-c', '1', direccion], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)

        # Analiza el resultado
        if "1 packets transmitted, 1 received" in resultado.stdout:
            print(f'Ping a {direccion} exitoso.')
            return True
        else:
            print(f'No se recibió respuesta del ping a {direccion}.')
            return False

    except subprocess.CalledProcessError:
        print(f'Error al intentar realizar ping a {direccion}.')
        return False

# Ejemplo de uso
direccion = "192.168.15.4"
verificar_ping(direccion)
