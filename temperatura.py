def obtener_temperatura_cpu():
    try:
        # Abre el archivo que contiene la temperatura de la CPU
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as archivo:
            temperatura = float(archivo.read()) / 1000.0  # Divide por 1000 para obtener la temperatura en grados Celsius
            return temperatura
    except FileNotFoundError:
        return None

# Llama a la función para obtener la temperatura de la CPU
temperatura_actual = obtener_temperatura_cpu()

if temperatura_actual is not None:
    print(f"La temperatura de la CPU es de {temperatura_actual} grados Celsius.")
else:
    print("No se pudo obtener la temperatura de la CPU.")
