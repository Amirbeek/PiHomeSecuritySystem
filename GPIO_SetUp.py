from gpiozero import MotionSensor, LED
from picamzero import Camera
from signal import pause
import time
import os

# Global Variables
time_motion_started = time.time()
last_time_photo_taken = 0

# Set up GPIO
pir = MotionSensor(4)
led = LED(17)
MOVEMENT_DETECTED_TRESHOLD = 5.0
MIN_DURATION_BETWEEN_PHOTOS = 30.0
CAMERA_FOLDER_PATH = "./src/images_fl"
if not os.path.exists(CAMERA_FOLDER_PATH):
    os.mkdir(CAMERA_FOLDER_PATH)
print("GPIOs setup Done!")

# Set up Camera
camera = Camera()
camera.still_size(1536, 864)
camera.flip_camera(vflip=True, hflip=True)
time.sleep(2)
print("Camera set up Okay!")


def take_photo(camera, folder_path):
    file_name = folder_path + "/img_" + str(time.time()) + ".jpg"
    camera.take_photo(file_name)
    return file_name


def motion_detected():
    global time_motion_started
    print("Starting timer")
    time_motion_started = time.time()
    led.on()


def motion_finished():
    global last_time_photo_taken
    led.off()
    motion_duration = time.time() - time_motion_started
    print(motion_duration)
    if motion_duration > MOVEMENT_DETECTED_TRESHOLD:
        if time.time() - last_time_photo_taken > MIN_DURATION_BETWEEN_PHOTOS:
            last_time_photo_taken = time.time()
            print("Photo is taken And sent to Email!")
            photo_file_name = take_photo(camera, CAMERA_FOLDER_PATH)


pir.when_motion = motion_detected
pir.when_no_motion = motion_finished

pause()
