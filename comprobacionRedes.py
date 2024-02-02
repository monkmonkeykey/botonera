import subprocess
import time

import subprocess
import time
programa_a_ejecutar = "/home/pi/PowerRoom/botonera/botones2024.py"
def is_spi_enabled():
    try:
        with open('/boot/config.txt', 'r') as config_file:
            config_content = config_file.read()
            return 'dtparam=spi=on' in config_content
    except FileNotFoundError:
        return False

def check_ssh():
    try:
        subprocess.run(["systemctl", "is-active", "ssh"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Verificar si SPI está habilitado
if is_spi_enabled():
    print("SPI está habilitado en la Raspberry Pi.")
    subprocess.run(["python", programa_a_ejecutar])
    # Intentar comprobar hasta que el servicio SSH esté activo
    while not check_ssh():
        print("Esperando que el servicio SSH se active...")
        time.sleep(5)  # Espera 5 segundos antes de volver a verificar

    print("El servicio SSH está activo. Continuando con el programa.")
else:
    print("SPI no está habilitado en la Raspberry Pi.")

