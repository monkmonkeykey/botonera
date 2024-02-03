import tm1637
from time import sleep

# Configura los pines GPIO utilizados para el display (ajústalos según tus conexiones)
CLK = 20
DIO = 19

# Inicializa el objeto TM1637
display = tm1637.TM1637(clk=CLK, dio=DIO, brightness=1.0)

try:
    # Asigna números a cada dígito
    display.show([1, 2, 3, 4])

    # Espera unos segundos para que puedas ver la asignación
    sleep(5)
except KeyboardInterrupt:
    pass
finally:
    display.cleanup()
