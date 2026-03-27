import { useState } from "react";

import ChatWindow from "./src/components/communication/ChatWindow";
import VoiceFeedback from "./src/components/communication/VoiceFeedback";
import Notifications from "./src/components/communication/Notifications";

import Home from "./src/components/memory/Home.jsx";
import History from "./src/components/memory/History.jsx";
import JARVISCore from "./src/components/core/JarvisCore.jsx";
import SettingsPage from "./src/components/memory/SettingsPage.jsx";
import Tasks from "./src/components/core/TaskRouter.jsx";
import Heartbeat from "./src/components/core/Heartbeat.jsx";

import Login from "./src/components/auth/Login.jsx";
import Register from "./src/components/auth/Register.jsx";

import "./src/components/styles/variables.css";
import "./src/components/styles/animations.css";
import "./src/components/styles/App.css";
import "./src/components/styles/jarvis.css";
import "./src/components/auth/Auth.css";

function App() {
  const [currentPage, setCurrentPage] = useState("home");
  const [active, setActive] = useState(false);
  const [user, setUser] = useState(null);
  const [authPage, setAuthPage] = useState("login"); // "login" | "register"

  const handleLogin = (userData) => {
    setUser(userData);
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    setUser(null);
    setAuthPage("login");
  };

  

  // Show login or register if not logged in
  if (!user) {
    if (authPage === "register") {
      return (
        <Register
          onLogin={handleLogin}
          switchToLogin={() => setAuthPage("login")}
        />
      );
    }
    return (
      <Login
        onLogin={handleLogin}
        switchToRegister={() => setAuthPage("register")}
      />
    );
  }

  function renderPage() {
    if (currentPage === "home") {
      return <Home />;
    } else if (currentPage === "history") {
      return <History />;
    } else if (currentPage === "settings") {
      return <SettingsPage />;
    } else if (currentPage === "chat") {
      return <ChatWindow />;
    } else if (currentPage === "voice") {
      return <VoiceFeedback />;
    } else if (currentPage === "notifications") {
      return <Notifications />;
    }
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1 className="app-title">JARVIS Assistant</h1>
        <div className="user-info">
          <span className="user-greeting">Welcome, {user.display_name || user.username}</span>
          <button className="logout-btn" onClick={handleLogout}>Logout</button>
        </div>
      </header>

      <nav className="app-nav">
        <button className="nav-button" onClick={() => setCurrentPage("home")}>Home</button>
        <button className="nav-button" onClick={() => setCurrentPage("chat")}>Chat</button>
        <button className="nav-button" onClick={() => setCurrentPage("voice")}>Voice</button>
        <button className="nav-button" onClick={() => setCurrentPage("notifications")}>Notifications</button>
        <button className="nav-button" onClick={() => setCurrentPage("history")}>History</button>
        <button className="nav-button" onClick={() => setCurrentPage("settings")}>Settings</button>

        <button
          className={`jarvis-rotating-button ${active ? "active" : "inactive"}`}
          onClick={() => setActive(!active)}
        >
          {active ? "ACTIVE" : "DEACTIVE"}
          <div className="jarvis-circle jarvis-circle1"></div>
          <div className="jarvis-circle jarvis-circle2"></div>
        </button>

        <div className="heartbeat-container">
          <div className="heartbeat">
            <div className="ecg-line"></div>
          </div>
        </div>
      </nav>

      <Tasks />
      <Heartbeat />
      <JARVISCore />

      <hr className="divider" />

      <div>
        {renderPage()}
      </div>
    </div>
  );
}

export default App;
