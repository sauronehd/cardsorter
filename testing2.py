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

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(
    main={"size": (4608, 2592)}
)
picam2.configure(camera_config)
picam2.start()
#force push
# Let camera warm up and apply controls
picam2.set_controls({
    "ExposureTime": 10000,  # 1/100 sec
    "Sharpness": 2.0,
    "Contrast": 1.2
})
time.sleep(1)  # Let controls settle

# Autofocus
for i in range(10):
    if picam2.autofocus_cycle():
        print("Autofocus succeeded")
        break
    print(f"Autofocus attempt {i+1} failed, retrying...")
else:
    print("Autofocus failed after 10 attempts, continuing anyway")

time.sleep(2)
picam2.capture_file("temp.jpg")
wait_for_file("temp.jpg")

# Preprocessing and OCR
img = cv2.imread("temp.jpg")
if img is None:
    print("Image failed to load!")
else:
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Crop out dark bands top/bottom and edges
    h, w = gray.shape
    gray = gray[int(h * 0.75):int(h * 0.88), int(w * 0.08):int(w * 0.55)]
    # CLAHE to normalize uneven lighting
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    gray = clahe.apply(gray)

    # Adaptive threshold - handles local lighting variation
    thresh = cv2.adaptiveThreshold(
        gray, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31,  # block size
        10   # constant subtracted from mean
    )

    cv2.imwrite("thresh.png", thresh)

    # OCR with better config
    text = pytesseract.image_to_string(thresh, config="--psm 6")
    print(f"OCR result:\n{text}")