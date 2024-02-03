from gpiozero import TM1637SevenSegment
from time import sleep

# Define los pines GPIO utilizados para el display (ajústalos según tus conexiones)
tm = TM1637SevenSegment(dio=20, clk=19)

try:
    while True:
        for num in range(10000):
            # Muestra el número en el display
            tm.display(num)
            sleep(0.5)
except KeyboardInterrupt:
    tm.clear()
