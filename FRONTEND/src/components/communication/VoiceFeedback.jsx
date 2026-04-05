import { useState, useEffect, useRef } from "react";
import { runCommand } from "../../api";

export default function VoiceFeedback() {
  const [transcript, setTranscript] = useState("");
  const [response, setResponse] = useState("");
  const [listening, setListening] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);

  const recognitionRef = useRef(null);
  const speakingRef = useRef(false);

  // ── SPEAK ─────────────────────────────────────────────────
  function speak(text) {
    return new Promise((resolve) => {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.88;
      utterance.pitch = 0.72;
      utterance.volume = 1;

      // Pick a deep voice if available
      const voices = window.speechSynthesis.getVoices();
      const deepVoice = voices.find(
        (v) => v.name.includes("Google UK English Male") ||
               v.name.includes("Microsoft David") ||
               v.name.includes("Daniel")
      );
      if (deepVoice) utterance.voice = deepVoice;

      speakingRef.current = true;
      setSpeaking(true);

      utterance.onend = () => {
        speakingRef.current = false;
        setSpeaking(false);
        resolve();
      };

      utterance.onerror = () => {
        speakingRef.current = false;
        setSpeaking(false);
        resolve();
      };

      window.speechSynthesis.speak(utterance);
    });
  }

  // ── ASK FLASK ─────────────────────────────────────────────
  async function askJarvis(input) {
    try {
      const data = await runCommand(input);
      return data.response || "I could not process that.";
    } catch {
      return "I am unable to connect to the server right now.";
    }
  }

  // ── START LISTENING ───────────────────────────────────────
  function startListening() {
    if (listening || speakingRef.current) return;

    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) {
      setError("Voice not supported. Use Chrome or Edge.");
      return;
    }

    const recognition = new SR();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognitionRef.current = recognition;

    recognition.onstart = () => {
      setListening(true);
      setError("");
    };

    recognition.onresult = async (e) => {
      const text = e.results[0][0].transcript;
      const confidence = e.results[0][0].confidence;

      setTranscript(text);

      if (confidence < 0.6) {
        setError("Could not hear clearly. Please speak again.");
        setListening(false);
        return;
      }

      const reply = await askJarvis(text);
      setResponse(reply);
      setHistory((prev) => [...prev, { user: text, jarvis: reply }]);
      await speak(reply);

      setTimeout(() => startListening(), 400);
    };

    recognition.onerror = (e) => {
      if (e.error !== "no-speech") {
        setError(`Error: ${e.error}`);
      }
      setListening(false);
    };

    recognition.onend = () => setListening(false);

    recognition.start();
  }

  function stopListening() {
    recognitionRef.current?.stop();
    window.speechSynthesis.cancel();
    setListening(false);
    setSpeaking(false);
    speakingRef.current = false;
  }

  function testVoice() {
    speak("Hello! I am JARVIS, your personal AI assistant. How can I help you?");
  }

  useEffect(() => {
    if (error) {
      const t = setTimeout(() => setError(""), 5000);
      return () => clearTimeout(t);
    }
  }, [error]);

  return (
    <div className="page-container">
      <div className="voice-wrapper">

        {/* Status orb */}
        <div className={`voice-orb ${listening ? "orb-listening" : speaking ? "orb-speaking" : "orb-idle"}`}>
          <div className="orb-ring orb-ring1" />
          <div className="orb-ring orb-ring2" />
          <div className="orb-ring orb-ring3" />
          <span className="orb-label">
            {listening ? "Listening..." : speaking ? "Speaking..." : "JARVIS"}
          </span>
        </div>

        {/* Controls */}
        <div className="voice-controls">
          <button
            className={`voice-btn ${listening ? "voice-btn-stop" : "voice-btn-start"}`}
            onClick={listening ? stopListening : startListening}
          >
            {listening ? "Stop" : "Talk to JARVIS"}
          </button>
          <button className="voice-btn voice-btn-test" onClick={testVoice}>
            Test Voice
          </button>
        </div>

        {/* Transcript */}
        {transcript && (
          <div className="voice-bubble voice-bubble-user">
            <span className="voice-bubble-label">You</span>
            <p>{transcript}</p>
          </div>
        )}

        {/* Response */}
        {response && (
          <div className="voice-bubble voice-bubble-jarvis">
            <span className="voice-bubble-label">JARVIS</span>
            <p>{response}</p>
          </div>
        )}

        {/* Error */}
        {error && <p className="voice-error">{error}</p>}

        {/* History */}
        {history.length > 0 && (
          <div className="voice-history">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "10px" }}>
              <p className="section-title" style={{ margin: 0 }}>Session history</p>
              <button className="clear-button" style={{ fontSize: "12px", padding: "4px 10px" }} onClick={() => setHistory([])}>
                Clear
              </button>
            </div>
            {[...history].reverse().map((h, i) => (
              <div key={i} className="voice-history-item">
                <p className="voice-history-user">You: {h.user}</p>
                <p className="voice-history-jarvis">JARVIS: {h.jarvis}</p>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}