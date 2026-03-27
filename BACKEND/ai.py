import requests
import json


class JarvisAI:
    OLLAMA_URL = "http://localhost:11434/api/chat"

    def ask_ai(self, user_input):
        try:
            print(f"Sending to local AI: {user_input}")

            response = requests.post(
                url=self.OLLAMA_URL,
                json={
                    "model": "llama3.2:1b",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are Jarvis, a helpful assistant. Keep responses brief and friendly."
                        },
                        {"role": "user", "content": user_input}
                    ],
                    "stream": False
                }
            )

            if response.status_code != 200:
                return f"Ollama Error: {response.status_code}"

            data = response.json()
            return data['message']['content']

        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Ollama. Is it running?"
        except Exception as e:
            return f"Error: {str(e)}"

_ai = JarvisAI()

def ask_ai(user_input):
    return _ai.ask_ai(user_input)