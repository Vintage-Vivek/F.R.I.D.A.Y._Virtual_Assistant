import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from openai import OpenAI
from gtts import gTTS
import pygame
import os


# F.R.I.D.A.Y - "Fast Responsive Intelligent Digital Assistant for You"

recognizer = sr.Recognizer()
engine = pyttsx3.init() 
newsapi = "--------------------------"  # Replace with your actual NewsData API key

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 
    pygame.mixer.init()
    pygame.mixer.music.load('temp.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

def aiProcess(command):
    client = OpenAI(api_key="----------------------------------")  # Replace with your OpenAI API key
    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a virtual assistant named friday."},
            {"role": "user", "content": command}
        ]
    )
    return completion.choices[0].message.content

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music.get(song, None)
        if link:
            webbrowser.open(link)
        else:
            speak("Sorry, I couldn't find that song.")
    elif "headlines" in c.lower():
        # NewsData API setup
        url = "-----------------------" # Replace with your actual NewsData API URL
        params = {
            # "apikey": ,
            # "country": "",  
            # "language": ""  # set your own parameters here
        }
        # Make GET request to NewsData API
        r = requests.get(url, params=params)
        
        if r.status_code == 200:
            # Print the JSON response to see the format
            print("NewsData API response:", r.json())  # Debugging: Print API response
            articles = r.json().get('results', [])
            if articles:
                for article in articles[:5]:
                    speak(article['title'])
            else:
                speak("No headlines found.")
        else:
            print("Failed to fetch news:", r.status_code, r.text)  # Debugging: Print error details
            speak("Unable to fetch news right now.")
    else:
        output = aiProcess(c)
        speak(output) 

if __name__ == "__main__":
    speak("Initializing friday....")
    while True:
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source, duration=2)
                print("Listening for wake word...")
                
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=3)

            try:
                word = recognizer.recognize_google(audio).lower()
                print(f"Detected phrase: {word}")
                
                if word == "hello":
                    speak("Yes?")
                    with sr.Microphone() as source:
                        print("Listening for command...")
                        audio = recognizer.listen(source, timeout=10)
                        command = recognizer.recognize_google(audio)
                        print(f"Detected command: {command}")
                        processCommand(command)
            except sr.UnknownValueError:
                print("Could not understand the wake word.")
            except sr.RequestError:
                print("Speech recognition service is unavailable.")
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for wake word.")
        except Exception as e:
            print(f"Error: {e}")
