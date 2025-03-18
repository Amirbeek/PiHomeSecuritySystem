from flask import Flask
import os

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
                last_photo_file_name = line.rsplit()
        difference = line_counter - previous_line_counter
        previous_line_counter = line_counter
        message = str(difference) + " new photos since you las checked <br/>"
        message += 'Last Photo: ' + last_photo_file_name + '<br/>'
        message += f'<img src="{last_photo_file_name}" />'
        return message
    else:
        return "No Photo Available"


app.run(host="0.0.0.0")