import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from selenium import webdriver
from selenium.webdriver.common.by import By
import time


# ========================
# Spotify Authentication
# ========================
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id="c21bdb68de634f0fb9c6f5c1f3954ae0",
                                               client_secret="625313a7f836475babe6512e72abb81f",
                                               redirect_uri="http://localhost:8888/callback",
                                               scope="user-modify-playback-state user-read-playback-state"))


# ========================
# Initialize Speech Recognition and TTS
# ========================
recognizer = sr.Recognizer()
machine = pyttsx3.init()


# ========================
# Text-to-Speech Function
# ========================
def talk(text):
    machine.say(text)
    machine.runAndWait()


# ========================
# Voice Command Function
# ========================
def get_instruction():
    try:
        with sr.Microphone() as source:
            print("Listening...")
            recognizer.adjust_for_ambient_noise(source)
            speech = recognizer.listen(source)
            instruction = recognizer.recognize_google(speech)
            instruction = instruction.lower()
            if "jarvis" in instruction:
                instruction = instruction.replace('jarvis', "").strip()  # Remove "jarvis" from the command
                print(f"Recognized command: {instruction}")
                return instruction
    except sr.UnknownValueError:
        print("Sorry, I did not understand that.")
        talk("Sorry, I did not understand that.")
    except sr.RequestError as e:
        print(f"Could not request results from Google Speech Recognition service; {e}")
        talk("There was a problem with the recognition service.")
    return None


# ========================
# Spotify Automation Logic
# ========================
def spotify_automation(instruction):
    if 'spotify' in instruction:
        song_name = instruction.replace('spotify', '').strip()
        results = sp.search(q=song_name, limit=1)
        if results['tracks']['items']:
            song_uri = results['tracks']['items'][0]['uri']
            sp.start_playback(uris=[song_uri])
            talk(f'Playing {song_name}')
        else:
            talk("Song not found")

    elif 'pause' in instruction:
        sp.pause_playback()
        talk('Music paused')

    elif 'resume' in instruction:
        sp.start_playback()
        talk('Resuming music')

    elif 'next' in instruction:
        sp.next_track()
        talk('Skipping to next track')

    elif 'stop' in instruction:
        sp.pause_playback()
        talk('Music stopped')

    else:
        talk('Please say a valid command')


# ========================
# General Instruction Handling
# ========================
def play_instruction():
    instruction = get_instruction()
    if instruction:
        # Handle YouTube commands
        if "play" in instruction:
            song = instruction.replace('play', "").strip()
            talk("Playing " + song)
            pywhatkit.playonyt(song)
        
        # Handle Spotify commands
        elif any(keyword in instruction for keyword in ["spotify", "pause", "resume", "next", "stop"]):
            spotify_automation(instruction)

        # Time command
        elif 'time' in instruction:
            current_time = datetime.datetime.now().strftime('%I:%M %p')
            talk('The current time is ' + current_time)

        # Date command
        elif 'date' in instruction:
            date = datetime.datetime.now().strftime('%d/%m/%Y')
            talk("Today's date is " + date)

        # General conversation commands
        elif 'how are you' in instruction:
            talk('I am fine, how about you?')
        elif 'what is your name' in instruction:
            talk('I am Jarvis, what can I do for you?')

        # Wikipedia lookup
        elif 'who is' in instruction:
            human = instruction.replace('who is', '').strip()
            info = wikipedia.summary(human, 1)
            print(info)
            talk(info)
        
        else:
            talk("Please say that again.")
    else:
        talk("Please say that again.")


# ========================
# WhatsApp Automation Logic
# ========================
def whatsapp_automation(instruction):
    if 'send message' in instruction:
        contact = instruction.replace('send message to', '').strip()
        message = "Hello from Jarvis!"  # Customize your message
        # Send WhatsApp message using pywhatkit
        try:
            phone_number = '+917842762931'  # Replace with actual phone number
            pywhatkit.sendwhatmsg(phone_number, message, datetime.datetime.now().hour, datetime.datetime.now().minute + 2)
            talk(f"Message sent to {contact}")
        except Exception as e:
            print(f"Error sending message: {e}")
            talk("There was an error sending the message.")

    elif 'call' in instruction:
        contact = instruction.replace('call', '').strip()
        initiate_whatsapp_call(contact)

    elif 'video call' in instruction:
        contact = instruction.replace('video call', '').strip()
        initiate_whatsapp_video_call(contact)


# ========================
# WhatsApp Call Functions
# ========================
def initiate_whatsapp_call(contact_name):
    # Open WhatsApp Web and call the contact
    driver = webdriver.Chrome(executable_path='chromedriver.exe')  # Update with your WebDriver path
    driver.get('https://web.whatsapp.com')
    input('Press ENTER after scanning QR code')
    time.sleep(3)  # Wait for the page to load

    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.send_keys(contact_name)
    time.sleep(2)

    # Click on the contact
    contact = driver.find_element(By.XPATH, f'//span[@title="{contact_name}"]')
    contact.click()

    # Click the call button
    call_button = driver.find_element(By.XPATH, '//span[@data-icon="phone"]')
    call_button.click()
    talk(f"Calling {contact_name} on WhatsApp")

## ========================
## Whatsapp video call Logic
## ========================
def initiate_whatsapp_video_call(contact_name):
    # Open WhatsApp Web and initiate video call
    driver = webdriver.Chrome(executable_path='chromedriver.exe')  # Update with your WebDriver path
    driver.get('https://web.whatsapp.com')
    input('Press ENTER after scanning QR code')
    time.sleep(3)

    search_box = driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')
    search_box.send_keys(contact_name)
    time.sleep(2)

    # Click on the contact
    contact = driver.find_element(By.XPATH, f'//span[@title="{contact_name}"]')
    contact.click()

    # Click the video call button
    video_call_button = driver.find_element(By.XPATH, '//span[@data-icon="video"]')
    video_call_button.click()
    talk(f"Starting video call with {contact_name}")


# ========================
# Start Listening Process
# ========================
play_instruction()

