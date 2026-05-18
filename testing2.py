import os
import time
import cv2
from picamera2 import Picamera2
import pytesseract

def wait_for_file(path, timeout=5):
    start = time.time()
    while time.time() - start < timeout:
        if os.path.exists(path) and os.path.getsize(path) > 0:
            return True
        time.sleep(0.1)
    return False

picam2 = Picamera2()
camera_config = picam2.create_still_configuration(main={"size": (4608, 2592)})
picam2.configure(camera_config)
picam2.start()

picam2.set_controls({
    "ExposureTime": 10000,
    "Sharpness": 2.0,
    "Contrast": 1.2
})
time.sleep(1)

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

img = cv2.imread("temp.jpg")
if img is None:
    print("Image failed to load!")
else:
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # --- Crop: save the raw crop first to verify framing ---
    h, w = gray.shape
    crop = gray[int(h * 0.5):int(h * 0.6), int(w * 0.3):int(w * 0.5)]
    cv2.imwrite("debug_crop.png", crop)  # inspect this first!

    # Upscale 2x before processing
    crop = cv2.resize(crop, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Denoise BEFORE thresholding
    denoised = cv2.fastNlMeansDenoising(crop, h=20)

    # CLAHE for uneven lighting
    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    equalized = clahe.apply(denoised)

    # Threshold
    thresh = cv2.adaptiveThreshold(
        equalized, 255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY,
        31, 10
    )

    # Invert if background is dark (check mean pixel value)
    if cv2.mean(thresh)[0] < 127:
        thresh = cv2.bitwise_not(thresh)

    cv2.imwrite("thresh.png", thresh)

    # Single line mode since it's a title/banner
    text = pytesseract.image_to_string(thresh, config="--psm 7 --oem 3")
    print(f"OCR result:\n{text}")