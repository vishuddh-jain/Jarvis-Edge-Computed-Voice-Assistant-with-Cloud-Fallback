import ollama
import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def ask_ai(prompt):
    print("⚡ Attempting cloud fast-lane (Groq)...")
    
    try:
        # 1. TRY THE INTERNET FIRST
        client = Groq()
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model="llama-3.1-8b-instant",
            timeout=10.0  # Increased to 10 seconds to allow for connection time
        )
        return chat_completion.choices[0].message.content
        
    except Exception as cloud_error: # <--- This defines the variable!
        # 2. INTERNET FAILED, AUTO-FALLBACK TO LOCAL OLLAMA
        print(f"Cloud unreachable. Reason: {cloud_error}")
        print("Rerouting to offline secure vault (Ollama)...")
        
        try:
            response = ollama.chat(
                model='qwen2.5:0.5b',
                messages=[{"role": "user", "content": prompt}]
            )
            return response['message']['content']
            
        except Exception as local_error:
            # 3. BOTH FAILED
            print(f"Local Error: {local_error}")
            return "Critical error. Both cloud and local neural networks are currently offline."
