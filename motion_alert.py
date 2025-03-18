from gpiozero import MotionSensor, LED
from dotenv import load_dotenv
from picamzero import Camera
from signal import pause
import yagmail
import time
import os

def start_motion_detection():
    load_dotenv()

    # Global Variables
    time_motion_started = time.time()
    last_time_photo_taken = 0
    MOVEMENT_DETECTED_TRESHOLD = 5.0
    MIN_DURATION_BETWEEN_PHOTOS = 30.0
    CAMERA_FOLDER_PATH = "./src/images_fl"
    LOG_FILE_NAME = os.path.join(CAMERA_FOLDER_PATH, "photo_logs.txt")
    SENDER_MAIL = os.getenv('MAIN_EMAIL')
    RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
    password = os.getenv('MAIL_PASSWORD')

    # Set up GPIO
    pir = MotionSensor(4)
    led = LED(17)

    if not os.path.exists(CAMERA_FOLDER_PATH):
        os.makedirs(CAMERA_FOLDER_PATH)
    print("GPIOs setup Done!")

    # Remove log file
    if os.path.exists(LOG_FILE_NAME):
        os.remove(LOG_FILE_NAME)
        print("Previous file is removed")

    # Set up Camera
    camera = Camera()
    camera.still_size = (1536, 864)
    camera.flip_camera(vflip=True, hflip=True)
    time.sleep(2)
    print("Camera set up Okay!")

    yag = yagmail.SMTP(SENDER_MAIL, password)
    print('EMAIL Set Up OKAY!')

    def take_photo(camera, folder_path):
        file_name = os.path.join(folder_path, "img_" + str(time.time()) + ".jpg")
        camera.take_photo(file_name)
        return file_name

    def send_photo_by_email(yagmail_client, file_name):
        yagmail_client.send(to=RECEIVER_EMAIL, subject='New Photo From Your House', contents="Check out the new photo",
                            attachments=file_name)

    def update_photo_log_file(log_file_name, file_name):
        with open(log_file_name, "a") as f:
            f.write(file_name + "\n")

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
                update_photo_log_file(log_file_name=LOG_FILE_NAME, file_name=photo_file_name)
                send_photo_by_email(yag, photo_file_name)

    pir.when_motion = motion_detected
    pir.when_no_motion = motion_finished
    print("Everything is set up")
    pause()

