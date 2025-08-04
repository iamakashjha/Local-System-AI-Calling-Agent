import whisper
import sounddevice as sd
import numpy as np
import json

model = whisper.load_model("small") 

def recognize_from_mic(timeout=5):
    samplerate = 16000
    print("Listening...")
    recording = sd.rec(int(timeout * samplerate), samplerate=samplerate, channels=1, dtype='float32')
    sd.wait()
    audio = np.squeeze(recording)
    result = model.transcribe(audio, fp16=False, language="en")
    return result["text"].strip()