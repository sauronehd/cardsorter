import pytesseract
from PIL import Image
import os
import os
import sys
if os.name == "posix":
    print("Importing pi camera2")
    from picamera2 import Picamera2
else:
    print("Not importing picamera2, quitting")
    sys.exit(1)

try:
    wait = input("Enter to start")
    camera = Picamera2()
    camera.start_and_capture_file("temp.jpg")
    image = Image.open("temp.jpg")
    text = pytesseract.image_to_string(image)
    print(text)
except:
    print("Error, possibly not using linux/pi")