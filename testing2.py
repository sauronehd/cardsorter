from ocrfunc import ocr
from picamera2 import Picamera2, Preview
from PIL import Image
import time
import cv2
picam2 = Picamera2()
camera_config = picam2.create_preview_configuration()
picam2.configure(camera_config)
picam2.start_preview(Preview.QTGL)
picam2.start()
focused = picam2.autofocus_cycle()
while not focused:
    focused = picam2.autofocus_cycle()
print(f"focused is {focused}")
time.sleep(2)
picam2.capture_file("temp.jpg")

image = Image.open("temp.jpg")
#print(image.shape)
img = cv2.imread("image.png", 0)
_, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imwrite("thresh.png", thresh)
print(f"The image text is:{ocr(image)}")
