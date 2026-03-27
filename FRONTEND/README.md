# JARVIS AI Assistant

A React-based AI assistant inspired by JARVIS. This app combines **chat, voice, command routing, notifications, and history tracking**, powered by **Oloma AI** or a local Ollama server. It also includes simple **Email, File, and System management** modules.

---

## Features

- Chat with AI using Oloma AI API (`gpt-4o-mini` or `gemma3:4b`)  
- Voice commands using Web Speech API (speech recognition & synthesis)  
- Command routing for emails, files, and system tasks  
- History tracker for past commands  
- Notifications system for alerts  
- Configurable settings and preferences  

---

## Tech Stack

- **Frontend:** React, JavaScript, HTML, CSS  
- **AI Backend:** Oloma AI API or local Ollama server  
- **Browser APIs:**  
  - SpeechRecognition for voice input  
  - SpeechSynthesis for voice output  

---

## Installation

1. Clone the repo:

```bash
git clone https://github.com/yourusername/jarvis-react.git
cd jarvis-react

Install dependencies:

npm install


Configure API Key:

Create a .env file based on .env.example

Add your OpenAI / Oloma API key:

VITE_OPENAI_KEY=your_api_key_here


Start the app:

npm run dev


Open http://localhost:5173
 in your browser.

Usage

Mode Selection:

Chat → normal AI conversation

Command → route instructions (emails, files, system)

Voice → speak to JARVIS

Quick Actions: Check email, list files, or system status using buttons.

Command prefix: Use / for command mode, e.g., /check emails.

Settings: Enable/disable voice assistant, configure preferences.

Commands & Managers

Email Commands:

send email → Sends an email

check emails → Shows inbox summary

delete email → Deletes spam or selected emails

File Commands:

list files → Shows all files in a directory

search files → Search for specific files

create file → Creates a new file

System Commands:

system status → Shows CPU, memory, disk, network, uptime

Help Command:

/help → Lists available commands

Task routing is handled by TaskRouter.js, which calls the respective manager.

Voice Interaction

Click Voice button to start voice mode

Speak commands or chat → JARVIS converts speech to text

JARVIS responds vocally using SpeechSynthesis

Auto-listening ensures continuous interaction

Notifications & History

Notifications.jsx: Displays alerts, new messages, and system notifications

History.jsx: Tracks past commands with timestamp and delete/clear functionality

Settings & Preferences

Enable/disable voice assistant

Manage assistant behavior using React Context (AssistantContext and TaskContext)

Preferences are global and persist across components

Project Structure
src/
├── components/
│   ├── ChatWindow.jsx
│   ├── JARVISCore.jsx
│   ├── VoiceFeedback.jsx
│   ├── History.jsx
│   ├── Notifications.jsx
│   ├── Preferences.jsx
│   └── App.jsx
├── contexts/
│   ├── AssistantContext.jsx
│   └── TaskContext.jsx
├── helpers/
│   ├── CommandAnalyzer.jsx
│   └── TaskRouter.jsx
├── managers/
│   ├── EmailManager.js
│   ├── FileManager.js
│   └── SystemStatus.js
├── styles/
│   └── app.css
└── main.jsx

Contributing

Fork the repo

Create a branch (git checkout -b feature/new-feature)

Commit your changes (git commit -m "Add feature")

Push to branch (git push origin feature/new-feature)

Open a pull request

License

This project is MIT licensed. See LICENSE for details.
