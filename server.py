import threading

from flask import Flask
import os
from motion_alert import start_motion_detection

CAMERA_FOLDER_PATH = "./src/images_fl"
LOG_FILE_NAME = os.path.join(CAMERA_FOLDER_PATH, "photo_logs.txt")
app = Flask(__name__, static_url_path=CAMERA_FOLDER_PATH, static_folder=CAMERA_FOLDER_PATH)
previous_line_counter = 0


@app.route("/")
def index():
    return "Hello"


@app.route('/check_photos')
def check_photos():
    global previous_line_counter
    line_counter = 0
    if os.path.exists(LOG_FILE_NAME):
        last_photo_file_name = ''
        with open(LOG_FILE_NAME, "r") as f:
            for line in f:
                line_counter += 1
                last_photo_file_name = line.strip()
        difference = line_counter - previous_line_counter
        previous_line_counter = line_counter
        message = f"{difference} new photos since you last checked <br/>"
        message += f'Last Photo: {last_photo_file_name}<br/>'
        message += f'<img src="{last_photo_file_name}" />'
        return message
    else:
        return "No Photo Available"


def run_motion_detection():
    start_motion_detection()


if __name__ == "__main__":
    detector_thread = threading.Thread(target=run_motion_detection)
    detector_thread.start()
    app.run(host="0.0.0.0", use_reloader=False)
