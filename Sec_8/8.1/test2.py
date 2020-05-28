from PIL import Image
import pytesseract

image = Image.open('code2.jpg')
# 转换为灰度图像
image = image.convert('L')
image.show()
# 二值化处理
image = image.convert('1')
image.show()