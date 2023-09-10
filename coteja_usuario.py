import paramiko

# Dirección IP del dispositivo al que te quieres conectar
ip_dispositivo = "192.168.15.28"  # Reemplaza con la dirección IP del dispositivo

# Credenciales de inicio de sesión
nombre_usuario = "pi"    # Reemplaza con tu nombre de usuario
contraseña = "mono"     # Reemplaza con tu contraseña

# Crea una instancia del cliente SSH
cliente_ssh = paramiko.SSHClient()

# Establece la política de seguridad para aceptar automáticamente la clave del servidor
cliente_ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

try:
    # Conéctate al dispositivo
    cliente_ssh.connect(ip_dispositivo, username=nombre_usuario, password=contraseña)

    # Abre una conexión SSH y ejecuta un comando para obtener el nombre de usuario
    stdin, stdout, stderr = cliente_ssh.exec_command("whoami")

    # Lee la salida del comando
    nombre_usuario_resultado = stdout.read().decode().strip()

    print(f"El nombre de usuario en el dispositivo {ip_dispositivo} es: {nombre_usuario_resultado}")

except paramiko.AuthenticationException:
    print("Error de autenticación. Comprueba las credenciales.")
except paramiko.SSHException as e:
    print(f"Error de SSH: {e}")
except Exception as e:
    print(f"Error: {e}")
finally:
    # Cierra la conexión SSH
    cliente_ssh.close()
