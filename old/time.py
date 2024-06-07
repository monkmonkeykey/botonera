import time

while True:
    # Obtiene el tiempo en segundos en el momento en que se inicia el programa
    tiempo_inicio = time.time()

    # Realiza algunas tareas o ejecuta tu programa aquí
    # Por ejemplo, vamos a esperar 5 segundos antes de imprimir el tiempo transcurrido
    time.sleep(1)

    # Calcula el tiempo transcurrido desde el inicio del programa en segundos
    tiempo_transcurrido = time.time() - tiempo_inicio

    print("Tiempo transcurrido desde el inicio del programa en segundos:", tiempo_transcurrido)
