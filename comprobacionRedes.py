import subprocess

def check_ssh():
    try:
        subprocess.run(["systemctl", "is-active", "ssh"], check=True)
        print("El servicio SSH está activo.")
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
