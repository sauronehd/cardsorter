from ocrfunc import ocr
from picamera2 import Picamera2
from PIL import Image


camera = Picamera2()
camera.start_and_capture_file("temp.jpg")
image = Image.open("temp.jpg")
print(f"The image text is:{ocr(image)}")
