import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
from models.ai_assistant import ask_ai
import threading


recognizer = sr.Recognizer()
# engine = pyttsx3.init()
is_speaking =False

def speak(text):
    def run():
        global is_speaking
        is_speaking = True
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        is_speaking = False

    threading.Thread(target=run).start()
  

# Create continuous listener
def listen_loop():
    global is_speaking
    r = sr.Recognizer()

    while True:
        try:

            if is_speaking:
                continue
            with sr.Microphone() as source:
                print("Listening...")
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5, phrase_time_limit=5)

            word = r.recognize_google(audio).lower()
            print("Heard:", word)

            if "jarvis" in word:
                speak("Yes?")
                listen_command()

        except Exception:
            pass

# Separate command listener
def listen_command():
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source:
            print("Jarvis Active...")
            audio = r.listen(source)

        command = r.recognize_google(audio)
        print("Command:", command)

        processCommand(command)

    except Exception:
        speak("Sorry, I didn't catch that")


def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif "open chatgpt" in c.lower():
        webbrowser.open("https://chatgpt.com")
    elif "open github" in c.lower():
        webbrowser.open("https://github.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    

    # AI fallback (MOST IMPORTANT)
    else:
        speak("Thinking...")
        response = ask_ai(c)
        print(response)
        speak(response)
       

if __name__ == "__main__":
    speak("Initializing Jarvis")

    listener_thread = threading.Thread(target=listen_loop)
    listener_thread.daemon = True
    listener_thread.start()

    while True:
        pass