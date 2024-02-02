import subprocess
import time
programa_a_ejecutar = "/home/pi/PowerRoom/botonera/botones2024.py"
def check_ssh():
    try:
        subprocess.run(["systemctl", "is-active", "ssh"], check=True)
        subprocess.run(["python", programa_a_ejecutar])
        return True
    except subprocess.CalledProcessError:
        return False

# Intentar comprobar hasta que el servicio SSH esté activo
while not check_ssh():
    print("Esperando que el servicio SSH se active...")
    time.sleep(5)  # Espera 5 segundos antes de volver a verificar

print("El servicio SSH está activo. Continuando con el programa.")

