import speech_recognition as sr
import pyttsx3
import requests

# Point this to your live FastAPI server on EC2
TEST_EC2_URL = "http://ec2-3-110-158-125.ap-south-1.compute.amazonaws.com:8000/ask"

# 1. INITIALIZE THE ENGINE ONCE GLOBALLY
engine = pyttsx3.init()

def test_speak(text):
    # 2. ONLY COMMAND IT TO SPEAK, DO NOT RE-INITIALIZE
    engine.say(text)
    engine.runAndWait()

def test_listen_and_send():
    r = sr.Recognizer()
    test_speak("Initializing Test Jarvis")
    
    while True:
        print("Listening...")
        try:
            with sr.Microphone() as source:
                r.adjust_for_ambient_noise(source, duration=0.5)
                audio = r.listen(source, timeout=5, phrase_time_limit=5)
            
            text = r.recognize_google(audio)
            print(f"You said: {text}")
            
            if "jarvis" in text.lower():
                test_speak("Yes?")
                
                with sr.Microphone() as source:
                    audio = r.listen(source)
                command = r.recognize_google(audio)
                print(f"Command: {command}")
                
                test_speak("Thinking...")
                
                # Send the request to FastAPI
                response = requests.post(TEST_EC2_URL, json={"prompt": command})
                ai_reply = response.json().get("reply", "Sorry, error reaching test server.")
                
                print(f"Jarvis: {ai_reply}")
                test_speak(ai_reply)

        except Exception as e:
            print(f"Error Occurred: {e}")

if __name__ == "__main__":
    test_listen_and_send()