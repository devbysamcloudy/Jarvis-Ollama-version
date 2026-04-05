# JARVIS — Full Stack AI Assistant
## Project Documentation

---

## Overview

JARVIS (Just A Rather Very Intelligent System) is a full-stack AI-powered personal assistant built with a React frontend and a Flask backend, connected to a PostgreSQL cloud database (Supabase). It supports voice interaction, system commands, file organization, AI chat, weather updates, and user authentication.

---

## Project Structure

```
JARVIS(FRONTEND-BACKEND)/
├── FRONTEND/                        # React + Vite web application
│   ├── src/
│   │   ├── components/
│   │   │   ├── auth/
│   │   │   │   ├── Login.jsx        # Login form connected to Flask JWT auth
│   │   │   │   ├── Register.jsx     # Registration form with validation
│   │   │   │   ├── ProtectedRoute.jsx  # Route guard for authenticated users
│   │   │   │   └── Auth.css         # Auth page styling
│   │   │   ├── communication/
│   │   │   │   ├── ChatWindow.jsx   # AI chat + JARVIS command interface
│   │   │   │   ├── VoiceFeedback.jsx # Voice recognition + speech synthesis
│   │   │   │   └── Notifications.jsx # Real-time notifications from DB
│   │   │   ├── core/
│   │   │   │   ├── JarvisCore.jsx   # Core JARVIS logic
│   │   │   │   ├── Heartbeat.jsx    # Real ECG heartbeat monitor (Canvas)
│   │   │   │   ├── TaskRouter.jsx   # Routes tasks to appropriate handlers
│   │   │   │   └── CommandAnalyzer.jsx # Analyzes user commands
│   │   │   ├── memory/
│   │   │   │   ├── Home.jsx         # Dashboard with weather widget
│   │   │   │   ├── History.jsx      # Command + chat history from DB
│   │   │   │   └── SettingsPage.jsx # User preferences saved to DB
│   │   │   └── styles/
│   │   │       ├── App.css          # Main stylesheet (all components)
│   │   │       ├── Heartbeat.css    # ECG monitor styles
│   │   │       ├── variables.css    # CSS custom properties
│   │   │       ├── animations.css   # Global animations
│   │   │       └── jarvis.css       # JARVIS HUD styles
│   │   ├── api.js                   # Centralized Flask API connector
│   │   ├── main.jsx                 # React entry point
│   │   └── index.css                # Base styles
│   ├── App.jsx                      # Root component with auth flow
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
│
└── BACKEND/                         # Flask Python backend
    ├── run.py                       # Application entry point
    ├── db.py                        # Database + app factory (create_app)
    ├── models.py                    # SQLAlchemy database models
    ├── .env                         # Environment variables (not in git)
    ├── routes/
    │   ├── __init__.py
    │   ├── auth.py                  # Register, login, logout, /me
    │   ├── history.py               # Command history, chat history, file actions
    │   ├── preferences.py           # Get and update user preferences
    │   ├── commands.py              # Execute JARVIS commands via API
    │   ├── weather.py               # Weather data from OpenWeatherMap
    │   └── notifications.py         # Notifications CRUD
    ├── ai.py                        # Ollama local AI integration
    ├── voice.py                     # Voice recognition (CLI)
    ├── system_info.py               # CPU, battery, disk, processes
    ├── file_organizer.py            # Smart file organization by type
    ├── weather.py                   # Weather CLI module
    ├── security.py                  # Command validation and safety checks
    ├── logger.py                    # Activity logging
    ├── dashboard.py                 # CLI dashboard
    ├── memory.py                    # User memory module
    └── requirement.txt              # Python dependencies
```

---

## What Was Built

### 1. Authentication System
- User registration with hashed passwords (bcrypt)
- JWT token-based login — tokens stored in localStorage
- Protected routes — app only loads after login
- Auto-login on page refresh using saved token and user data
- Logout clears token and redirects to login

### 2. Database (Supabase PostgreSQL)
Connected via SQLAlchemy ORM. Tables created automatically on startup.

| Table | Purpose |
|---|---|
| `users` | Stores user accounts with hashed passwords |
| `sessions` | JWT session tracking |
| `preferences` | Per-user settings (theme, city, AI model, voice) |
| `command_history` | Every CLI/web command with response and type |
| `chat_history` | All AI conversations with tokens used |
| `file_actions` | File organize/undo actions with paths |
| `notifications` | System and AI alerts per user |

### 3. JARVIS Command System
Commands typed in chat are routed to Flask `/api/commands/run`. Supported commands:

