import React, { useState, useEffect, useRef } from "react";
import TaskRouter from "./TaskRouter";

function JARVISCore() {
  // State for all communication
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [mode, setMode] = useState("chat"); // chat, command, voice
  const [ollamaStatus, setOllamaStatus] = useState("checking");
  
  // Voice recognition
  const [listening, setListening] = useState(false);
  const [isSpeaking, setIsSpeaking] = useState(false);
  const recognitionRef = useRef(null);

  const OLLAMA_BASE_URL = "http://localhost:11434";
  const OLLAMA_MODEL = "gemma3:4b";

    // Check Ollama connection on mount
  useEffect(() => {
    checkOllamaConnection();
  }, []);

  async function checkOllamaConnection() {
    try {
      const response = await fetch(`${OLLAMA_BASE_URL}/api/tags`);
      if (response.ok) setOllamaStatus("connected");
      else setOllamaStatus("disconnected");
    } catch (err) {
      setOllamaStatus("disconnected");
    }
  }

  function CommandAnalyzer(command) {
    const cleanCommand = command.toLowerCase();
    
    if (cleanCommand.includes("email") || cleanCommand.includes("mail")) {
      return "Email functionality is available. Try: 'check emails' or 'send email'";
    } else if (cleanCommand.includes("file") || cleanCommand.includes("document")) {
      return "File functionality is available. Try: 'list files' or 'organize files'";
    } else if (cleanCommand.includes("system") || cleanCommand.includes("status")) {
      return "System status functionality is available. Try: 'system status'";
    } else if (cleanCommand.includes("help") || cleanCommand.includes("what can you do")) {
      return getCommandHelp();
    } else {
      return "I'm not sure how to process that command. Try asking for /help";
    }
  }

  async function handleInput(userInput) {
    if (!userInput.trim()) return;
    
    // Add user message
    const userMsg = { role: "user", content: userInput, type: mode };
    setMessages(prev => [...prev, userMsg]);
    setLoading(true);

    try {
      let response;
      
      if (mode === "command" || userInput.startsWith("/")) {
        // Process as command
        response = await processCommand(userInput);
      } else {
        // Process as chat (AI response)
        response = await getAIResponse(userInput);
      }
      
      // Add AI/System response
      const systemMsg = { 
        role: "assistant", 
        content: response, 
        type: mode 
      };
      setMessages(prev => [...prev, systemMsg]);

      // Speak if in voice mode
      if (mode === "voice") {
        await speakText(response);
      }
      
    } catch (error) {
      console.error("Error:", error);
      const errorMsg = { 
        role: "system", 
        content: `Error: ${error.message}`,
        type: "error" 
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
      setInput("");
    }
  }

  // AI RESPONSE (OLLAMA)
  async function getAIResponse(prompt) {
    try {
      const response = await fetch(`${OLLAMA_BASE_URL}/api/generate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          model: OLLAMA_MODEL,
          prompt: prompt,
          stream: false,
          options: { temperature: 0.7, num_predict: 500 }
        }),
      });

      const data = await response.json();
      return data.response || "No response from AI.";
    } catch (error) {
      console.error("Ollama error:", error);
      throw error;
    }
  }

  // COMMAND PROCESSING 
  async function processCommand(command) {
  const cleanCommand = command.replace(/^\//, '');
  
  // First try Ollama for intelligent command understanding
  try {
    const aiResponse = await getAIResponse(
      `Analyze this command and return ONLY the task category: "${cleanCommand}". ` +
      `Categories: email, file, system, status, help, other.`
    );
    
    const category = aiResponse.toLowerCase().trim();
    
    // Route to appropriate handler - NO "await" before TaskRouter
    if (category.includes("email")) {
      return TaskRouter(`email ${cleanCommand}`);  // NO "await"
    } else if (category.includes("file")) {
      return TaskRouter(`file ${cleanCommand}`);  // NO "await"
    } else if (category.includes("system") || category.includes("status")) {
      return TaskRouter("status");  // NO "await"
    } else if (category.includes("help")) {
      return getCommandHelp();
    } else {
      // Let Ollama handle general commands
      return await getAIResponse(
        `As JARVIS assistant, respond to this command: "${cleanCommand}". ` +
        `Be helpful and concise.`
      );
    }
  } catch (error) {
    // Fallback to basic command analyzer
    return CommandAnalyzer(cleanCommand);
  }
}

  function getCommandHelp() {
    return `Available commands:
    • Email: "check emails", "send email", "organize inbox"
    • Files: "list files", "delete file", "organize files"
    • System: "system status", "check status"
    • Chat: Normal conversation
    • Voice: Click voice mode to speak
    Prefix with / for command mode, e.g., "/check emails"`;
  }

  // VOICE FUNCTIONS
  function startVoiceMode() {
    if (ollamaStatus !== "connected") {
      alert("Ollama not connected. Please start Ollama service.");
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Browser doesn't support voice recognition.");
      return;
    }

    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognitionRef.current = recognition;

    recognition.onstart = () => {
      setListening(true);
      setMode("voice");
    };

    recognition.onresult = async (e) => {
      const transcript = e.results[0][0].transcript;
      setInput(transcript);
      await handleInput(transcript);
      setListening(false);
    };

    recognition.onend = () => {
      setListening(false);
    };

    recognition.start();
  }

  function speakText(text) {
    return new Promise((resolve) => {
      if (!text.trim()) {
        resolve();
        return;
      }

      setIsSpeaking(true);
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.85;
      utterance.pitch = 0.75;

      utterance.onend = () => {
        setIsSpeaking(false);
        resolve();
      };

      window.speechSynthesis.speak(utterance);
    });
  }

  //RENDER
  return (
    <div className="jarvis-core">
      <div className="status-bar">
        <div className="status-item">
          <span className={`status-dot status-${ollamaStatus}`}></span>
          Ollama: {ollamaStatus === "connected" ? "Connected" : "Disconnected"}
        </div>
        <div className="status-item">
          <span className={`status-dot ${listening ? 'listening' : ''}`}></span>
          Voice: {listening ? "Listening..." : "Ready"}
        </div>
        <div className="status-item">
          Mode: <strong>{mode.toUpperCase()}</strong>
        </div>
      </div>

      
      <div className="mode-selector">
        <button 
          onClick={() => setMode("chat")}
          className={mode === "chat" ? "active" : ""}
        >
           Chat
        </button>
        <button 
          onClick={() => setMode("command")}
          className={mode === "command" ? "active" : ""}
        >
           Commands
        </button>
        <button 
          onClick={startVoiceMode}
          className={mode === "voice" ? "active" : ""}
          disabled={listening || isSpeaking}
        >
           {listening ? "Listening..." : "Voice"}
        </button>
      </div>

      <div className="messages-container">
        {messages.length === 0 ? (
          <div className="welcome-message">
            <h3>JARVIS Assistant</h3>
            <p>Select a mode above to start interacting.</p>
            <p>• Chat: Normal conversation with AI</p>
            <p>• Commands: Control email, files, system</p>
            <p>• Voice: Speak to JARVIS</p>
          </div>
        ) : (
          messages.map((msg, idx) => (
            <div key={idx} className={`message ${msg.role} ${msg.type}`}>
              <div className="message-header">
                <strong>
                  {msg.role === "user" ? "You" : 
                   msg.role === "assistant" ? "JARVIS" : "System"}
                </strong>
                <span className="message-type">{msg.type}</span>
              </div>
              <div className="message-content">{msg.content}</div>
            </div>
          ))
        )}
      </div>

      <div className="input-section">
        <textarea
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();
              handleInput(input);
            }
          }}
          placeholder={
            mode === "command" ? "Type command (or /help)..." :
            mode === "voice" ? "Click voice button to speak..." :
            "Type your message..."
          }
          disabled={loading || listening || isSpeaking}
          rows={3}
        />
        
        <div className="input-controls">
          <button
            onClick={() => handleInput(input)}
            disabled={!input.trim() || loading || listening || isSpeaking}
          >
            {loading ? "Processing..." : 
             mode === "command" ? "Execute" : "Send"}
          </button>
          
          <button
            onClick={() => setMessages([])}
            className="secondary"
          >
            Clear
          </button>
          
          <button
            onClick={() => handleInput("/help")}
            className="secondary"
          >
            Help
          </button>
        </div>

        <div className="quick-actions">
          <button onClick={() => handleInput("check emails")}>
             Check Email
          </button>
          <button onClick={() => handleInput("system status")}>
             System Status
          </button>
          <button onClick={() => handleInput("list files")}>
             List Files
          </button>
        </div>
      </div>
    </div>
  );
}

export default JARVISCore;