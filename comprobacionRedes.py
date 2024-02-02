import subprocess

def is_spi_initialized():
    try:
        lsmod_output = subprocess.check_output(['lsmod'], text=True)
        return 'spi_bcm2835' in lsmod_output
    except subprocess.CalledProcessError:
        return False

def check_ssh():
    try:
        subprocess.run(["systemctl", "is-active", "ssh"], check=True)
        return True
    except subprocess.CalledProcessError:
        return False

# Verificar si el servicio SPI está inicializado
if is_spi_initialized():
    print("El servicio SPI está inicializado en la Raspberry Pi.")

    # Intentar comprobar hasta que el servicio SSH esté activo
    while not check_ssh():
        print("Esperando que el servicio SSH se active...")
        time.sleep(5)  # Espera 5 segundos antes de volver a verificar

    print("El servicio SSH está activo. Continuando con el programa.")
else:
    print("El servicio SPI no está inicializado en la Raspberry Pi.")
