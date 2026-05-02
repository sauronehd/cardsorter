from ocrfunc import ocr
from picamera2 import Picamera2, Preview
from PIL import Image
import time

picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
focused = picam2.autofocus_cycle()
while not focused:
    focused = picam2.autofocus_cycle()

time.sleep(2)
picam2.capture_file("temp.jpg")

image = Image.open("temp.jpg")
#print(image.shape)
print(f"The image text is:{ocr(image)}")
