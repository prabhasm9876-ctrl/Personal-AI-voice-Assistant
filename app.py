# Offline AI Voice Assistant (Optimized for Speed on AMD + Windows)
# Uses LM Studio (OpenAI-compatible API), Vosk STT, Piper/pyttsx3 TTS
# Non-streaming, short context, low tokens, GPU offload assumed via LM Studio

import json
import queue
import sounddevice as sd
import vosk
import requests
import pyttsx3

# =========================
# CONFIG (SPEED-CRITICAL)
# =========================
LM_STUDIO_API = "http://localhost:1234/v1/chat/completions"
MODEL_NAME = "phi-2"          # Fast model
MAX_TOKENS = 120               # Hard limit
TEMPERATURE = 0.7
TOP_P = 0.9
CONTEXT_SYSTEM_PROMPT = (
    "You are a fast offline assistant. "
    "Answer briefly in at most 4 sentences."
)

SAMPLE_RATE = 16000
VOSK_MODEL_PATH = "models/vosk-model-small-en-us"

# =========================
# TEXT TO SPEECH (FAST)
# =========================
engine = pyttsx3.init()
engine.setProperty('rate', 180)
engine.setProperty('volume', 1.0)

def speak(text: str):
    engine.say(text)
    engine.runAndWait()

# =========================
# SPEECH TO TEXT (VOSK)
# =========================
model = vosk.Model(VOSK_MODEL_PATH)
q = queue.Queue()

def audio_callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen_once():
    with sd.RawInputStream(
        samplerate=SAMPLE_RATE,
        blocksize=8000,
        dtype='int16',
        channels=1,
        callback=audio_callback
    ):
        recognizer = vosk.KaldiRecognizer(model, SAMPLE_RATE)
        print("Listening... Speak now")
        while True:
            data = q.get()
            if recognizer.AcceptWaveform(data):
                result = json.loads(recognizer.Result())
                text = result.get("text", "").strip()
                if text:
                    return text

# =========================
# LLM CALL (NON-STREAMING)
# =========================

import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "mistral"   # or phi, tinyllama, whatever you already pulled

def ask_llm(prompt):
    payload = {
        "model": MODEL,
        "prompt": prompt,
        "stream": False,
        "options": {
            "num_ctx": 2048,
            "num_predict": 200,
            "temperature": 0.7,
            "top_p": 0.9
        }
    }

    r = requests.post(OLLAMA_URL, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()["response"]

    response = requests.post(LM_STUDIO_API, json=payload, timeout=120)
    response.raise_for_status()
    data = response.json()                                              

    return data["choices"][0]["message"]["content"].strip()

# =========================
# MAIN LOOP
# =========================

def main():
    print("Offline AI Assistant ready (fast mode)")
    while True:
        user_text = listen_once()
        print("You:", user_text)

        if user_text.lower() in {"exit", "quit", "stop"}:
            speak("Goodbye")
            break

        answer = ask_llm(user_text)
        print("AI:", answer)
        speak(answer)


if __name__ == "__main__":
    main()
