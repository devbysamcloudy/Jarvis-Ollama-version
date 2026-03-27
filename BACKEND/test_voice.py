import voice

print("Testing voice...")
voice.speak("Hello, I am Jarvis. Please say something.")

command = voice.listen()
if command:
    voice.speak(f"You said: {command}")
else:
    voice.speak("I didn't hear anything")