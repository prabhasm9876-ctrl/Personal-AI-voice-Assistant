from ollama_client import ask_ollama
from tts_test import test_tts_engine as speak

while True:
    user = input("You: ")
    if user.lower() in ["exit", "quit"]:
        break

    reply = ask_ollama(user)
    print("AI:", reply)
    speak(reply)
