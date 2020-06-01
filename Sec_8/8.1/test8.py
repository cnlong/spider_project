"""
B站滑块验证码
https://blog.csdn.net/weixin_45042620/article/details/105905106
"""
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from PIL import Image
from io import BytesIO
import time

browser = webdriver.Chrome()
url = 'https://passport.bilibili.com/login'
browser.get(url)

username = browser.find_element_by_id('login-username')
passwd = browser.find_element_by_id('login-passwd')
username.send_keys('13809023772')
passwd.send_keys('cal09160829')
wait = WebDriverWait(browser, 10)

login = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, 'btn-login')))
login.click()

time.sleep(3)

# 获取缺口图片、滑块位置、完整图片
# 完整图片的canvas默认是隐藏的，可以设置其display为block，即可查看完整图片
# 带缺口图片和滑块位置的宽高一致，所以会显示在同一大小的框中
c_background = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas.geetest_canvas_bg.geetest_absolute')))
c_slice=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas.geetest_canvas_slice.geetest_absolute')))
c_full_bg=wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'canvas.geetest_canvas_fullbg.geetest_fade.geetest_absolute')))

# 隐藏滑块，截取全图，根据c_backgroud裁剪只含缺口的图片
# 执行JS隐藏滑块
# execute_script函数可以传入多参数，argumenst是指JS代码后的所有参数，"arguments[0].style=arguments[1]"是要执行的JS代码，
# 而后面的c_slice, "display: none"就是后续传入的多参数
# 最终要执行的JS代码即"c_slice.style='display: none'"
browser.execute_script("arguments[0].style=arguments[1]", c_slice, "display: none")

# 网页整体截图
# get_screenshot_as_png()，得到的是二进制数据；通过BytesIO进行转换为Image可接受的格式
screenshot = browser.get_screenshot_as_png()
screenshot = Image.open(BytesIO(screenshot))

# 获取带缺口的验证码图片的位置和大小，然后计算出其四周范围，然后截图获取该带缺口的图片
img_size = c_background.size
location = c_background.location
top, bottom, left, right = location['y'], location['y'] + img_size['height'], location['x'], location['x'] + img_size['width']
# 根据四周范围裁剪截图
img1 = screenshot.crop((left, top, right, bottom))
img1.save('background.png')

# 获取既包含滑块又包含缺口的图片,即将上一步中设置的display改为block
browser.execute_script("arguments[0].style=arguments[1]", c_slice, "display: block")
screenshot = browser.get_screenshot_as_png()
screenshot = Image.open(BytesIO(screenshot))
img_size = c_background.size
location = c_background.location
top, bottom, left, right = location['y'], location['y'] + img_size['height'], location['x'], location['x'] + img_size['width']
# 根据四周范围裁剪截图
img2 = screenshot.crop((left, top, right, bottom))
img2.save('background2.png')


# 获取不包含缺口和滑块的完整图片，设置完整图片的display为block即可
browser.execute_script("arguments[0].style=arguments[1]", c_full_bg, "display: block")
screenshot = browser.get_screenshot_as_png()
screenshot = Image.open(BytesIO(screenshot))
img_size = c_background.size
location = c_background.location
top, bottom, left, right = location['y'], location['y'] + img_size['height'], location['x'], location['x'] + img_size['width']
# 根据四周范围裁剪截图
img3 = screenshot.crop((left, top, right, bottom))
img3.save('background3.png')

# 比对只带缺口的背景图片和不带缺口和滑块的完整图片
# 遍历两张图片的上的像素点，比较同像素点的RGB格式，设定阈值，差值大于这个阈值的点，即为不同的像素
fullbg_img = Image.open('background3.png')
bg_img = Image.open('background.png')

# 遍历一张图片x轴
for i in range(fullbg_img.size[0]):
    # 遍历y轴
    for j in range(fullbg_img.size[1]):
        # 获取带缺口图片此时像素点的RGB值
        bg_pixel = bg_img.load()[i, j]
        # 获取完整图片此时像素点的RGB值
        fullbg_pixel = fullbg_img.load()[i, j]
        # 设置一个阈值，像素值之差超过阈值即认为该像素不相同，此时像素点的x轴距离即为缺口的位置
        threshold = 10
        # 判断像素的各个值颜色之差，ads()去绝对值
        # 没有差距的像素点，计算之后的值为0，小于阈值即为true,有差距的像素点，计算之后的值大于阈值，即为false
        if not(abs(bg_pixel[0]-fullbg_pixel[0]) < threshold and abs(bg_pixel[1]-fullbg_pixel[1]) < threshold and abs(bg_pixel[2]-fullbg_pixel[2]) < threshold):
            distance = i
            print(distance)
            # break只能跳出当前的i循环，还会接着下一个i的循环，所以后续还需要加个break
            break
        else:
            # 继续循环，不走后续步骤，即继续循环j
            continue
    else:
        continue
    break





