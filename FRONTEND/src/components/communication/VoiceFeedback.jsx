import { useState, useEffect, useRef } from "react";
import { runCommand } from "../../api";

const BASE_URL = "http://localhost:5000/api";
const getToken = () => localStorage.getItem("token");

async function speakElevenLabs(text) {
  const res = await fetch(`${BASE_URL}/voice/speak`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${getToken()}`,
    },
    body: JSON.stringify({ text }),
  });
  if (!res.ok) throw new Error("ElevenLabs failed");
  const blob = await res.blob();
  return URL.createObjectURL(blob);
}

export default function VoiceFeedback() {
  const [transcript, setTranscript] = useState("");
  const [response, setResponse] = useState("");
  const [listening, setListening] = useState(false);
  const [speaking, setSpeaking] = useState(false);
  const [error, setError] = useState("");
  const [history, setHistory] = useState([]);
  const [useElevenLabs, setUseElevenLabs] = useState(true);

  const recognitionRef = useRef(null);
  const speakingRef = useRef(false);
  const audioRef = useRef(null);

  async function speak(text) {
    speakingRef.current = true;
    setSpeaking(true);
    try {
      if (useElevenLabs) {
        const audioUrl = await speakElevenLabs(text);
        const audio = new Audio(audioUrl);
        audioRef.current = audio;
        await new Promise((resolve) => {
          audio.onended = resolve;
          audio.onerror = resolve;
          audio.play().catch(resolve);
        });
        URL.revokeObjectURL(audioUrl);
      } else {
        await browserSpeak(text);
      }
    } catch {
      setError("ElevenLabs unavailable, using browser voice");
      await browserSpeak(text);
    } finally {
      speakingRef.current = false;
      setSpeaking(false);
    }
  }

  function browserSpeak(text) {
    return new Promise((resolve) => {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.88;
      utterance.pitch = 0.72;
      utterance.volume = 1;
      const voices = window.speechSynthesis.getVoices();
      const deepVoice = voices.find(
        (v) => v.name.includes("Google UK English Male") ||
               v.name.includes("Microsoft David") ||
               v.name.includes("Daniel")
      );
      if (deepVoice) utterance.voice = deepVoice;
      utterance.onend = resolve;
      utterance.onerror = resolve;
      window.speechSynthesis.speak(utterance);
    });
  }

  async function askJarvis(input) {
    try {
      const data = await runCommand(input);
      return data.response || "I could not process that.";
    } catch {
      return "I am unable to connect to the server right now.";
    }
  }

  function startListening() {
    if (listening || speakingRef.current) return;
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SR) { setError("Voice not supported. Use Chrome or Edge."); return; }

    const recognition = new SR();
    recognition.lang = "en-US";
    recognition.continuous = false;
    recognition.interimResults = false;
    recognitionRef.current = recognition;

    recognition.onstart = () => { setListening(true); setError(""); };

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
      if (e.error !== "no-speech") setError(`Error: ${e.error}`);
      setListening(false);
    };

    recognition.onend = () => setListening(false);
    recognition.start();
  }

  function stopListening() {
    recognitionRef.current?.stop();
    window.speechSynthesis.cancel();
    if (audioRef.current) { audioRef.current.pause(); audioRef.current = null; }
    setListening(false);
    setSpeaking(false);
    speakingRef.current = false;
  }

  function testVoice() {
    speak("Hello! I am JARVIS, your personal AI assistant. How can I help you today?");
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

        <div className={`voice-orb ${listening ? "orb-listening" : speaking ? "orb-speaking" : "orb-idle"}`}>
          <div className="orb-ring orb-ring1" />
          <div className="orb-ring orb-ring2" />
          <div className="orb-ring orb-ring3" />
          <span className="orb-label">
            {listening ? "Listening..." : speaking ? "Speaking..." : "JARVIS"}
          </span>
        </div>

        {/* ElevenLabs toggle */}
        <div style={{ display: "flex", alignItems: "center", gap: "10px", fontSize: "13px", color: "var(--text-dim)" }}>
          <span>Browser</span>
          <label style={{ position: "relative", display: "inline-block", width: "40px", height: "22px", cursor: "pointer" }}>
            <input type="checkbox" checked={useElevenLabs} onChange={(e) => setUseElevenLabs(e.target.checked)} style={{ opacity: 0, width: 0, height: 0 }} />
            <span style={{ position: "absolute", top: 0, left: 0, right: 0, bottom: 0, background: useElevenLabs ? "#38bdf8" : "#334155", borderRadius: "22px", transition: "0.3s" }}>
              <span style={{ position: "absolute", height: "16px", width: "16px", left: useElevenLabs ? "21px" : "3px", bottom: "3px", background: "white", borderRadius: "50%", transition: "0.3s" }} />
            </span>
          </label>
          <span style={{ color: useElevenLabs ? "#38bdf8" : "var(--text-muted)" }}>
            ElevenLabs {useElevenLabs ? "ON" : "OFF"}
          </span>
        </div>

        <div className="voice-controls">
          <button className={`voice-btn ${listening ? "voice-btn-stop" : "voice-btn-start"}`} onClick={listening ? stopListening : startListening}>
            {listening ? "Stop" : "Talk to JARVIS"}
          </button>
          <button className="voice-btn voice-btn-test" onClick={testVoice}>
            Test Voice
          </button>
        </div>

        {transcript && (
          <div className="voice-bubble voice-bubble-user">
            <span className="voice-bubble-label">You</span>
            <p>{transcript}</p>
          </div>
        )}

        {response && (
          <div className="voice-bubble voice-bubble-jarvis">
            <span className="voice-bubble-label">JARVIS</span>
            <p>{response}</p>
          </div>
        )}

        {error && <p className="voice-error">{error}</p>}

        {history.length > 0 && (
          <div className="voice-history">
            <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "10px" }}>
              <p className="section-title" style={{ margin: 0 }}>Session history</p>
              <button className="clear-button" style={{ fontSize: "12px", padding: "4px 10px" }} onClick={() => setHistory([])}>Clear</button>
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