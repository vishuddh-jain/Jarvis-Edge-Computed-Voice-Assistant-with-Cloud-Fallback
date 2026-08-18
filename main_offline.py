import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import vosk  # <-- REQUIRED TO PARSE VOSK OUTPUT
from models.ai_assistant import ask_ai

# 2. Add this line to mute all the background C++ logs
vosk.SetLogLevel(-1)

# Initialize the speech engine once globally to prevent freezing
engine = pyttsx3.init()

def speak(text):
    # 1. Clean the text of AI markdown that crashes the voice engine
    clean_text = text.replace("*", "").replace("#", "")
    
    # 2. Break the massive paragraph into smaller sentences
    chunks = clean_text.split('\n')
    
    # 3. Queue up all the small sentences (DO NOT run and wait yet)
    for chunk in chunks:
        if chunk.strip():
            engine.say(chunk.strip())
            
    # 4. Command Windows to speak the entire queue, and wait until it's 100% finished
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
    elif c.lower().startswith("play"):
        try:
            song = c.lower().split(" ")[1]
            link = musicLibrary.music[song]
            webbrowser.open(link)
        except Exception:
            speak("I couldn't find that song in your library.")
    else:
        # speak("Thinking...")
        # response = ask_ai(c)
        # print("Ai: ", response)
        # speak(response)
        print("Thinking...") # Print instead of speak so we don't crash here
        response = ask_ai(c)
        print("Ai: ", response)
        # CLEAN THE TEXT: Remove asterisks and hashes that crash pyttsx3
        clean_response = response.replace("*", "").replace("#", "")
        speak(clean_response)

if __name__ == "__main__":
    speak("Initializing jarvis")
    r = sr.Recognizer()
    
    while True:
        print("Listening...")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            
            # 1. USE THE OFFLINE VOSK ENGINE
            # It automatically looks for the folder named 'model' in your directory
            word = r.recognize_vosk(audio)
                        
            if word:
                print(f"Heard: {word}")
            
            # 3. WAKE WORD DETECTION
            if "jarvis" in word.lower():
                speak("Yeah")
                print("Jarvis Active...")
                
                with sr.Microphone() as source:
                    audio = r.listen(source)
                
                command = r.recognize_vosk(audio)
                
                
                if command:
                    print(f"Command: {command}")
                    processCommand(command)

        except Exception as e:
            # STOP HIDING THE ERROR!
            print(f"CRITICAL MICROPHONE/SPEAKER ERROR: {e}")