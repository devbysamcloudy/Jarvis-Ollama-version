import { useState } from "react";
import CommandAnalyzer from "./CommandAnalyzer";

function AssistantCore() {
  const [input, setInput] = useState("");
  const [response, setResponse] = useState("");

  async function handleCommand() {
    if (!input.trim()) return;

    // Step 1: Send text to AI (or fallback)
    const aiText = await fetchAIResponse(input);

    // Step 2: Analyze intent
    const result = CommandAnalyzer(aiText);

    // Step 3: Show result
    setResponse(result);
    setInput("");
  }

  return (
    <div className="assistant-core">
      <input
        type="text"
        placeholder="Type a command..."
        value={input}
        onChange={(e) => setInput(e.target.value)}
      />
      <button onClick={handleCommand}>Send</button>

      <div className="assistant-response">
        {response}
      </div>
    </div>
  );
}

export default AssistantCore;

/* ---------------- AI FETCH ---------------- */

async function fetchAIResponse(text) {
  try {
    const res = await fetch("https://api.openai.com/v1/chat/completions", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${import.meta.env.VITE_OPENAI_KEY}`,
      },
      body: JSON.stringify({
        model: "gpt-3.5-turbo",
        messages: [{ role: "user", content: text }],
      }),
    });

    const data = await res.json();
    return data.choices[0].message.content;
  } catch (error) {
    console.error("Error fetching AI response:", error);
    return text;
  }
}
