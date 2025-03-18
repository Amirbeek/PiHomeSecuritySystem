from gpiozero import MotionSensor, LED
from signal import pause
import time

# Global Variables
time_motion_started = time.time()

# Set up GPIO
pir = MotionSensor(4)
led = LED(17)
print("GPIOs setup Done!")


def motion_detected():
    print("Starting timer")
    global time_motion_started
    time_motion_started = time.time()
    led.on()


def motion_finished():
    led.off()
    motion_duration = time.time() - time_motion_started
    print(motion_duration)
    if motion_duration > 5.0:
        print('Taking a photo and selling it by email')


pir.when_motion = motion_detected()
pir.when_no_motion = motion_finished()

pause()
