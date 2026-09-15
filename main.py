import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
from models.ai_assistant import ask_ai


r = sr.Recognizer()
# engine = pyttsx3.init()


def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()
  
  
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
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
        
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        link = musicLibrary.music[song]
        webbrowser.open(link)
    elif c.lower().startswith("fuck"):
        speak("thankyou buddy")

    # AI fallback (MOST IMPORTANT)
    else:
        speak("Thinking...")
        response = ask_ai(c)
        print("Ai: ", response)
        speak(response)
       

if __name__ == "__main__":
    speak("Initializing jarvis")
    while True:
        print("Listening...")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            
            if "jarvis" in text.lower():
                speak("Yes?")
                
                with sr.Microphone() as source:
                    audio = r.listen(source)
                command = r.recognize_google(audio)
                print(f"Command: {command}")
                
                speak("Thinking...")

                processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))
            



