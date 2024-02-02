import os
import time

def is_spi_active():
    spi_path = "/sys/class/spi_master/"
    return any(os.path.isdir(os.path.join(spi_path, d)) for d in os.listdir(spi_path))

def check_ssh():
    try:
        subprocess.run(["systemctl", "is-active", "ssh"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Verificar si el servicio SPI está activo
if is_spi_active():
    print("El servicio SPI está activo en la Raspberry Pi.")

    # Intentar comprobar hasta que el servicio SSH esté activo
    while not check_ssh():
        print("Esperando que el servicio SSH se active...")
        time.sleep(5)  # Espera 5 segundos antes de volver a verificar

    print("El servicio SSH está activo. Continuando con el programa.")
else:
    print("El servicio SPI no está activo en la Raspberry Pi.")