| Command | Action |
|---|---|
| `cpu` | Shows current CPU usage |
| `battery` | Shows battery status |
| `disk` | Shows disk usage |
| `processes` | Lists top CPU processes |
| `open [app]` | Opens a program (e.g. `open notepad`) |
| `kill [app]` | Terminates a process (e.g. `kill chrome`) |
| `organize [folder]` | Organizes files by type in any folder |
| `organize desktop` | Organizes the Desktop (OneDrive-aware) |
| `organize downloads` | Organizes the Downloads folder |
| `undo [folder]` | Restores files from organized folders |
| `list files [folder]` | Lists all files in a folder |
| `weather [city]` | Gets live weather for any city |
| `logs` | Shows last 10 lines from jarvis.log |
| `help` | Lists all available commands |
| Anything else | Sent to Ollama AI (gemma3:4b) |

All commands are saved to the database with timestamp, type, response, and success status.

### 4. File Organizer
Upgraded from the original CLI-only version:
- Accepts any folder path or shortcut (`desktop`, `downloads`, `documents` etc.)
- **OneDrive-aware** — automatically detects OneDrive Desktop path
- Organizes into: Images, Documents, Music, Videos, Archives, Code, Others
- Full undo support — restores files and removes empty folders
- Returns structured JSON for the React frontend to display

### 5. Weather Integration
- Live weather from OpenWeatherMap API
- Displayed on the Home dashboard with icon, temperature, description, humidity, wind
- City search — user can search any city from the dashboard
- Weather command also works in chat (`weather Nairobi`)
- API key stored securely in `.env`

### 6. Voice Assistant
- Uses browser Web Speech API (SpeechRecognition + SpeechSynthesis)
- Voice commands routed through Flask backend — same as typed commands
- Deep voice output with pitch and rate tuned for JARVIS feel
- Pulsing orb UI — blue (idle), green (listening), purple (speaking)
- Session history shown below the orb
- Test voice button to unlock browser audio

### 7. Real ECG Heartbeat Monitor
- Canvas-based real ECG waveform (P wave, QRS complex, T wave)
- Scrolling animation synced to BPM
- BPM slider (40–180)
- Alert mode — turns red with sharper waveform
- Glowing cyan line with grid background

### 8. History Page
- Two tabs: Commands and Chat
- Loads from Supabase database
- Shows command type, response preview, timestamp, success status
- Clear all commands button
- Refresh button

### 9. Settings Page
- Loads preferences from database on mount
- Editable: theme, city, AI model, language, voice toggle, notifications toggle
- Saves back to database via PATCH request
- Confirmation message on save

### 10. Notifications Page
- Loads from database
- Filter by: all, unread, info, success, warning, error
- Mark as read, delete individual, clear all
- Unread count badge on title

---

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/auth/register` | Create account |
| POST | `/api/auth/login` | Login, returns JWT token |
| GET | `/api/auth/me` | Get current user |
| POST | `/api/auth/logout` | Logout |
| POST | `/api/commands/run` | Run a JARVIS command |
| GET | `/api/history/commands` | Get command history |
| POST | `/api/history/commands` | Save a command |
| DELETE | `/api/history/commands` | Clear command history |
| GET | `/api/history/chat` | Get chat history |
| POST | `/api/history/chat` | Save a chat message |
| GET | `/api/history/files` | Get file actions |
| POST | `/api/history/files` | Save a file action |
| GET | `/api/preferences/` | Get preferences |
| PATCH | `/api/preferences/` | Update preferences |
| GET | `/api/weather/` | Get weather for a city |
| GET | `/api/notifications/` | Get notifications |
| PATCH | `/api/notifications/<id>/read` | Mark notification as read |
| DELETE | `/api/notifications/<id>` | Delete a notification |
| DELETE | `/api/notifications/` | Clear all notifications |

---

## Environment Variables (.env)

```
WEATHER_API_KEY=your_openweathermap_key
DATABASE_URL=postgresql://postgres.xxxx:password@aws-x-xx.pooler.supabase.com:5432/postgres
JWT_SECRET_KEY=your-secret-key
```

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 18, Vite, JavaScript |
| Backend | Python, Flask, Flask-SQLAlchemy |
| Database | PostgreSQL (Supabase cloud) |
| Auth | Flask-JWT-Extended, Flask-Bcrypt |
| AI | Ollama (gemma3:4b — runs locally) |
| Voice | Web Speech API (browser-native) |
| Weather | OpenWeatherMap API |
| Styling | Custom CSS with CSS variables |
| HTTP | Fetch API (frontend), Requests (backend) |

---

## How to Run

### Backend
```bash
cd BACKEND
pip install -r requirement.txt
python run.py
# Runs on http://localhost:5000
```

### Frontend
```bash
cd FRONTEND
npm install
npm run dev
# Runs on http://localhost:5173
```

### Ollama (for AI chat)
```bash
ollama serve
ollama pull gemma3:4b
```

---

## Developer

**Samuel** — Full Stack Developer  
GitHub: `devbysamcloudy`  
School: Moringa School, Nairobi  
Expected Graduation: July 2026
