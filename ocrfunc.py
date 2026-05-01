import pytesseract





def ocr(image):
    try:
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        print(f"Error: {e}")
        return False