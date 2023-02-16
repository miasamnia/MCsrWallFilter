import keyboard
import time
import pyautogui
import cv2
import numpy as np
from PIL import Image


# time.sleep(2)
# img = pyautogui.screenshot(region=[1280 * (4 % 2), 288 * (4 / 2) - 144 * (4 % 2), 1280, 288])
# im = img.convert("RGB")
# im.save('D:\.desktop\\test\c.png')
# time.sleep(20)

num = 3600
time.sleep(0.5)
for n in range(num):
    time.sleep(2)
    for i in range(10):
        # keyboard.press_and_release('shift+win+s')
        img = pyautogui.screenshot(region=[1280*(i%2), 288*(i/2)-144*(i%2), 1280, 288])
        img_standard = img.resize((480, 216), Image.LANCZOS)
        img_standard.save('D:\.desktop\wpImage\\'+str(n*10+i+3959)+'.png')
    keyboard.press_and_release('t')