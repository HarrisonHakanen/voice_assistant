import sounddevice as sd
import vosk
import queue
import json
import requests
import os
from TTS.api import TTS
import soundfile as sf
from playsound import playsound
from pydub import AudioSegment
import re
import uuid


initial_context = (
    "You are an English tutor. "
    "Your goal is to help the user practice English conversation "
    "in simple and encouraging language."
)


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


def talk_to_ai(user_input, context=initial_context):
    full_prompt = context + " User says: " + user_input
    r = requests.post("http://localhost:11434/api/generate", json={
        "model": "gemma3",
        "prompt": full_prompt,
        "stream": False
    })
    res = r.json()
    return res.get('response', "I'm sorry, I couldn't generate a response.")
    

def speak(text_list):
    try:
        combined = AudioSegment.silent(duration=0)

        for sentence in text_list:
            clean = sentence.strip()
            if len(clean) < 5 or not re.search(r'[a-zA-Z0-9]', clean):
                print(f"Ignorado: '{clean}'")
                continue

            try:
                temp_path = f"temp_{uuid.uuid4().hex}.wav"
                tts.tts_to_file(text=clean, file_path=temp_path)
                audio_segment = AudioSegment.from_wav(temp_path)
                os.remove(temp_path)

            except Exception as e:
                print(f"Erro na frase '{clean}': {e}")
                # Sintetizar frase padrão de erro
                error_temp = f"temp_error_{uuid.uuid4().hex}.wav"
                tts.tts_to_file(text="Sorry, I couldn't understand that sentence.", file_path=error_temp)
                audio_segment = AudioSegment.from_wav(error_temp)
                os.remove(error_temp)

            combined += audio_segment

        combined.export("response.wav", format="wav")
        playsound("response.wav")

    except Exception as e:
        print(f"Erro geral ao sintetizar: {e}")


def split_into_sentences(text):
    return re.split(r'(?<=[.!?]) +', text)
    


model = vosk.Model("vosk-model-en-us-0.22")
q = queue.Queue()
tts = TTS(model_name="tts_models/en/ljspeech/glow-tts", progress_bar=True)



while True:
    print("Listening...")
    user_input = listen()
    print("You said:", user_input)

    if user_input.strip() == "":
        continue
    if user_input.lower() in ["exit", "quit", "stop"]:
        break

    response = talk_to_ai(user_input)
    print(response)

    sentences = split_into_sentences(response)
    speak(sentences)


