JARVIS(FRONTEND-BACKEND)/
├── FRONTEND/React + Vite
│ ├── App.jsxauth flow
│ ├── index.html
│ ├── package.json
│ ├── vite.config.js
│ └── src/
│ ├── api.jsFlask connector
│ ├── index.css
│ ├── main.jsx
│ └── components/
│ ├── auth/new
│ │ ├── Login.jsx
│ │ ├── Register.jsx
│ │ ├── ProtectedRoute.jsx
│ │ └── Auth.css
│ ├── communication/
│ │ ├── ChatWindow.jsxcommands + AI
│ │ ├── VoiceFeedback.jsxupdated
│ │ └── Notifications.jsxDB connected
│ ├── core/
│ │ ├── JarvisCore.jsx
│ │ ├── Heartbeat.jsxreal ECG
│ │ ├── TaskRouter.jsx
│ │ └── CommandAnalyzer.jsx
│ ├── memory/
│ │ ├── Home.jsxweather widget
│ │ ├── History.jsxDB connected
│ │ └── SettingsPage.jsxDB connected
│ └── styles/
│ ├── App.cssfull rewrite
│ ├── Heartbeat.css
│ ├── variables.css
│ ├── animations.css
│ └── jarvis.css

└── BACKEND/Flask + Python
├── run.pyentry point
├── db.pyapp factory + Supabase
├── models.pyall DB tables
├── .envsecrets — not in git
├── INFO.mddocumentation
├── requirement.txt
├── routes/new
│ ├── __init__.py
│ ├── auth.pyregister, login, JWT
│ ├── commands.pyrun JARVIS commands
│ ├── history.pycommands + chat + files
│ ├── preferences.pyuser settings
│ ├── weather.pyOpenWeatherMap
│ └── notifications.pyalerts CRUD
├── ai.pyOllama gemma3:4b
├── file_organizer.pyOneDrive-aware
├── system_info.pyCPU, disk, battery
├── security.pycommand validation
├── voice.pyCLI voice
├── weather.pyCLI weather
├── logger.pyactivity logs
├── dashboard.pyCLI dashboard
└── main.pyCLI entry point