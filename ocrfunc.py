import pytesseract
from PIL import Image
from picamera2 import Picamera2


try:
    wait = input("Enter to start")
    camera = Picamera2()
    camera.start_and_capture_file("temp.jpg")
    image = Image.open("temp.jpg")
    text = pytesseract.image_to_string(image)
    print(text)
except:
    print("Error, possibly not using linux/pi")