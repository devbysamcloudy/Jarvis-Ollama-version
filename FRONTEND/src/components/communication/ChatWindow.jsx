//import React from 'react'
import React, { useState, useEffect, useRef } from "react";
import axios from "axios";
import { runCommand, saveChat } from "../../api";

const COMMANDS = [
  "cpu", "battery", "disk", "processes", "help",
  "open ", "kill ", "organize", "undo", "list files", "weather",
];

function isJarvisCommand(input) {
  const lower = input.trim().toLowerCase();
  return COMMANDS.some((cmd) => lower === cmd || lower.startsWith(cmd));
}

function ChatWindow() {
  const [msgs, setMsgs] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [ollamaStatus, setOllamaStatus] = useState("checking");
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [msgs]);

  useEffect(() => {
    const checkOllama = async () => {
      try {
        await axios.get("http://localhost:11434/api/tags", { timeout: 5000 });
        setOllamaStatus("running");
      } catch {
        setOllamaStatus("stopped");
      }
    };
    checkOllama();
  }, []);

  const addMsg = (role, content, type = "chat") => {
    setMsgs((prev) => [...prev, { role, content, type }]);
  };

  const handleSend = async () => {
    if (!input.trim()) return;

    const userInput = input.trim();
    addMsg("user", userInput);
    setInput("");
    setLoading(true);

    try {
      if (isJarvisCommand(userInput)) {
        // ── Send to Flask backend ──
        const data = await runCommand(userInput);
        const response = data.response || data.error || "No response";
        addMsg("assistant", response, data.type || "command");
        await saveChat(userInput, response, "command");

      } else {
        // ── Send to Ollama ──
        const response = await axios.post(
          "http://localhost:11434/api/generate",
          {
            model: "gemma3:4b",
            prompt: userInput,
            stream: false,
            options: { temperature: 0.7, num_predict: 500 },
          },
          { headers: { "Content-Type": "application/json" }, timeout: 45000 }
        );
        const aiResponse = response.data.response;
        addMsg("assistant", aiResponse, "ai");
        await saveChat(userInput, aiResponse, "chat");
      }

    } catch (err) {
      let errorMessage = `Error: ${err.message}`;
      if (err.message.includes("timeout")) {
        errorMessage = "The model is taking too long. Please try again.";
      }
      if (err.message.includes("Failed to fetch") || err.message.includes("Network")) {
        errorMessage = "Cannot connect to JARVIS backend. Is Flask running?";
      }
      addMsg("assistant", errorMessage, "error");
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const clearChat = () => setMsgs([]);

  const testConnection = async () => {
    setLoading(true);
    try {
      const response = await axios.get("http://localhost:11434/api/tags", { timeout: 5000 });
      alert(`Ollama running. Models: ${response.data.models.map((m) => m.name).join(", ")}`);
      setOllamaStatus("running");
    } catch (error) {
      alert(`Ollama connection failed: ${error.message}`);
      setOllamaStatus("stopped");
    } finally {
      setLoading(false);
    }
  };

  const getTypeLabel = (type) => {
    const labels = {
      command: "JARVIS",
      system:  "System",
      file:    "Files",
      ai:      "AI",
      error:   "Error",
      chat:    "JARVIS",
    };
    return labels[type] || "JARVIS";
  };

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="chat-title-container">
          <h2 className="chat-title">JARVIS Chat</h2>
          <div className="status-indicator">
            <span className={`status-dot status-${ollamaStatus}`}></span>
            <span className="status-text">
              {ollamaStatus === "running" ? "Ollama Connected" :
               ollamaStatus === "checking" ? "Connecting..." : "Ollama Offline"}
            </span>
          </div>
        </div>
        <div className="chat-controls">
          <button onClick={testConnection} disabled={loading} className="nav-button">
            Test Ollama
          </button>
          <button onClick={clearChat} disabled={loading} className="nav-button">
            Clear Chat
          </button>
        </div>
      </div>

      <div className="messages-window">
        {msgs.length === 0 ? (
          <div className="welcome-message">
            <p className="welcome-title">JARVIS is ready</p>
            <p className="welcome-subtitle">
              Type a command like <strong>cpu</strong>, <strong>organize desktop</strong>,{" "}
              <strong>open notepad</strong>, or just chat normally.
            </p>
            <div style={{ marginTop: "12px", fontSize: "13px", color: "#555570" }}>
              <strong>Commands:</strong> cpu · battery · disk · processes · open [app] ·
              kill [app] · organize [folder] · undo [folder] · weather [city] · help
            </div>
          </div>
        ) : (
          msgs.map((msg, idx) => (
            <div key={idx} className={`message-bubble ${msg.role}`}>
              <div className="message-sender">
                {msg.role === "user" ? "You" : getTypeLabel(msg.type)}
              </div>
              <div className="message-content">
                {msg.content.split("\n").map((line, i) => (
                  <p key={i} className="message-line">{line || <br />}</p>
                ))}
              </div>
            </div>
          ))
        )}
        <div ref={messagesEndRef} />
      </div>

      <div className="input-container">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type a command or chat message... (Enter to send)"
          disabled={loading}
          rows={3}
          className="chat-textarea"
        />
        <div className="input-controls">
          <div className="input-hint">
            {loading ? "Processing..." : "Enter to send · Shift+Enter for new line"}
          </div>
          <button
            onClick={handleSend}
            disabled={loading || !input.trim()}
            className={`send-button ${loading ? "loading" : ""}`}
          >
            {loading ? "Thinking..." : "Send"}
          </button>
        </div>
      </div>

      <div className="chat-footer">
        <div className="model-info">
          <span className="model-label">AI Model:</span>
          <span className="model-name">gemma3:4b</span>
        </div>
        <div className="connection-info">
          <span className="connection-label">Backend:</span>
          <span className="connection-url">localhost:5000</span>
        </div>
      </div>
    </div>
  );
}

export default ChatWindow;
