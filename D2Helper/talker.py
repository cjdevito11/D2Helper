import random
import time
import pyautogui
import keyboard
from datetime import datetime

inGame = False

# Array of messages
messages = [
    "Join the D2 Hustlers Discord - https://discord.gg/QSH9uZqVmK",
    "Wassup?? -     -   -   https://discord.gg/QSH9uZqVmK",
    "Who's on?  -     -   -    https://discord.gg/QSH9uZqVmK",
    "Free Rushes - D2 Hustlers - https://discord.gg/QSH9uZqVmK",
    "D2 Hustlers are looking for new members! (SCL, SCNL, HCL) - https://discord.gg/QSH9uZqVmK",
    "D2 Hustlers - Duel Tournaments, Tons of free giveaways, rushes, Professional help, Trade rooms, Help rooms, Noobie rooms, Mentorship - https://discord.gg/QSH9uZqVmK",
    "Anyone looking for a super active D2R group to play and have fun with check out the D2 Hustlers - https://discord.gg/QSH9uZqVmK",
    "Hey there! How's everyone doing?  -     -   -    https://discord.gg/QSH9uZqVmK",
    "Looking for a team to play with? Join us!  -     -   -    https://discord.gg/QSH9uZqVmK",
    "Free items for new members! Join our Discord - https://discord.gg/QSH9uZqVmK",
    "Let's get some games going! - https://discord.gg/QSH9uZqVmK",
    "Anyone up for a trade? - https://discord.gg/QSH9uZqVmK",
    "New to the game? Get help here!  -     -   -    https://discord.gg/QSH9uZqVmK",
    "Join our community for the latest updates and events - https://discord.gg/QSH9uZqVmK",
    "Looking for tips and tricks? Check out our Discord - https://discord.gg/QSH9uZqVmK",
    "D2 Hustlers is the place to be for all D2R players! - https://discord.gg/QSH9uZqVmK",
    "Join us for fun and giveaways! - https://discord.gg/QSH9uZqVmK",
    "Need a rush? We got you covered! -     -   -   - https://discord.gg/QSH9uZqVmK",
    "Let's raid together! - https://discord.gg/QSH9uZqVmK",
    "Looking for a mentor? Find one here!  -     -   -    https://discord.gg/QSH9uZqVmK",
    "Join D2 Hustlers for daily activities and more! - https://discord.gg/QSH9uZqVmK",
    "Want to be part of a great community? Join us! - https://discord.gg/QSH9uZqVmK",
    "Free gear and items available!  -     -   -    https://discord.gg/QSH9uZqVmK",
    "Stay updated with the latest game news - https://discord.gg/QSH9uZqVmK",
    "Meet new friends and teammates!  -     -   -    https://discord.gg/QSH9uZqVmK",
    "D2 Hustlers are recruiting! - https://discord.gg/QSH9uZqVmK",
    "Looking for a challenge? Join our tournaments! - https://discord.gg/QSH9uZqVmK",
    "Get your questions answered by pros!  -     -   -    https://discord.gg/QSH9uZqVmK",
    "Join us for exclusive events and rewards - https://discord.gg/QSH9uZqVmK",
    "Need help with a quest? Ask here! - https://discord.gg/QSH9uZqVmK",
    "Join the conversation! - https://discord.gg/QSH9uZqVmK",
    "Share your gaming moments with us!  -     -   -    https://discord.gg/QSH9uZqVmK",
    "D2 Hustlers: Where gamers unite! - https://discord.gg/QSH9uZqVmK",
    "Join our Discord for a better gaming experience - https://discord.gg/QSH9uZqVmK",
    "Looking for game strategies? Find them here!  -     -   -    https://discord.gg/QSH9uZqVmK",
    "Join us for fun and excitement! - https://discord.gg/QSH9uZqVmK",
    "Get exclusive tips and tricks from experts - https://discord.gg/QSH9uZqVmK",
    "Find your perfect gaming buddy here - https://discord.gg/QSH9uZqVmK",
    "Join D2 Hustlers for an amazing community - https://discord.gg/QSH9uZqVmK",
    "Ready for some action? Join us now!  -     -   -    https://discord.gg/QSH9uZqVmK",
    "Join our group for the best D2R experience - https://discord.gg/QSH9uZqVmK",
    "Meet fellow gamers and make new friends - https://discord.gg/QSH9uZqVmK",
    "Join the hustle! - https://discord.gg/QSH9uZqVmK",
    "Join now for exclusive giveaways and events - https://discord.gg/QSH9uZqVmK",
    "Looking for a community? Join D2 Hustlers  -     -   -    https://discord.gg/QSH9uZqVmK",
    "Need help with builds? Get advice here  -     -   -    https://discord.gg/QSH9uZqVmK",
    "Join D2 Hustlers and level up your game - https://discord.gg/QSH9uZqVmK",
    "New to the game? We can help! - https://discord.gg/QSH9uZqVmK",
    "Join us and become a pro! - https://discord.gg/QSH9uZqVmK",
    "Looking for tips? Join our Discord  -     -   -    https://discord.gg/QSH9uZqVmK",
    "Join the best D2R community today!  -     -   -    https://discord.gg/QSH9uZqVmK"
]

# Function to send a message
def send_message(message):
    global inGame
    if inGame:
        pyautogui.press('enter')
    pyautogui.typewrite(message)
    pyautogui.press('enter')

# Function to get the current timestamp
def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

# Main loop
try:
    while True:
        # Check for the kill switch
        if keyboard.is_pressed('+'):
            print(f"{get_timestamp()} - Kill switch activated. Exiting...")
            break

        x = 0
        while x < 2:
            # Select a random message
            message = random.choice(messages)
            print(f"{get_timestamp()} - Sending Message: {message}")
            send_message(message)
            time.sleep(random.randint(20,40))
            x += 1

        # Wait for a random interval between 2-5 minutes
        wait_time = random.randint(20*60, 50*60)
        for _ in range(wait_time):
            # Check for the kill switch during the wait
            if keyboard.is_pressed('+'):
                print(f"{get_timestamp()} - Kill switch activated. Exiting...")
                break
            time.sleep(1)
        
except KeyboardInterrupt:
    print(f"{get_timestamp()} - Script terminated by user.")
except Exception as e:
    print(f"{get_timestamp()} - An error occurred: {e}")

print(f"{get_timestamp()} - Script ended.")
