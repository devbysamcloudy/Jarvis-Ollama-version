import sounddevice as sd
import numpy as np
import io
import wave
import speech_recognition as sr
import pyttsx3
import ai


class VoiceAssistant:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, text):
        """Convert text to speech"""
        print(f"Jarvis: {text}")
        self.engine.say(text)
        self.engine.runAndWait()

    def listen(self, duration=5):
        """Record from microphone and convert to text"""
        fs = 16000  # Sample rate (16 kHz)

        print("Listening...")

        # Record audio from microphone
        recording = sd.rec(int(duration * fs), samplerate=fs, channels=1, dtype='int16')
        sd.wait()  # Wait for recording to finish

        wav_io = io.BytesIO()
        with wave.open(wav_io, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit = 2 bytes
            wav_file.setframerate(fs)
            wav_file.writeframes(recording.tobytes())

        wav_io.seek(0)  # Rewind to beginning

        # Use speech_recognition to recognize the audio
        r = sr.Recognizer()
        with sr.AudioFile(wav_io) as source:
            audio = r.record(source)

        try:
            # Use Google's free speech recognition
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
        """Send voice input to AI and speak response"""
        response = ai.ask_ai(user_input)
        self.speak(response)
        return response

_voice = VoiceAssistant()

def speak(text):
    return _voice.speak(text)

def listen(duration=5):
    return _voice.listen(duration)

def process_with_ai(user_input):
    return _voice.process_with_ai(user_input)