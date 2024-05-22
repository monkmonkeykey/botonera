import board
import busio
import digitalio
import adafruit_tlc5947
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import ThreadingOSCUDPServer
import threading

# Define pins connected to the TLC5947
SCK = board.SCK
MOSI = board.MOSI
LATCH = digitalio.DigitalInOut(board.D21)

# Initialize SPI bus.
spi = busio.SPI(clock=SCK, MOSI=MOSI)

# Initialize TLC5947
tlc5947 = adafruit_tlc5947.TLC5947(spi, LATCH)

# Define maximum and minimum PWM values
MAX_PWM = 30000
MIN_PWM = 0

# Define number of LEDs
NUM_LEDS = 10

# Create an OSC client
osc_client = udp_client.SimpleUDPClient("127.0.0.1", 12345)  # Adjust IP and port as needed

# Define a callback function to handle incoming OSC messages
def handle_volume(address, *args):
    global target_volume
    # Limitar el valor de target_volume dentro del rango de 0 a 1
    target_volume = max(0.0, min(1.0, args[0]))

# Create a dispatcher to map OSC addresses to callback functions
dispatcher = Dispatcher()
dispatcher.map("/volume", handle_volume)

# Create an OSC server to receive messages
server = ThreadingOSCUDPServer(("0.0.0.0", 12345), dispatcher)  # Adjust IP and port as needed

# Define the initial volume variable
volume = 0.0
target_volume = 0.0

# Create PWMOut objects for each LED
leds = [tlc5947.create_pwm_out(i) for i in range(NUM_LEDS)]

# Function to update LEDs based on target volume
def update_leds(target_volume):
    if target_volume == 0.0:
        for led in leds:
            led.duty_cycle = MIN_PWM
    else:
        num_leds_to_light = min(int(target_volume * NUM_LEDS), NUM_LEDS)  # Asegurar que num_leds_to_light no exceda NUM_LEDS
        for i in range(num_leds_to_light):
            leds[i].duty_cycle = MAX_PWM
        for i in range(num_leds_to_light, NUM_LEDS):
            leds[i].duty_cycle = MIN_PWM
    # Write changes to TLC5947
    tlc5947.write()

# Function to run the OSC server in a separate thread
def run_server():
    server.serve_forever()

# Start the OSC server in a separate thread
server_thread = threading.Thread(target=run_server)
server_thread.start()

# Main loop
try:
    while True:
        update_leds(target_volume)
except KeyboardInterrupt:
    # Shutdown OSC server and join server thread
    server.shutdown()
    server_thread.join()
