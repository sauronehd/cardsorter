from algorithim import *
import pytesseract
from PIL import Image
image = Image.open("ROS019.png")
numbers = [["0","o"],["1","i"],["2","s"],["3","e"],["4","r"],["5","s"],["6","p"],["7","f"],["8","b"],["9","p"]]
#text = pytesseract.image_to_string(image)
text = input("Enter your text: ")
print(f"text is : {text}")
rawCardSet = (text[0:3])
print(f"rawCardSet is {rawCardSet}")
for i in range(len(rawCardSet)):
    l = rawCardSet[i]
    if l.isnumeric():
        print(f"{rawCardSet[i]} is {l}")
        for n in numbers:
            if l==n[0]:
                if n[0] == "1" and i == 0:
                    pass
                else:

                    print(f"Replacing {l} with {n[1]}")
                    rawCardSet = rawCardSet.replace(l,n[1])
                    print(f"rawcardset is now: {rawCardSet}")




print(rawCardSet)
rawCardSet = rawCardSet.lower()
rawCardSet = rawCardSet.strip()
print(rawCardSet)
similar = findSimilarSet(rawCardSet)
match = ["", 0]
for pair in similar:
    if pair[1]>match[1]:
        match[1] = pair[1]
        match[0] = pair[0]
print(match)