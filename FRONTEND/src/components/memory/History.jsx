import  { useState, useEffect } from "react";
import { getCommands, getChatHistory, clearCommands } from "../../api";

function History() {
  const [commands, setCommands] = useState([]);
  const [chats, setChats] = useState([]);
  const [tab, setTab] = useState("commands");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => { fetchAll(); }, []);

  const fetchAll = async () => {
    setLoading(true);
    setError("");
    try {
      const [cmdData, chatData] = await Promise.all([
        getCommands(50),
        getChatHistory(50),
      ]);
      setCommands(cmdData.commands || []);
      setChats(chatData.chat || []);
    } catch {
      setError("Could not load history from server");
    } finally {
      setLoading(false);
    }
  };

  const handleClearCommands = async () => {
    if (!window.confirm("Clear all command history?")) return;
    await clearCommands();
    setCommands([]);
  };

  const formatTime = (iso) => {
    if (!iso) return "";
    return new Date(iso).toLocaleString();
  };

  const getTypeColor = (type) => {
    const colors = { system: "#00d4ff", file: "#00ff88", ai: "#a855f7", general: "#888", error: "#ff5566" };
    return colors[type] || "#888";
  };

  return (
    <div className="history-container">
      <div className="history-header">
        <h1 className="history-title">History</h1>
        <button className="clear-button" onClick={fetchAll}>Refresh</button>
      </div>

      <div style={{ display: "flex", gap: "8px", marginBottom: "16px" }}>
        <button className={`nav-button ${tab === "commands" ? "active" : ""}`} onClick={() => setTab("commands")}>
          Commands ({commands.length})
        </button>
        <button className={`nav-button ${tab === "chat" ? "active" : ""}`} onClick={() => setTab("chat")}>
          Chat ({chats.length})
        </button>
      </div>

      {loading && <p className="empty-state">Loading history...</p>}
      {error && <p style={{ color: "#ff5566" }}>{error}</p>}

      {!loading && tab === "commands" && (
        <>
          <div style={{ display: "flex", justifyContent: "flex-end", marginBottom: "8px" }}>
            <button className="clear-button" onClick={handleClearCommands}>Clear All</button>
          </div>
          {commands.length === 0 ? <p className="empty-state">No commands yet</p> : (
            <ul className="history-list">
              {commands.map((item) => (
                <li key={item.id} className="history-item">
                  <div className="item-content">
                    <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                      <span style={{ fontSize: "11px", color: getTypeColor(item.type), border: `1px solid ${getTypeColor(item.type)}`, borderRadius: "4px", padding: "1px 6px" }}>
                        {item.type}
                      </span>
                      <span className="command">{item.command}</span>
                    </div>
                    {item.response && (
                      <p style={{ fontSize: "12px", color: "#888", margin: "4px 0 0" }}>
                        {item.response.slice(0, 100)}{item.response.length > 100 ? "..." : ""}
                      </p>
                    )}
                    <span className="time">{formatTime(item.executed_at)}</span>
                  </div>
                  <span style={{ color: item.success ? "#00ff88" : "#ff5566", fontSize: "12px" }}>
                    {item.success ? "✓" : "✗"}
                  </span>
                </li>
              ))}
            </ul>
          )}
        </>
      )}

      {!loading && tab === "chat" && (
        <>
          {chats.length === 0 ? <p className="empty-state">No chat history yet</p> : (
            <ul className="history-list">
              {chats.map((item) => (
                <li key={item.id} className="history-item">
                  <div className="item-content">
                    <span className="command">{item.user_message}</span>
                    {item.ai_response && (
                      <p style={{ fontSize: "12px", color: "#888", margin: "4px 0 0" }}>
                        {item.ai_response.slice(0, 100)}{item.ai_response.length > 100 ? "..." : ""}
                      </p>
                    )}
                    <span className="time">{formatTime(item.sent_at)}</span>
                  </div>
                  <span style={{ fontSize: "11px", color: "#555570" }}>{item.mode}</span>
                </li>
              ))}
            </ul>
          )}
        </>
      )}
    </div>
  );
}

export default History;
