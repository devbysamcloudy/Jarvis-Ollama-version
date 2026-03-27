import json
import os

class Memory:
    MEMORY_FILE = "memory.json"

    def __init__(self):
        self.user_name = None
        self._load_memory()

    def _load_memory(self):
        if os.path.exists(self.MEMORY_FILE):
            try:
                with open(self.MEMORY_FILE, 'r') as f:
                    data = json.load(f)
                    self.user_name = data.get('name')
            except:
                pass

    def set_name(self, name):
        self.user_name = name
        return f"I'll call you {name}"

    def get_name(self):
        return self.user_name if self.user_name else "unknown"

    def greet(self):
        if self.user_name:
            return f"Hello {self.user_name}"
        else:
            return "Hello. What's your name?"

_memory = Memory()

def set_name(name):
    return _memory.set_name(name)

def get_name():
    return _memory.get_name()

def greet():
    return _memory.greet()