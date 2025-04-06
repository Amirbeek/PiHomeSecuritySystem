from gpiozero import MotionSensor, LED
from dotenv import load_dotenv
from picamzero import Camera
from signal import pause
import yagmail
import time
import os
import tensorflow as tf
import numpy as np
from PIL import Image
from datetime import datetime

load_dotenv()

# Global Variables
time_motion_started = time.time()
last_time_photo_taken = 0
MOVEMENT_DETECTED_THRESHOLD = 5.0  # Seconds
MIN_DURATION_BETWEEN_PHOTOS = 30.0  # Seconds
CAMERA_FOLDER_PATH = "/home/pi/Desktop/Lesson_Tasks/GitProject/PiHomeSecuritySystem/src/images_fl"
LOG_FILE_NAME = os.path.join(CAMERA_FOLDER_PATH, "photo_logs.txt")
SENDER_MAIL = os.getenv('MAIN_EMAIL')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
password = os.getenv('MAIL_PASSWORD')
class_labels = ['No Human', 'Human']

# Load TFLite model
interpreter = tf.lite.Interpreter(model_path="./model/human_detection_model.tflite")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# Set up GPIO
pir = MotionSensor(4)
led = LED(17)

# Ensure image folder exists
if not os.path.exists(CAMERA_FOLDER_PATH):
    os.makedirs(CAMERA_FOLDER_PATH)
print("GPIOs setup Done!")

# Remove old log file
if os.path.exists(LOG_FILE_NAME):
    os.remove(LOG_FILE_NAME)
    print("Previous log file removed")

# Set up Camera
camera = Camera()
camera.still_size = (1536, 864)
camera.flip_camera(vflip=True, hflip=True)
time.sleep(2)
print("Camera set up Okay!")

# Set up email client
yag = yagmail.SMTP(SENDER_MAIL, password)
print('EMAIL Set Up OKAY!')


def blink_led(times=3, delay=0.2):
    for _ in range(times):
        led.on()
        time.sleep(delay)
        led.off()
        time.sleep(delay)


def take_photo(camera, folder_path):
    file_name = os.path.join(folder_path, "img_" + str(time.time()) + ".jpg")
    camera.take_photo(file_name)
    return file_name


def preprocess_image(image_path):
    img = Image.open(image_path).convert('RGB')
    img = img.resize((224, 224))
    img = np.array(img).astype(np.float32) / 255.0
    img = np.expand_dims(img, axis=0)
    return img


def send_photo_by_email(yagmail_client, file_name):
    yagmail_client.send(
        to=RECEIVER_EMAIL,
        subject='New Photo From Your House',
        contents="Check out the new photo 📷",
        attachments=file_name
    )


def update_photo_log_file(log_file_name, file_name, label):
    with open(log_file_name, "a") as f:
        f.write(f"{datetime.now()} - {file_name} - {label}\n")


def motion_detected():
    global time_motion_started
    print("Motion detected. Starting timer.")
    time_motion_started = time.time()
    blink_led()


def motion_finished():
    global last_time_photo_taken, time_motion_started
    led.off()
    motion_duration = time.time() - time_motion_started
    print(f"Motion ended. Duration: {motion_duration:.2f} seconds")

    if motion_duration > MOVEMENT_DETECTED_THRESHOLD:
        print("Motion duration exceeded threshold. Processing...")

        if time.time() - last_time_photo_taken > MIN_DURATION_BETWEEN_PHOTOS:
            last_time_photo_taken = time.time()
            photo_file_name = take_photo(camera, CAMERA_FOLDER_PATH)
            print(f"Photo taken: {photo_file_name}")

            input_data = preprocess_image(photo_file_name)
            interpreter.set_tensor(input_details[0]['index'], input_data)
            interpreter.invoke()
            output_data = interpreter.get_tensor(output_details[0]['index'])
            predicted_class = np.argmax(output_data)
            prediction_label = class_labels[predicted_class]
            print(f"Model Prediction: {prediction_label}")

            update_photo_log_file(LOG_FILE_NAME, photo_file_name, prediction_label)

            if prediction_label == 'Human':
                print("Human detected. Sending email...")
                send_photo_by_email(yag, photo_file_name)
            else:
                print("No human detected. Email not sent.")


# Motion detection callbacks
pir.when_motion = motion_detected
pir.when_no_motion = motion_finished

print("System is ready and running. Waiting for motion...")
pause()
