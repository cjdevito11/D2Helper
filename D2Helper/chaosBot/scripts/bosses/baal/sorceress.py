import pyautogui
import time

def hydraBaal():
    print('Hydra Sorc - Baal')
    pyautogui.moveTo(1750,200)
    time.sleep(.5)
    pyautogui.press(teleHotkey)
    time.sleep(.7)
    pyautogui.press(teleHotkey)
    time.sleep(.6)
    pyautogui.moveTo(1750,750)
    time.sleep(.5)
    pyautogui.press(teleHotkey)
    time.sleep(.6)
    pyautogui.press(teleHotkey)
    time.sleep(.8)
    print(f'* pyautogui.move(500,600) *')
    pyautogui.moveTo(500,600)
    time.sleep(.6)
    pyautogui.press(teleHotkey)
    time.sleep(.5)
    print(f'* pyautogui.move(240,330) *')
    pyautogui.moveTo(240,330)
    pyautogui.press(attackHotkey)
    time.sleep(.2)
    pyautogui.press(attackHotkey)
    time.sleep(.2)
    pyautogui.press(attackHotkey)
    time.sleep(.2)
    pyautogui.press(attackHotkey)
    time.sleep(.2)
    pyautogui.press(attackHotkey)
    time.sleep(.2)
    pyautogui.press(attackHotkey)
    time.sleep(.2)
    pyautogui.press(attackHotkey)
    time.sleep(.2)
    pyautogui.press(attackHotkey)
    time.sleep(2)
    pyautogui.moveTo(1750,350)
    time.sleep(.5)
    pyautogui.press(teleHotkey)
    time.sleep(1)
    pyautogui.press(teleHotkey)
    time.sleep(.5)

def blizzBaal():
    pass

def meteorBaal():
    pass