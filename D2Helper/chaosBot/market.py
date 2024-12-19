import setup
import time
import pyautogui
import random

messages = [
        "Looking for some action? D2 Hustlers is expanding our EU community! Join us for tournaments, giveaways, 24/7 voice chat, and more! Discord: https://discord.gg/QSH9uZqVmK",
        "Need a solid D2R community? Come hang with the D2 Hustlers! We've got duels, trade channels, and constant voice chat! EU players especially welcome! Discord: https://discord.gg/QSH9uZqVmK",
        "D2 Hustlers - where legends are made! Join us for giveaways, tournaments, trade deals, and non-stop chat. EU crew growing strong! Discord: https://discord.gg/QSH9uZqVmK1",
        "Join the crew that took the #1 Ladder Spot this season! D2 Hustlers is growing our EU community. Giveaways, duels, trades, and 24/7 voice chat await! Discord: https://discord.gg/QSH9uZqVmK",
        "D2 Hustlers are in the house! Looking for EU players to join our tournaments, trades, and 24/7 voice chat. Let's dominate together! Discord: https://discord.gg/QSH9uZqVmK1",
        "EU players, this one's for you! D2 Hustlers is expanding and we want YOU in on the fun! Tournaments, duels, trades, and more. Discord: https://discord.gg/QSH9uZqVmK",
        "Want to play with the best? D2 Hustlers - giveaways, tournaments, and a thriving EU community. Join our Discord and let's hustle: https://discord.gg/QSH9uZqVmK",
        "Looking to join a top-tier D2R community? D2 Hustlers offers trade channels, duels, giveaways, and a 24/7 voice chat. EU members wanted! Discord: https://discord.gg/QSH9uZqVmK",
        "D2 Hustlers: Where the grind never stops! Join our growing EU crew for tournaments, trades, and great company. Discord: https://discord.gg/QSH9uZqVmK",
        "D2 Hustlers secured the #1 Ladder spot this season! Join our EU community for giveaways, duels, and 24/7 voice chat. Discord: https://discord.gg/QSH9uZqVmK"
    ]

def sayInGame(text):
    time.sleep(.3)
    pyautogui.press('enter')
    time.sleep(.3)
    pyautogui.write(text, interval=0.04)
    time.sleep(.3)
    pyautogui.press('enter')
    time.sleep(.3)

def monitorChat():
    while True:
        time.sleep(5)
        print('Reading Chat')
        chat_text = setup.read_screen_text(region=(0, 600, 650, 930))  # Adjust region to match chat area
        print(f'chat_text: {chat_text}')
        if "joined our world" in chat_text:
            print("Print in game")
            message = random.choice(messages)
            sayInGame(message)

monitorChat()
