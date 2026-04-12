import sounddevice as sd
import numpy as np
import io
import wave
import speech_recognition as sr
import requests
import os
import re
import soundfile as sf
from dotenv import load_dotenv
import ai

load_dotenv()

ELEVENLABS_API_KEY = os.getenv("ELEVENLABS_API_KEY")
ELEVENLABS_URL = "https://api.elevenlabs.io/v1/text-to-speech"
VOICE_ID = "pNInz6obpgDQGcFmaJgB"  # Adam


def clean_text(text):
    emoji_pattern = re.compile(
        "[" u"\U0001F600-\U0001F64F" u"\U0001F300-\U0001F5FF"
        u"\U0001F680-\U0001F9FF" u"\U0001FA00-\U0001FA9F"
        u"\U00002700-\U000027BF" u"\U0001F1E0-\U0001F1FF"
        u"\U00002500-\U00002BEF" u"\U00010000-\U0010FFFF" "]+",
        flags=re.UNICODE
    )
    text = emoji_pattern.sub("", text)
    text = re.sub(r"\*+", "", text)
    text = re.sub(r"#+\s*", "", text)
    text = re.sub(r"`+", "", text)
    text = re.sub(r"_{2,}", "", text)
    text = re.sub(r"\[|\]|\(|\)", "", text)
    text = text.replace("%", " percent").replace("&", " and")
    text = re.sub(r"\s+", " ", text).strip()
    if len(text) > 400:
        text = text[:400] + "."
    return text


class VoiceAssistant:
    def speak(self, text):
        """Convert text to speech using ElevenLabs."""
        print(f"Jarvis: {text}")
        text = clean_text(text)
        if not text:
            return

        try:
            response = requests.post(
                f"{ELEVENLABS_URL}/{VOICE_ID}",
                headers={
                    "xi-api-key": ELEVENLABS_API_KEY,
                    "Content-Type": "application/json",
                },
                json={
                    "text": text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {
                        "stability": 0.4,
                        "similarity_boost": 0.75,
                        "style": 0.5,
                        "use_speaker_boost": True,
                    },
                },
                timeout=15,
            )

            if response.status_code == 200:
                # Play audio from bytes directly
                audio_bytes = io.BytesIO(response.content)
                data, samplerate = sf.read(audio_bytes)
                sd.play(data, samplerate)
                sd.wait()
            else:
                print(f"ElevenLabs error: {response.status_code} — {response.text}")

        except Exception as e:
            print(f"ElevenLabs speak failed: {e}")

    def listen(self, duration=5):
        """Record from microphone and convert to text."""
        fs = 16000
        print("Listening...")
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()

        wav_io = io.BytesIO()
        with wave.open(wav_io, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(fs)
            wav_file.writeframes(recording.tobytes())
        wav_io.seek(0)

        r = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio = r.record(source)

        try:
            command = r.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.UnknownValueError:
            print("Could not understand audio")
            return ""
        except sr.RequestError:
            print("Could not request results; check internet connection")
            return ""
        except Exception as e:
            print(f"Error: {e}")
            return ""

    def process_with_ai(self, user_input):
        response = ai.ask_ai(user_input)
        self.speak(response)
        return response


_voice = VoiceAssistant()

def speak(text): return _voice.speak(text)
def listen(duration=5): return _voice.listen(duration)
def process_with_ai(user_input): return _voice.process_with_ai(user_input)