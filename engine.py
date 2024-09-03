import pyttsx3
from decouple import config
from datetime import datetime 
import speech_recognition as sr
from random import choice
from utils import opening_text
import requests
from folder.online_ops import find_my_ip, get_latest_news, get_random_advice, get_random_joke, get_weather_report, play_on_youtube, search_on_google, search_on_wikipedia, send_whatsapp_message
from folder.os_ops import open_notepad,open_calculator,open_camera,open_cmd
from pprint import pprint
import os

USERNAME = config('USER')
BOTNAME = config('BOTNAME')

# Directory to save user input audio
#AUDIO_DIR = "user_audio"

# Create directory if it doesn't exist
# if not os.path.exists(AUDIO_DIR):
#     os.makedirs(AUDIO_DIR)

engine = pyttsx3.init('sapi5')
#sapi5 is a microsoft speech api

# Set Rate
engine.setProperty('rate', 190)

# Set Volume
engine.setProperty('volume', 1.0)

# Set Voice (Female)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)


r = sr.Recognizer()
# Text to Speech Conversion
def speak(text):
    """Used to speak whatever text is passed to it"""
    engine.say(text)
    engine.runAndWait()

def greet_user():
    """Greets the user according to the time"""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        speak(f"Good Morning {USERNAME}")
        print(f"Good Morning {USERNAME}")
    elif 12 <= hour < 16:
        speak(f"Good afternoon {USERNAME}")
        print(f"Good afternoon {USERNAME}")
    elif 16 <= hour < 19:
        speak(f"Good Evening {USERNAME}")
        print(f"Good Evening {USERNAME}")
    else:
        speak(f"Hello {USERNAME}")
        print(f"Hello {USERNAME}")
    speak(f"I am your {BOTNAME}. How may I help you?")
    print(f"I am your {BOTNAME}. How may I help you?")

# Function to speak text
def speak(text):
    """Used to speak whatever text is passed to it"""
    engine.say(text)
    engine.runAndWait()

# Takes Input from User
def take_user_input():
    """Takes user input, recognizes it using Speech Recognition module and converts it into text"""
    with sr.Microphone() as source:
        print('Tuning in.....')
        r.adjust_for_ambient_noise(source)  # Adjust for ambient noise
        audio = r.listen(source, timeout=5)  # Listen for up to 5 seconds or until silence is detected

    try:
        print('Catching On')
        query = r.recognize_google(audio, language='en-in')
        print(f"User said: {query}")
        
        if not 'exit' in query or 'stop' in query:
            speak(choice(opening_text))
        else:
            hour = datetime.now().hour
            if hour >= 21 and hour < 6:
                speak(f"Good night, take care {USERNAME}!")
                print(f"Good night, take care {USERNAME}!")
            else:
                speak(f'Have a good day {USERNAME}!')
                print(f'Have a good day {USERNAME}!')
            exit()
        # audio_filename = f"user_input_{datetime.now().strftime('%Y%m%d%H%M%S')}.mp3"
        # audio_path = os.path.join(AUDIO_DIR, audio_filename)
        # audio.export(audio_path, format="mp3")
        return query.lower()
    except sr.UnknownValueError:
        speak('Sorry, I could not understand. Could you please say that again?')
        print('Sorry, I could not understand. Could you please say that again?')
    except sr.RequestError:
        speak('Sorry, I am facing some issues. Please try again later.')
        print('Sorry, I am facing some issues. Please try again later.')
    return None

if __name__ == '__main__':
    greet_user()
    
    while True:
        query = take_user_input()
        
        if query:
            print(f"User Query: {query}")
            function_executed = False
            
            if 'open notepad' in query:
                open_notepad()
                function_executed = True
            
            elif 'open command prompt' in query or 'open cmd' in query:
                open_cmd()
                function_executed = True
            
            elif 'open camera' in query:
                open_camera()
                function_executed = True
            
            elif 'open calculator' in query:
                open_calculator()
                function_executed = True
            
            elif 'ip address' in query:
                ip_address = find_my_ip()
                speak(f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen {USERNAME}.')
                print(f'Your IP Address is {ip_address}')
                function_executed = True
            
            elif 'wikipedia' in query:
                speak(f'What do you want to search on Wikipedia{USERNAME}?')
                print('What do you want to search on Wikipedia?')
                search_query = take_user_input()
                results = search_on_wikipedia(search_query)
                speak(f"According to Wikipedia, {results}")
                speak("For your convenience, I am printing it on the screen.")
                print(results)
                function_executed = True
            
            elif 'youtube' in query:
                speak(f'What do you want to play on Youtube, {USERNAME}?')
                print('What do you want to play on Youtube?')
                video = take_user_input()
                play_on_youtube(video)
                function_executed = True
            
            elif 'search on google' in query:
                speak(f'What do you want to search on Google, {USERNAME}?')
                print('What do you want to search on Google?')
                query = take_user_input()
                search_on_google(query)
                function_executed = True
            
            elif "send whatsapp message" in query:
                speak(
                    f'On what number should I send the message {USERNAME}? Please enter in the console: ')
                number = input("Enter the number: ")
                speak("What is the message?")
                message = take_user_input()
                send_whatsapp_message(number, message)
                function_executed = True
            
            # Uncomment this block if you want to include email functionality
            # elif "send an email" in query:
            #     speak("On what email address do I send sir? Please enter in the console: ")
            #     receiver_address = input("Enter email address: ")
            #     receiver_address=take_user_input()
            #     speak("What should be the subject?")
            #     subject = take_user_input()
            #     speak("What is the message ?")
            #     message = take_user_input()
            #     if send_email(receiver_address, subject, message):
            #         speak("I've sent the email.")
            #     else:
            #         speak("Something went wrong while I was sending the mail. Please check the error logs.")
            #     function_executed = True
            
            elif 'joke' in query:
                speak(f"Hope you like this one..")
                joke = get_random_joke()
                speak(joke)
                pprint(joke)
                function_executed = True
            
            elif "advice" in query:
                speak(f"Here's an advice for you..")
                advice = get_random_advice()
                speak(advice)
                pprint(advice)
                function_executed = True
            
            elif 'news' in query:
                speak(f"I'm reading out the latest news headlines")
                speak(get_latest_news())
                print(*get_latest_news(), sep='\n')
                function_executed = True
            
            elif 'weather' in query:
                ip_address = find_my_ip()
                city = requests.get(f"https://ipapi.co/{ip_address}/city/").text
                speak(f"Getting weather report for your city {city}")
                weather, temperature, feels_like = get_weather_report(city)
                speak(f"The current temperature is {temperature}, but it feels like {feels_like}")
                speak(f"Also, the weather report talks about {weather}")
                print(f"Description: {weather}\nTemperature: {temperature}\nFeels like: {feels_like}")
                function_executed = True
            
            if function_executed:
                break
