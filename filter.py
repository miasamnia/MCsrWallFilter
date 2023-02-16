import os
from PIL import Image
import numpy as np
import tensorflow as tf
import keyboard
import time
import pyautogui
import win32api, win32con
import win32gui as w

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
pyautogui.FAILSAFE = False

# 'DESERT', 'DESERTNOWATER', 'GREEN', 'GREENDESERT', 'GREENNOTREE',
# 'GREENNOWATER', 'GREENNOWATERTREE', 'GREENVILLAGE', 'LOADING', 'NOTREE',
# 'PERFECT', 'PERFECTNOWATER', 'RUINEDPORTAL', 'SAVANA'
want = ['PERFECT', 'PERFECTNOWATER']
InstanceNumber = 10
WallRow = 5
WallColumn = 2
TimePerCheck = 2
TimeWhenPlaying = 1

ResolutionX = win32api.GetSystemMetrics(win32con.SM_CXSCREEN)
ResolutionY = win32api.GetSystemMetrics(win32con.SM_CYSCREEN)

pixelX = ResolutionX / WallColumn
pixelY = ResolutionY / WallRow

#sum = 2100
model = tf.keras.models.load_model('cher3.h5')
path = 'D:\.desktop\Image\\'
filelist = list(os.listdir(path))
while True:
    time.sleep(TimeWhenPlaying)
    instance = [0] * InstanceNumber  # 1 for locked, 0 for reset
    num = 0
    while 'Fullscreen Projector (Scene)' in w.GetWindowText(
            w.GetForegroundWindow()): # and num < 6:  # break when 6 instances locked
        keyboard.press('t')
        time.sleep(TimePerCheck-0.15*num)
        for i in range(InstanceNumber):  # read screen
            if instance[i] == 1:
                continue
            # keyboard.press_and_release('shift+win+s')
            img = pyautogui.screenshot(
                region=[pixelX * (i % WallColumn), pixelY * (i / WallColumn) - pixelY / WallColumn * (i % WallColumn),
                        pixelX,
                        pixelY])
            img_standard = img.resize((480, 216), Image.LANCZOS)
            Core = img_standard.getdata()
            arr1 = np.array(Core, dtype='float32') / 255.0
            list_img = arr1.tolist()
            im = np.array(list_img).reshape(1, 480, 216, 3)

            predictions_single = model.predict(im)

            # print(filelist[np.argmax(predictions_single)])
            # print(predictions_single)
            # pyautogui.moveTo(1280 * (i % 2) + 640, 288 * (i / 2) - 144 * (i % 2) + 144)
            if filelist[np.argmax(predictions_single)] in want:
                keyboard.press('shift')
                pyautogui.click(pixelX * (i % WallColumn) + pixelX / 2,
                                pixelY * (i / WallColumn) - pixelY / 2 * (i % WallColumn) + pixelY / 2)
                keyboard.release('shift')
                instance[i] = 1
                num += 1
                # print(filelist[np.argmax(predictions_single)])
                # img_standard.save(
                #    'D:\.desktop\\fit\\'  + filelist[np.argmax(predictions_single)]+ str(sum) + '.png')
                # sum+=1
            # img_standard.save('D:\.desktop\\fit\\'  + filelist[np.argmax(predictions_single)]+ str(sum) + '.png')
            # sum+=1
            # if sum%1000 == 0:
            #     time.sleep(10)