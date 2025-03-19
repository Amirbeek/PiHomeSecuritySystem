# PiHomeSecuritySystem

## Overview
PiHomeSecuritySystem is an advanced Raspberry Pi-based security system that leverages real-time motion detection, live video streaming, and immediate email alerts to provide robust home surveillance. This system is accessible via a web interface, allowing users to monitor their home remotely.

## Features
- **Real-Time Motion Detection**: Uses the HC-SR505 motion sensor to detect movement.
- **Email Alerts**: Sends an email with a photo attachment when motion is detected.
- **Live Video Streaming**: Streams live video which can be accessed through the web interface.
- **Local Photo Storage**: Saves photos triggered by motion events locally for later review.

## Hardware Components
- Raspberry Pi 5
- Camera Module (MF130)
- HC-SR505 Motion Sensor
- LEDs for visual indication of system status

## Software Components
- Python for backend logic
- Flask for the web interface
- `dotenv` for environment variable management
- `gpiozero` and `picamera` for interfacing with the hardware
- `yagmail` for sending emails

## Setup
1. **Install Dependencies**:
   ```bash
   pip install Flask gpiozero picamera yagmail python-dotenv
```
2. **Clone the Repository**:
```
git clone https://github.com/Amirbeek/PiHomeSecuritySystem.git
```

3. **Set Environment Variables: Create a .env file in your project root with the following keys**:
```
MAIN_EMAIL=your-email@example.com
RECEIVER_EMAIL=receiver-email@example.com
MAIL_PASSWORD=your-email-password
```

## Running the Project
Navigate to the project directory and run:
```
python app.py
```

## Project Documentation Images
- ![Early stage setup on the breadboard](https://github.com/Amirbeek/PiHomeSecuritySystem/tree/main/progress_images/1.jpg)
- ![Detailed connections of sensors and camera](https://github.com/Amirbeek/PiHomeSecuritySystem/tree/main/progress_images/2.jpg)
- ![Integration of the Raspberry Pi with sensors and camera](https://github.com/Amirbeek/PiHomeSecuritySystem/tree/main/progress_images/3.png)
- ![The HC-SR505 motion sensor in action](https://github.com/Amirbeek/PiHomeSecuritySystem/tree/main/progress_images/motion.png)

## Improvements
- **Enhance Live Streaming**: Implement adaptive bitrate streaming for better performance under varying network conditions.
- **Web Interface Enhancements**: Improve the UI/UX design to make it more user-friendly and visually appealing.
- **Expand Notification Options**: Add support for SMS notifications or integration with mobile apps.

## Contributing
Contributors are welcome to improve the PiHomeSecuritySystem. Here are some areas where you can help:
- Implementing new features such as the suggested improvements.
- Bug fixes and performance enhancements.
- Documentation and examples.

## License
This project is licensed under the MIT License - see the [LICENSE.md](LICENSE) file for details.

## Acknowledgments
Big thanks to everyone who has contributed to this project so far!



