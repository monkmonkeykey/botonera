import paramiko
import socket
import time

# Credenciales de inicio de sesión
nombre_usuario = "pi"    # Reemplaza con tu nombre de usuario
contraseña = "mono"     # Reemplaza con tu contraseña

# Rango de direcciones IP a escanear
mascara_subred = "192.168.15."
inicio_rango = 1
fin_rango = 10  # Cambia el valor según el rango de direcciones IP que desees probar

# Tiempo de espera en segundos
timeout_segundos = 0.2

# Crea una instancia del cliente SSH
cliente_ssh = paramiko.SSHClient()

# Establece la política de seguridad para aceptar automáticamente la clave del servidor
cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

# Bucle para intentar conectarse a diferentes direcciones IP
for i in range(inicio_rango, fin_rango + 1):
    ip_dispositivo = f"{mascara_subred}{i}"

    try:
        # Conéctate al dispositivo con un tiempo de espera
        cliente_ssh.connect(ip_dispositivo, username=nombre_usuario, password=contraseña, timeout=timeout_segundos)

        # Abre una conexión SSH y ejecuta un comando para obtener el nombre de usuario
        stdin, stdout, stderr = cliente_ssh.exec_command("whoami")

        # Lee la salida del comando
        nombre_usuario_resultado = stdout.read().decode().strip()

        print(f"Conexión exitosa a {ip_dispositivo}. Nombre de usuario: {nombre_usuario_resultado}")
        break  # Sale del bucle si la conexión es exitosa

    except paramiko.AuthenticationException:
        print(f"Fallo de autenticación para {ip_dispositivo}. Comprobando siguiente dirección.")
    except paramiko.SSHException as e:
        print(f"Fallo de SSH para {ip_dispositivo}: {e}. Comprobando siguiente dirección.")
    except socket.timeout:
        print(f"Tiempo de espera agotado para {ip_dispositivo}. Comprobando siguiente dirección.")
    except Exception as e:
        print(f"Error al intentar conectar a {ip_dispositivo}: {e}. Comprobando siguiente dirección.")
    finally:
        # Cierra la conexión SSH (si se estableció)
        if cliente_ssh.get_transport() is not None:
            cliente_ssh.close()
        # Espera un breve período antes de intentar la siguiente conexión
        time.sleep(1)
