import pytesseract
from PIL import Image

# Open an image and extract text
image = Image.open("document.jpg")
text = pytesseract.image_to_string(image)

print(text)