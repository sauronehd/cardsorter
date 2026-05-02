from asyncio import wait

from ocrfunc import ocr
from picamera2 import Picamera2, Preview
from PIL import Image
import os
import time
import cv2

def wait_for_file(path, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(path) and os.path.getsize(path) > 0:
            return True
        time.sleep(0.1)
    return False


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
wait_for_file("temp.jpg")
image = Image.open("temp.jpg")
#print(image.shape)
img = cv2.imread("image.png", 0)
_, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
cv2.imwrite("thresh.png", thresh)
print(f"The image text is:{ocr(image)}")


