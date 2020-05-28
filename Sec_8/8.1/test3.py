"""
二值化默认的阈值是127，指定二值化的阈值，提高图片清晰度
"""
from PIL import Image
import pytesseract

image = Image.open('code2.jpg')
image = image.convert('L')
# 设定阈值
threshold = 127
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

image = image.point(table, '1')
result = pytesseract.image_to_string(image)
print(result)