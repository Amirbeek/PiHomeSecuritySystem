from flask import Flask, send_from_directory
import os

# Path to the folder containing images
CAMERA_FOLDER_PATH = "/home/pi/Desktop/Lesson_Tasks/GitProject/PiHomeSecuritySystem/src/images_fl"
LOG_FILE_NAME = "/home/pi/Desktop/Lesson_Tasks/GitProject/PiHomeSecuritySystem/src/images_fl/photo_logs.txt"

# Flask app setup to serve images from the given folder
app = Flask(__name__, static_url_path=CAMERA_FOLDER_PATH, static_folder=CAMERA_FOLDER_PATH)

previous_line_counter = 0


@app.route("/")
def index():
    return "Hello"


@app.route('/check_photos')
def check_photos():
    global previous_line_counter
    line_counter = 0
    print(os.path.exists(LOG_FILE_NAME))
    if os.path.exists(LOG_FILE_NAME):
        last_photo_file_name = ''
        with open(LOG_FILE_NAME, "r") as f:
            for line in f:
                line_counter += 1
                last_photo_file_name = line.strip()
        difference = line_counter - previous_line_counter
        previous_line_counter = line_counter

        message = str(difference) + " new photos since you last checked <br/>"
        message += 'Last Photo: ' + last_photo_file_name + '<br/>'
        print(last_photo_file_name)
        # Directly reference the image file using the URL path
        message += "<img src=\"" + last_photo_file_name + "\" />"
        return message
    else:
        return "No Photo Available"


# Serve the image directly from the images folder
@app.route('/images/<filename>')
def send_photo(filename):
    return send_from_directory(CAMERA_FOLDER_PATH, filename)


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)

