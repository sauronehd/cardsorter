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

    # Initial crop to rough region of interest
    h, w = gray.shape
    crop = gray[int(h * 0.5):int(h * 0.6), int(w * 0.3):int(w * 0.75)]
    cv2.imwrite("debug_crop.png", crop)

    # Upscale 2x
    crop = cv2.resize(crop, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Denoise before thresholding
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

    # Invert if background is dark
    if cv2.mean(thresh)[0] < 127:
        thresh = cv2.bitwise_not(thresh)

    # --- Auto-crop: remove black borders by finding content pixels ---
    _, binary = cv2.threshold(equalized, 30, 255, cv2.THRESH_BINARY)
    coords = cv2.findNonZero(binary)

    if coords is None:
        print("No content found after thresholding — check debug_crop.png")
    else:
        x, y, cw, ch = cv2.boundingRect(coords)

        # Add padding so letters aren't right at the edge
        pad = 10
        y1 = max(0, y - pad)
        y2 = min(thresh.shape[0], y + ch + pad)
        x1 = max(0, x - pad)
        x2 = min(thresh.shape[1], x + cw + pad)

        text_region = thresh[y1:y2, x1:x2]
        cv2.imwrite("text_region.png", text_region)

        # Try multiple PSM modes, use first non-empty result
        best = ""
        for psm in [7, 6, 11, 3]:
            result = pytesseract.image_to_string(
                text_region, config=f"--psm {psm} --oem 3"
            ).strip()
            print(f"PSM {psm}: '{result}'")
            if result and not best:
                best = result

        print(f"\nBest OCR result: '{best}'")