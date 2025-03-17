import lgpio
import time

# GPIO Pins
TRIG = 23  # GPIO 23 (Trigger)
ECHO = 24  # GPIO 24 (Echo)

# Open GPIO chip
h = lgpio.gpiochip_open(0)

# Set up pins
lgpio.gpio_claim_output(h, TRIG)
lgpio.gpio_claim_input(h, ECHO)

def get_distance():
    # Send 10us pulse to trigger
    lgpio.gpio_write(h, TRIG, 1)
    time.sleep(0.00001)
    lgpio.gpio_write(h, TRIG, 0)

    start_time = time.time()
    stop_time = time.time()

    # Wait for echo start
    while lgpio.gpio_read(h, ECHO) == 0:
        start_time = time.time()

    # Wait for echo end
    while lgpio.gpio_read(h, ECHO) == 1:
        stop_time = time.time()

    # Time difference
    elapsed_time = stop_time - start_time

    # Distance calculation (Speed of Sound = 34300 cm/s)
    distance = (elapsed_time * 34300) / 2
    return round(distance, 2)

try:
    while True:
        dist = get_distance()
        print(f"Distance: {dist} cm")
        time.sleep(1)

except KeyboardInterrupt:
    print("Measurement stopped by user")
    lgpio.gpiochip_close(h)
