import neopixel
import board

def configurar_brillo(pixels, brillo, color):
    """
    Configura el brillo de NeoPixels.

    Args:
        pixels: Objeto NeoPixel.
        brillo: Nivel de brillo deseado (0 a 255).
        color: Color deseado en formato (R, G, B).
    """
    color_atenuado = tuple(int(c * (brillo / 110)) for c in color)
    pixels.fill(color_atenuado)
    pixels.show()

# Configura el número de NeoPixels y el pin de datos
NUM_PIXELS = 16
PIN = board.D18

# Crea un objeto NeoPixel
pixels = neopixel.NeoPixel(PIN, NUM_PIXELS)

# Define el nivel de brillo deseado y el color
brillo = 128  # Puedes ajustar este valor según tu preferencia
color = (255, 0, 0)  # Por ejemplo, rojo

# Llama a la función para configurar el brillo de los NeoPixels
configurar_brillo(pixels, brillo, color)
