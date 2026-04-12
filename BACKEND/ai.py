import requests
import os
from dotenv import load_dotenv

load_dotenv()

class JarvisAI:
    GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
    API_KEY = os.getenv("GROQ_API_KEY")

    def ask_ai(self, user_input):
        try:
            print(f"Sending to Groq: {user_input}")

            response = requests.post(
                url=self.GROQ_URL,
                headers={
                    "Authorization": f"Bearer {self.API_KEY}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "llama-3.1-8b-instant",
                    "messages": [
                        {
                            "role": "system",
                            "content": "You are Jarvis, a helpful AI assistant. Keep responses brief and friendly."
                        },
                        {"role": "user", "content": user_input}
                    ],
                    "temperature": 0.7,
                    "max_tokens": 500
                },
                timeout=30
            )

            if response.status_code != 200:
                return f"Groq Error: {response.status_code} — {response.text}"

            data = response.json()
            return data["choices"][0]["message"]["content"]

        except requests.exceptions.ConnectionError:
            return "Error: Cannot connect to Groq. Check your internet connection."
        except requests.exceptions.Timeout:
            return "Error: Groq timed out. Try again."
        except Exception as e:
            return f"Error: {str(e)}"


_ai = JarvisAI()

def ask_ai(user_input):
    return _ai.ask_ai(user_input)