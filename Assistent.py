import sounddevice as sd
import vosk
import queue
import json
import requests
import os
from TTS.api import TTS
import soundfile as sf
from playsound import playsound


def callback(indata, frames, time, status):
    q.put(bytes(indata))


def listen():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")


def talk_to_ai(user_input):
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3",
        "prompt": f"You are an English tutor. Respond in simple English: {user_input}",
        "stream": False
    })

    res = r.json()
    return res.get('response', "I'm sorry, I couldn't generate a response.")
    

def speak(text):
    if len(text.strip()) < 10:
        print("⚠️ Texto muito curto para sintetizar.")
        return

    try:
        tts.tts_to_file(text=text, file_path="response.wav")
        if os.path.exists("response.wav"):
            playsound("response.wav")
        else:
            print("⚠️ Arquivo de áudio não foi criado.")
    except RuntimeError as e:
        print(f"Erro de execução ao sintetizar: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")



model = vosk.Model("vosk-model-en-us-0.22")
q = queue.Queue()
tts = TTS(model_name="tts_models/en/ljspeech/glow-tts", progress_bar=False)


while True:
    print("Listening...")
    user_input = listen()
    print("You said:", user_input)

    if user_input.strip() == "":
        continue
    if user_input.lower() in ["exit", "quit", "stop"]:
        break

    response = talk_to_ai(user_input)
    speak(response)