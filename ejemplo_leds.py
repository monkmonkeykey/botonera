import board
import neopixel

# Configura los NeoPixels
pixels = neopixel.NeoPixel(board.D18, 8)

def mapear(valor, inicioRango1, finRango1, inicioRango2, finRango2):
    # Calcula la proporción en la que valor está dentro del primer rango
    proporcion = (valor - inicioRango1) / (finRango1 - inicioRango1)

    # Mapea esa proporción al segundo rango
    valorMapeado = inicioRango2 + proporcion * (finRango2 - inicioRango2)

    return valorMapeado

valor = 5
inicioRango1 = 7
finRango1 = 1023
inicioRango2 = 0
finRango2 = 255




while True:
    valorMapeado = mapear(valor, inicioRango1, finRango1, inicioRango2, finRango2)
    print(valorMapeado)  # Esto imprimirá el valor mapeado
    # Establece el primer píxel en rojo y el segundo en verde
    pixels[0] = (255, 0, 0)
    pixels[1] = (0, 255, 0)
    
    # Actualiza los NeoPixels para reflejar los cambios
    pixels.show()


