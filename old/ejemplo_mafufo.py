import board
import busio
import digitalio
import adafruit_tlc5947
from pythonosc import udp_client
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer

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
    target_volume = args[0]

# Create a dispatcher to map OSC addresses to callback functions
dispatcher = Dispatcher()
dispatcher.map("/volume", handle_volume)

# Create an OSC server to receive messages
server = BlockingOSCUDPServer(("0.0.0.0", 12345), dispatcher)  # Adjust IP and port as needed

# Define the initial volume variable
volume = 0.0
target_volume = 0.0

# Create PWMOut objects for each LED
leds = [tlc5947.create_pwm_out(i) for i in range(NUM_LEDS)]

while True:
    #print(target_volume)
    if  target_volume == 0.0:
        leds[0].duty_cycle = MIN_PWM
        leds[1].duty_cycle = MIN_PWM
        leds[2].duty_cycle = MIN_PWM
        leds[3].duty_cycle = MIN_PWM
        leds[4].duty_cycle = MIN_PWM
        leds[5].duty_cycle = MIN_PWM
        leds[6].duty_cycle = MIN_PWM
        leds[7].duty_cycle = MIN_PWM
        leds[8].duty_cycle = MIN_PWM
        leds[9].duty_cycle = MIN_PWM
    elif  0.1 < target_volume < 0.2:
        leds[0].duty_cycle = MAX_PWM
        leds[1].duty_cycle = MIN_PWM
        leds[2].duty_cycle = MIN_PWM
        leds[3].duty_cycle = MIN_PWM
        leds[4].duty_cycle = MIN_PWM
        leds[5].duty_cycle = MIN_PWM
        leds[6].duty_cycle = MIN_PWM
        leds[7].duty_cycle = MIN_PWM
        leds[8].duty_cycle = MIN_PWM
        leds[9].duty_cycle = MIN_PWM
        
    elif 0.2 < target_volume < 0.3:
        leds[0].duty_cycle = MAX_PWM
        leds[1].duty_cycle = MAX_PWM
        leds[2].duty_cycle = MIN_PWM
        leds[3].duty_cycle = MIN_PWM
        leds[4].duty_cycle = MIN_PWM
        leds[5].duty_cycle = MIN_PWM
        leds[6].duty_cycle = MIN_PWM
        leds[7].duty_cycle = MIN_PWM
        leds[8].duty_cycle = MIN_PWM
        leds[9].duty_cycle = MIN_PWM
    elif 0.3 < target_volume < 0.4:
        leds[0].duty_cycle = MAX_PWM
        leds[1].duty_cycle = MAX_PWM
        leds[2].duty_cycle = MAX_PWM
        leds[3].duty_cycle = MIN_PWM
        leds[4].duty_cycle = MIN_PWM
        leds[5].duty_cycle = MIN_PWM
        leds[6].duty_cycle = MIN_PWM
        leds[7].duty_cycle = MIN_PWM
        leds[8].duty_cycle = MIN_PWM
        leds[9].duty_cycle = MIN_PWM  
    elif 0.4 < target_volume < 0.5:
        leds[0].duty_cycle = MAX_PWM
        leds[1].duty_cycle = MAX_PWM
        leds[2].duty_cycle = MAX_PWM
        leds[3].duty_cycle = MAX_PWM
        leds[4].duty_cycle = MIN_PWM
        leds[5].duty_cycle = MIN_PWM
        leds[6].duty_cycle = MIN_PWM
        leds[7].duty_cycle = MIN_PWM
        leds[8].duty_cycle = MIN_PWM
        leds[9].duty_cycle = MIN_PWM
    elif 0.5 < target_volume < 0.6:
        leds[0].duty_cycle = MAX_PWM
        leds[1].duty_cycle = MAX_PWM
        leds[2].duty_cycle = MAX_PWM
        leds[3].duty_cycle = MAX_PWM
        leds[4].duty_cycle = MAX_PWM
        leds[5].duty_cycle = MIN_PWM
        leds[6].duty_cycle = MIN_PWM
        leds[7].duty_cycle = MIN_PWM
        leds[8].duty_cycle = MIN_PWM
        leds[9].duty_cycle = MIN_PWM
    elif 0.6 < target_volume < 0.7:
        leds[0].duty_cycle = MAX_PWM
        leds[1].duty_cycle = MAX_PWM
        leds[2].duty_cycle = MAX_PWM
        leds[3].duty_cycle = MAX_PWM
        leds[4].duty_cycle = MAX_PWM
        leds[5].duty_cycle = MAX_PWM
        leds[6].duty_cycle = MIN_PWM
        leds[7].duty_cycle = MIN_PWM
        leds[8].duty_cycle = MIN_PWM
        leds[9].duty_cycle = MIN_PWM
    elif 0.7 < target_volume < 0.8:
        leds[0].duty_cycle = MAX_PWM
        leds[1].duty_cycle = MAX_PWM
        leds[2].duty_cycle = MAX_PWM
        leds[3].duty_cycle = MAX_PWM
        leds[4].duty_cycle = MAX_PWM
        leds[5].duty_cycle = MAX_PWM
        leds[6].duty_cycle = MAX_PWM
        leds[7].duty_cycle = MIN_PWM
        leds[8].duty_cycle = MIN_PWM
        leds[9].duty_cycle = MIN_PWM  
    elif 0.8 < target_volume < 0.9:
        leds[0].duty_cycle = MAX_PWM
        leds[1].duty_cycle = MAX_PWM
        leds[2].duty_cycle = MAX_PWM
        leds[3].duty_cycle = MAX_PWM
        leds[4].duty_cycle = MAX_PWM
        leds[5].duty_cycle = MAX_PWM
        leds[6].duty_cycle = MAX_PWM
        leds[7].duty_cycle = MAX_PWM
        leds[8].duty_cycle = MIN_PWM
        leds[9].duty_cycle = MIN_PWM
    elif 0.9 < target_volume < 1:
        leds[0].duty_cycle = MAX_PWM
        leds[1].duty_cycle = MAX_PWM
        leds[2].duty_cycle = MAX_PWM
        leds[3].duty_cycle = MAX_PWM
        leds[4].duty_cycle = MAX_PWM
        leds[5].duty_cycle = MAX_PWM
        leds[6].duty_cycle = MAX_PWM
        leds[7].duty_cycle = MAX_PWM
        leds[8].duty_cycle = MAX_PWM
        leds[9].duty_cycle = MAX_PWM
        
    '''
    # Gradually adjust the volume towards the target volume
    volume += (target_volume - volume) * 0.1

    # Calculate the number of LEDs to light up based on the volume
    num_leds_to_light = int(volume * NUM_LEDS)

    # Turn off all LEDs
    for led in leds:
        led.duty_cycle = MIN_PWM

    # Turn on LEDs up to num_leds_to_light
    for i in range(num_leds_to_light):
        leds[i].duty_cycle = MAX_PWM

    # Write the changes to the TLC5947
    tlc5947.write()

    # Handle incoming OSC messages
    
    '''
    server.handle_request()
