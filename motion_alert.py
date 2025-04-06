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
import cv2
load_dotenv()

# Global Variables
time_motion_started = time.time()
last_time_photo_taken = 0
MOVEMENT_DETECTED_THRESHOLD = 5.0
MIN_DURATION_BETWEEN_PHOTOS = 30.0
CAMERA_FOLDER_PATH = "/home/pi/Desktop/Lesson_Tasks/GitProject/PiHomeSecuritySystem/src/images_fl"
LOG_FILE_NAME = os.path.join(CAMERA_FOLDER_PATH, "photo_logs.txt")
SENDER_MAIL = os.getenv('MAIN_EMAIL')
RECEIVER_EMAIL = os.getenv('RECEIVER_EMAIL')
password = os.getenv('MAIL_PASSWORD')
class_labels = ['No Human', 'Human']


interpreter = tf.lite.Interpreter(model_path="./model/Human_detection.ipynb")
interpreter.allocate_tensors()
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

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


def preprocess_image(image_path):
    img = Image.open(image_path)
    img = img.resize((224, 224))
    img = np.array(img)
    img = np.expand_dims(img, axis=0)
    img = img.astype(np.float32)
    img = img / 255.0
    return img


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
    global last_time_photo_taken, time_motion_started
    led.off()
    motion_duration = time.time() - time_motion_started
    print(motion_duration)
    if motion_duration > MOVEMENT_DETECTED_THRESHOLD:
        print("In Progress")

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





#
# input_data = preprocess_image(image_path)
#
# # Set the input tensor
# interpreter.set_tensor(input_details[0]['index'], input_data)
#
# # Run inference
# interpreter.invoke()
#
# # Get the output tensor
# output_data = interpreter.get_tensor(output_details[0]['index'])
#
# # Post-process the output (e.g., get the predicted class)
# predicted_class = np.argmax(output_data)
# class_labels = ['No Human', 'Human']  # Adjust these based on your dataset
#
# print(f"The model predicts: {class_labels[predicted_class]}")