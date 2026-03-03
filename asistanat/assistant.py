import speech_recognition as sr
import pyttsx3
import datetime
import wikipedia
import pywhatkit
import requests
import openai
import os
from mtranslate import translate
from colorama import Fore, init

init(autoreset=True)

# ================= SETTINGS =================
OPENWEATHER_API = "your_openweather_api_key" \
""
# ============================================

# Initialize voice engine
engine = pyttsx3.init()

# Female voice option
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)  # female voice (usually index 1)
engine.setProperty('rate', 170)

def speak(text):
    print(Fore.CYAN + "nira:", text)
    engine.say(text)
    engine.runAndWait()

def translate_to_english(text):
    return translate(text, "en")

def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(Fore.GREEN + "Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1)
        audio = recognizer.listen(source)

        try:
            text = recognizer.recognize_google(audio, language="hi-IN")
            print(Fore.YELLOW + "You said:", text)
            return translate_to_english(text).lower()
        except:
            speak("Sorry, I didn't understand.")
            return ""

# ================= FEATURES =================

def open_apps(command):
    if "chrome" in command:
        speak("Opening Chrome")
        os.system("start chrome")  # Windows
    elif "code" in command or "vs code" in command:
        speak("Opening Visual Studio Code")
        os.system("code")

def send_whatsapp(command):
    speak("Tell me the phone number with country code")
    number = input("Enter number: ")
    if not number .startswith("+"):
        number = "+91" + number  # Default to India country code
    speak("What is the message?")
    message = take_command()

    now = datetime.datetime.now()
    send_time = now + datetime.timedelta(minutes=2)  # Schedule for 2 minutes later

    hour = send_time.hour
    minute = send_time.minute

    pywhatkit.sendwhatmsg(number, message, hour, minute)
    speak("Message scheduled successfully")

#def get_weather(command):
    speak("Tell me the city name")
    city = take_command()
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHER_API}&units=metric"
    response = requests.get(url).json()

    if response["cod"] != "404":
        temp = response["main"]["temp"]
        desc = response["weather"][0]["description"]
        speak(f"The temperature in {city} is {temp} degree Celsius with {desc}")
    else:
        speak("City not found")

def ask_chatgpt(command):
    speak("Thinking...")
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": command}]
    )
    answer = response.choices[0].message.content
    speak(answer)

# ================= MAIN LOOP =================

def run_assistant():
    speak("Hello, I am ALEXA. How can I help you sai?")

    while True:
        command = take_command()

        if "open" in command:
            open_apps(command)

        elif "send whatsapp" in command:
            send_whatsapp(command)

        elif "weather" in command:
            get_weather(command)

        elif "time" in command:
            time = datetime.datetime.now().strftime("%I:%M %p")
            speak(f"The time is {time}")

        elif "who is" in command:
            person = command.replace("who is", "")
            info = wikipedia.summary(person, 2)
            speak(info)

        elif "exit" in command or "stop" in command:
            speak("Goodbye!")
            break

        else:
           ask_chatgpt(command)

if __name__ == "__main__":
    run_assistant()

    