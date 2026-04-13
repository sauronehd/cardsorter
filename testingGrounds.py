import pytesseract
from PIL import Image
#hello
image = Image.open("ROS019.png")
text = pytesseract.image_to_string(image)
print(text)