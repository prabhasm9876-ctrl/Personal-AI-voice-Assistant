import queue
import sounddevice as sd
import vosk
import json
import os
import sys

# ---------- PATH SETUP ----------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "models", "vosk-model-small-en-us")

if not os.path.exists(MODEL_PATH):
    print("ERROR: Vosk model not found at:", MODEL_PATH)
    sys.exit(1)

# ---------- MODEL LOAD ----------
model = vosk.Model(MODEL_PATH)
q = queue.Queue()

# ---------- AUDIO CALLBACK ----------
def callback(indata, frames, time, status):
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# ---------- LISTEN FUNCTION ----------
def listen():
    rec = vosk.KaldiRecognizer(model, 16000)

    with sd.RawInputStream(
        samplerate=16000,
        blocksize=8000,
        dtype="int16",
        channels=1,
        callback=callback
    ):
        print("Listening... Speak now")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")

# ---------- TEST ----------
if __name__ == "__main__":
    text = listen()
    print("You said:", text)
