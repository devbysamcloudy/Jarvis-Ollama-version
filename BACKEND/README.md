# JARVIS - Personal AI Assistant

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Installation Guide](#installation-guide)
- [Configuration](#configuration)
- [Usage Guide](#usage-guide)
- [Command Reference](#command-reference)
- [Troubleshooting](#troubleshooting)
- [Team Collaboration](#team-collaboration)
- [License](#license)

---

## Overview

JARVIS is a command-line personal AI assistant that helps you monitor your system, manage files, handle emails, and have natural conversations through text or voice. Built with Python, it demonstrates OOP principles, database integration, and clean CLI design.

Perfect for: System administrators, developers, students learning Python, or anyone wanting a customizable AI assistant.

---

## Features

### System Monitoring
- Real-time CPU usage
- RAM consumption tracking
- Battery status
- Disk space monitoring
- Running processes viewer

### File Management
- Organize files by type (Images, Documents, Code, etc.)
- Undo organization
- Open programs with voice/text
- Safe kill commands with security confirmation

### Email Integration
- Send emails via Gmail
- Read inbox
- Check unread count
- Multi-user support

### Voice Interaction
- Speech-to-text recognition
- Text-to-speech responses
- Natural language processing with local AI (Ollama)
- Voice mode activation

### User System
- Register/Login with password
- Each user has personal command history
- JSON-based storage
- One-to-many relationships (User → Commands, User → FileActions)

### AI Conversations
- Local AI using Ollama (no internet required)
- Natural language understanding
- Context-aware responses
- Customizable AI personality

---

## Project Structure
jarvis/
│
├── main.py # Main application entry point
├── ai.py # AI integration with Ollama
├── voice.py # Speech recognition and synthesis
├── system_info.py # System monitoring functions
├── weather.py # Weather API integration
├── file_organizer.py # File organization utilities
├── email_oauth.py # Email sending/reading
├── security.py # Command validation & safety
├── logger.py # Activity logging (class-based)
├── memory.py # User name memory
├── dashboard.py # CLI dashboard display
├── users.json # User credentials (created on first register)
├── [username]_data.json # Per-user command history
├── jarvis.log # Application logs
├── requirements.txt # Python dependencies
└── README.md # This file


---

## Installation Guide

### Prerequisites
- Python 3.10 or higher
- pip package manager
- Git (optional)

### Step 1: Clone the Repository
```bash
git clone https://github.com/yourusername/jarvis.git
cd jarvis
Step 2: Create Virtual Environment

Windows:

python -m venv venv
venv\Scripts\activate

macOS/Linux:

python3 -m venv venv
source venv/bin/activate

Step 3: Install Dependencies

Create requirements.txt:

psutil>=7.0.0
requests>=2.32.0
python-dotenv>=1.0.0
sounddevice>=0.5.0
numpy>=2.0.0
speechrecognition>=3.10.0
pyttsx3>=2.90
ollama>=0.6.0
imap-tools>=1.7.0
pip install -r requirements.txt


Step 4: Install Ollama (for AI)

Visit ollama.com
 to download and install.

Then pull a model:

ollama pull llama3.2:1b
Step 5: Set Up Environment Variables

Create a .env file:

WEATHER_API_KEY=your_openweather_api_key
EMAIL=your_email@gmail.com
PASSWORD=your_app_password

Note: For Gmail, use an App Password
 not your regular password.

Step 6: Run JARVIS
python main.py


Configuration
Ollama Models

Edit ai.py to change the model:

"model": "llama3.2:1b"  # Change to any installed model
Weather API

Get a free API key from OpenWeatherMap

Email Settings

For Gmail, enable 2-factor authentication and create an app password.

Usage Guide
First Time Users

Run python main.py

Type register to create an account

Login with your credentials

Start using commands!

Basic Workflow
> login              # Access your account
> cpu                # Check CPU usage
> organize Downloads # Organize your downloads folder
> weather London     # Check weather
> voice              # Activate voice mode
> logout             # Sign out
> exit               # Close JARVIS
Command Reference
Authentication
Command	Description
register	Create new account
login	Sign in to existing account
logout	Sign out
whoami	Show current user
System Info
Command	Description
cpu	Show CPU usage
battery	Show battery status
disk	Show disk usage
processes	List top CPU processes
File Operations
Command	Description
open [program]	Open a program (e.g., open chrome)
kill [process]	Terminate a process (e.g., kill notepad)
organize [folder]	Organize files in folder
undo	Undo last organization
Utilities
Command	Description
weather [city]	Get weather forecast
logs	View recent activity
voice	Activate voice mode
menu	Show dashboard
clear	Clear screen
exit	Quit JARVIS
Email (if configured)
Command	Description
send [to] | [subject] | [body]	Send email
inbox	Read recent emails
unread	Check unread count
AI Conversations

Any command not recognized is sent to the AI:

> tell me a joke
> what's the meaning of life
> how do I fix my computer
Troubleshooting
Common Issues & Solutions
Issue	Solution
ModuleNotFoundError	Run pip install -r requirements.txt
Ollama not found	Install Ollama and run ollama serve
Voice not working	Check microphone and install pyaudio
Email authentication failed	Use App Password, not regular password
users.json not creating	Check folder write permissions
kill command not working	Run terminal as administrator
Platform-Specific Notes

Windows:

Run as administrator for kill commands

Use venv\Scripts\activate

macOS:

Grant microphone permissions in System Settings

Use source venv/bin/activate

Linux:

sudo apt install portaudio19-dev espeak-ng
python3 -m venv venv
source venv/bin/activate
Voice Setup

If voice doesn't work:

# Windows
pip install pyaudio

# Linux
sudo apt install portaudio19-dev python3-pyaudio
pip install sounddevice

# macOS
brew install portaudio
pip install pyaudio
Team Collaboration
Git Workflow
# Clone repository
git clone https://github.com/yourteam/jarvis.git

# Create feature branch
git checkout -b feature/your-feature

# Commit changes
git add .
git commit -m "Add your feature"

# Push and create pull request
git push origin feature/your-feature
Project Management

Use GitHub Projects or Jira for task tracking

Assign issues to team members

Review code via pull requests

Document all functions with docstrings

Coding Standards

Follow PEP 8 guidelines

Write docstrings for all functions

Use meaningful variable names

Keep functions under 50 lines

Add comments for complex logic

Contributing

Fork the repository

Create a feature branch

Commit your changes

Push to the branch

Open a Pull Request

Guidelines

Write clear commit messages

Update documentation

Add tests if applicable

Ensure code passes linting

License

This project is for educational purposes. Feel free to modify and distribute with attribution.

Acknowledgments

OpenAI for inspiration

Ollama for local AI models

Python community for amazing libraries

Moringa School for project guidance

Contact

For questions or support:

Create an issue on GitHub

Contact your project lead

Check the documentation first

Enjoy your JARVIS assistant!
