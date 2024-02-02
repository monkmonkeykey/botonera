import subprocess
import time
programa_a_ejecutar = "/home/pi/PowerRoom/botonera2024.py"
def check_ssh():
    try:
        subprocess.run(["systemctl", "is-active", "ssh"], check=True)
        
        return True
    except subprocess.CalledProcessError:
        return False

# Intentar comprobar hasta que el servicio SSH esté activo
while not check_ssh():
    print("Esperando que el servicio SSH se active...")
    time.sleep(5)  # Espera 5 segundos antes de volver a verificar

print("El servicio SSH está activo. Continuando con el programa.")




import subprocess




def check_ssh():
    try:
        subprocess.run(["systemctl", "is-active", "ssh"], check=True)
        print("El servicio SSH está activo.")
        # Ejecuta el programa
        
    except subprocess.CalledProcessError:
        print("El servicio SSH no está activo.")

def check_ping(host="8.8.8.8"):
    try:
        subprocess.run(["ping", "-c", "1", host], check=True)
        print(f"Se pudo hacer ping a {host}.")
    except subprocess.CalledProcessError:
        print(f"No se pudo hacer ping a {host}.")

# Ejemplo de uso
check_ssh()
check_ping()
