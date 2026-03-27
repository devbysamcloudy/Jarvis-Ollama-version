import React, { useState, useEffect, useRef } from "react";

// ==========================
// Oloma AI Config (hardcoded for frontend testing)
// ==========================
// These are normally in .env, but in plain frontend React, process.env is not defined.
const OPENAI_API_KEY = "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";
const BASE_URL = "https://api.olama.ai/v1";
const MODEL = "gpt-4o-mini";
const MAX_TOKENS = 2048;
const TEMPERATURE = 0.7;
const TOP_P = 0.9;
const FREQUENCY_PENALTY = 0;
const PRESENCE_PENALTY = 0;
const TIMEOUT = 60000;

function VoiceFeedback() {
  // ==========================
  // React state variables
  // ==========================
  const [userInformation, setUserInformation] = useState(""); // Last thing user said
  const [listening, setListening] = useState(false);          // If speech recognition is active
  const [error, setError] = useState("");                     // For showing errors in UI
  const recognitionRef = useRef(null);                        // Holds SpeechRecognition instance
  const speakingRef = useRef(false);                          // Track if JARVIS is currently speaking

  // ==========================
  // Start voice recognition
  // ==========================
  function startVoice() {
    // Prevent starting multiple recognitions simultaneously or while JARVIS is speaking
    if (listening || speakingRef.current) return;

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
      alert("Browser doesn't support voice. Use Chrome or Edge.");
      return;
    }

    // Create new recognition instance
    const recognition = new SpeechRecognition();
    recognition.lang = "en-US";
    recognition.continuous = false;   // Single-shot recognition for stability
    recognition.interimResults = false;
    recognitionRef.current = recognition;

    // Recognition started
    recognition.onstart = () => {
      console.log("Listening started...");
      setError("");
      setListening(true);
    };

    // Recognition result received
    recognition.onresult = async (e) => {
      const transcript = e.results[0][0].transcript;         // User speech text
      const confidence = e.results[0][0].confidence;        // Confidence score (0-1)
      console.log(`Transcript: "${transcript}" (confidence: ${(confidence * 100).toFixed(0)}%)`);

      // Low confidence -> prompt user to speak clearly
      if (confidence < 0.7) {
        setError("Low confidence—please speak clearly!");
        return;
      }

      setUserInformation(transcript); // Show what user said

      try {
        // Send transcript to Oloma AI and get response
        const aiResponse = await askOlomaAI(transcript);
        await makeJarvisTalk(aiResponse); // Wait for JARVIS to finish speaking
      } catch (err) {
        console.error("AI error:", err);
        await makeJarvisTalk("Sorry, I couldn't process that.");
      }

      // Automatically restart recognition after JARVIS finishes
      setTimeout(() => startVoice(), 300);
    };

    // Recognition error handling
    recognition.onerror = (e) => {
      console.error("Recognition error:", e.error);
      setError(e.error === "network" ? "Mic/network issue. Try again." : `Recognition error: ${e.error}`);
      setListening(false);
    };

    // Recognition ended
    recognition.onend = () => {
      console.log("Listening ended.");
      setListening(false);
    };

    // Start recognition
    recognition.start();
    setListening(true);
  }

  // ==========================
  // Stop voice recognition manually
  // ==========================
  function stopVoice() {
    if (recognitionRef.current) recognitionRef.current.stop();
    setListening(false);
  }

  // ==========================
  // Make JARVIS speak
  // Returns a Promise so we can wait until speaking finishes
  // ==========================
  function makeJarvisTalk(text) {
    return new Promise((resolve) => {
      speakingRef.current = true; // mark JARVIS as speaking
      const utterance = new SpeechSynthesisUtterance(text);
      utterance.rate = 0.85;  // slightly slower for clarity
      utterance.pitch = 0.75; // deeper voice
      utterance.volume = 1;

      // When JARVIS finishes speaking
      utterance.onend = () => {
        speakingRef.current = false;
        resolve();
      };

      window.speechSynthesis.cancel(); // stop any ongoing speech
      window.speechSynthesis.speak(utterance);
      console.log("JARVIS says:", text);
    });
  }

  // Call Oloma AI API
  async function askOlomaAI(question) {
    const controller = new AbortController();                 // for timeout
    const timeout = setTimeout(() => controller.abort(), TIMEOUT);

    const response = await fetch(`${BASE_URL}/chat/completions`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${OPENAI_API_KEY}`,
      },
      signal: controller.signal,
      body: JSON.stringify({
        model: MODEL,
        messages: [{ role: "user", content: question }],
        max_tokens: MAX_TOKENS,
        temperature: TEMPERATURE,
        top_p: TOP_P,
        frequency_penalty: FREQUENCY_PENALTY,
        presence_penalty: PRESENCE_PENALTY,
      }),
    });

    clearTimeout(timeout);
    const data = await response.json();
    return data.choices?.[0]?.message?.content || "Sorry, no response from AI.";
  }

  // Auto-clear user input after 6 seconds
  useEffect(() => {
    if (userInformation) {
      const timer = setTimeout(() => setUserInformation(""), 6000);
      return () => clearTimeout(timer);
    }
  }, [userInformation]);

  // Auto-clear error after 5 seconds
  useEffect(() => {
    if (error) {
      const timer = setTimeout(() => setError(""), 5000);
      return () => clearTimeout(timer);
    }
  }, [error]);

  // Render UI
  return (
    <div className="voice-container">
      <h2>JARVIS Voice Assistant (Oloma AI-powered)</h2>

      <div className="voice-controls">
        <button onClick={listening ? stopVoice : startVoice}>
          {listening ? "Stop Listening" : "Talk to JARVIS"}
        </button>
        <button onClick={() => makeJarvisTalk("Hello! I am JARVIS, your assistant.")}>
          Test Voice
        </button>
      </div>

      {userInformation && (
        <div>
          <p><strong>You said:</strong> {userInformation}</p>
        </div>
      )}
      {error && <div style={{ color: "orange" }}>{error}</div>}

      <small>Open console for logs.</small>
    </div>
  );
}

export default VoiceFeedback;
