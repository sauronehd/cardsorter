import os
import time
import cv2
from PIL import Image
from picamera2 import Picamera2, Preview
import pytesseract

def wait_for_file(path, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(path) and os.path.getsize(path) > 0:
            return True
        time.sleep(0.1)
    return False
#helo
picam2 = Picamera2()
camera_config = picam2.create_still_configuration(
    main={"size": (4608, 2592)}  # Full IMX708 resolution
)
picam2.configure(camera_config)
#picam2.start_preview(Preview.QTGL)
picam2.start()

focused = picam2.autofocus_cycle()
i =0
while not focused:
    print("Tyring to autofoucs")
    focused = picam2.autofocus_cycle()
    i = i + 1
    if i > 10:
        break

print(f"focused is {focused}")

time.sleep(2)
picam2.capture_file("temp.jpg")
wait_for_file("temp.jpg")

# Use consistent filename
img = cv2.imread("temp.jpg", 0)
if img is None:
    print("Image failed to load!")
else:
    _, thresh = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    cv2.imwrite("thresh.png", thresh)

    # Pass the preprocessed image to OCR, not the original
    text = pytesseract.image_to_string(thresh)
    print(f"The image text is: {text}")