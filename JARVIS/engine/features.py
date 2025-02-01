from shlex import quote
import subprocess
import threading
import pyautogui
import pygame
import eel
eel.init(r'C:\Users\KUSHAL\OneDrive\Desktop\voice\www')

from engine.command import speak
from engine.config import ASSISTANT_NAME
import os
import re
import pywhatkit as kit
import webbrowser
import sqlite3
import struct
import time
import pvporcupine
import pyaudio
import pyautogui as autogui


from engine.helper import extract_yt_term, remove_words
from hugchat import hugchat

con = sqlite3.connect("jarvis.db")
cursor = con.cursor()

# Initialize pygame mixer
pygame.mixer.init()

# Playing assistant sound function
@eel.expose
def playAssistantSound():
    # Specify the path to the sound file (make sure it is correct)
    music_dir = "C:\\Users\\KUSHAL\\OneDrive\\Desktop\\voice\\www\\assets\\audio\\start_sound.mp3"  # Make sure the file is an mp3
    try:
        # Load and play the sound
        pygame.mixer.music.load(music_dir)
        pygame.mixer.music.play()
    except pygame.error as e:
        # Handle errors if the sound file can't be played
        print(f"Error loading or playing the sound: {e}")
        speak("There was an error playing the sound.")

# Function to open a command
def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query = query.lower()

    app_name = query.strip()
    if app_name != "":

            try:
                cursor.execute(
                    'SELECT path FROM sys_command WHERE name IN (?)', (app_name,))
                results = cursor.fetchall()

                if len(results) != 0:
                    speak("Opening "+query)
                    os.startfile(results[0][0])

                elif len(results) == 0: 
                    cursor.execute(
                    'SELECT url FROM web_command WHERE name IN (?)', (app_name,))
                    results = cursor.fetchall()
                
                if len(results) != 0:
                    speak("Opening "+query)
                    webbrowser.open(results[0][0])

                else:
                    speak("Opening "+query)
                    try:
                        os.system('start '+query)
                    except:
                        speak("not found")
            except:
                speak("something went wrong")


# Function to play YouTube video
def PlayYoutube(query):
    search_term = extract_yt_term(query)
    speak("Playing " + search_term + " on YouTube")
    kit.playonyt(search_term)

# Function to extract YouTube search term from the query
def hotword():
    porcupine = None
    paud = None
    audio_stream = None
    try:
        # pre trained keywords
        porcupine = pvporcupine.create(keywords=["jarvis", "alexa","porcupine","hey siri"])
        paud = pyaudio.PyAudio()
        audio_stream = paud.open(rate=porcupine.sample_rate, channels=1, format=pyaudio.paInt16, input=True,
                                  frames_per_buffer=porcupine.frame_length)

        # loop for streaming
        while True:
            keyword = audio_stream.read(porcupine.frame_length)
            keyword = struct.unpack_from("h" * porcupine.frame_length, keyword)

            # processing keyword comes from mic
            keyword_index = porcupine.process(keyword)

            # checking first keyword detected
            if keyword_index >= 0:
                print("Hotword detected")

                # pressing shortcut key win+j
                autogui.keyDown("win")
                autogui.press("j")
                time.sleep(2)
                autogui.keyUp("win")

    except Exception as e:
        print(f"Error in hotword detection: {e}")
    finally:
        if porcupine is not None:
            porcupine.delete()
        if audio_stream is not None:
            audio_stream.close()
        if paud is not None:
            paud.terminate()

# Running hotword detection in a separate thread to avoid blocking
def start_hotword_thread():
    hotword_thread = threading.Thread(target=hotword)
    hotword_thread.daemon = True  # This makes the thread exit when the program exits
    hotword_thread.start()

# Call this function to start hotword detection
start_hotword_thread()

if __name__ == "__main__":
    eel.start('index.html')


def findContact(query):

    words_to_remove=[ASSISTANT_NAME,'make','a','to','phone','call','send','message','whatsapp','video']
    query=remove_words(query,words_to_remove)


    try:
        query=query.strip().lower()
        cursor.execute("SELECT mobile_no FROM contacts WHERE LOWER(name) LIKE ? OR LOWER(name) LIKE ?",('%'+query + '%',query + '%'))

        results=cursor.fetchall()
        print(results[0][0])
        mobile_number_str=str(results[0][0])
        
        if not mobile_number_str.startswith('+91'):
            mobile_number_str='+91'+mobile_number_str

        return mobile_number_str,query
    except:
        speak('not exist in contacts')
        return 0,0
    

def whatsApp(mobile_no,message,flag,name):

    if flag=='message':
        target_tab=13
        jarvis_message="message send successfully to"+name


    elif flag=='call':
        target_tab=7
        message=' '
        jarvis_message="calling to "+name 

    else:
        target_tab=6
        message=' '
        jarvis_message=" starting video call to "+name

    #Enc0de the message for url
    encoded_message=quote(message)

    #Construct the URL
    whatsapp_url=f"whatsapp://send?phone={mobile_no}&text={encoded_message}"

    #Construct the full command
    full_command=f'start ""  "{whatsapp_url}"'

    #open whatsapp with the constructed URL using cmd.exe
    subprocess.run(full_command,shell=True)
    time.sleep(5)
    subprocess.run(full_command,shell=True)

    pyautogui.hotkey('ctrl','f')

    for i in range(1,target_tab):
        pyautogui.hotkey('tab')


    pyautogui.hotkey('enter')
    speak(jarvis_message)

#chatbot
def chatBot(query):
    user_input=query.lower()
    chatbot=hugchat.ChatBot(cookie_path="engine\cookies.json")
    id=chatbot.new_conversation()
    chatbot.change_conversation(id)
    response = chatbot.chat(user_input)
    print(response)
    speak(response)
    return response


    
