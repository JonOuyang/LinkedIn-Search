from PIL import Image 
import pytesseract
from pytesseract import pytesseract
from pytesseract import Output
import pyautogui
import numpy as np
import cv2
import time

print(pyautogui.size()) 
print(pyautogui.position()) 

custom_config = r'--oem 3 --psm 6'
master_list = []

#while True:

def checkPost():
    global master_list
    pyautogui.moveTo(643, 643, duration=0.1)
    img = cv2.cvtColor(np.array(pyautogui.screenshot(region=(425, 225, 475, 775))), cv2.COLOR_RGB2BGR)
    text = pytesseract.image_to_string(img, config=custom_config)
    split = text.split("\n")
    counter = 0
    x = []
    while counter < len(split):
        if "-" in split[counter]:
            x = split[counter].split("-")
            break
        else:
            counter+=1
    while True:
        pyautogui.moveTo(643, 643, duration=0.1)
        pyautogui.scroll(-800)
        img = cv2.cvtColor(np.array(pyautogui.screenshot(region=(425, 225, 475, 775))), cv2.COLOR_RGB2BGR)
        text = pytesseract.image_to_string(img, config=custom_config).lower()
        if "degree" in text:
            #print("keyword found!")
            master_list.append({"Job Title: ":split[0], "Company: ":x[0]})
            break
        if "about the company" in text:
            #print("end of job post")
            break
            
def checkList():
    y = 400 
    for i in range(5):
        pyautogui.moveTo(215, y, duration=0.2)
        pyautogui.click()
        checkPost()
        y+=150
    counter = 5
    pyautogui.moveTo(215, 1000, duration=0.2)
    while counter<=25:
        #time.sleep(0.8)
        img = cv2.cvtColor(np.array(pyautogui.screenshot(region=(360, 960, 40, 80))), cv2.COLOR_RGB2BGR)
        text = pytesseract.image_to_string(img, config=custom_config).lower()
        fail=0
        if "x" in text:
            pyautogui.moveTo(215, 1000, duration=0.2)
            pyautogui.click()
            checkPost()
            counter+=1
            #print("click")
        else:
            fail+=1
        if fail==4:
            break
            pyautogui.moveTo(215, 1000, duration=0.2)
            pyautogui.scroll(-500)
        pyautogui.moveTo(215, 1000, duration=0.2)
        pyautogui.scroll(-70)

checkList()
print(master_list)

