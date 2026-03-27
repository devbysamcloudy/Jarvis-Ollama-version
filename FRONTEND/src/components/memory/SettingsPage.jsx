import  { useState, useEffect } from "react";
import { getPreferences, updatePreferences } from "../../api";

function SettingsPage() {
  const [prefs, setPrefs] = useState({
    theme: "dark",
    language: "en",
    city: "Nairobi",
    ai_model: "llama3.2:1b",
    voice_enabled: false,
    notifications_on: true,
  });
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);
  const [message, setMessage] = useState("");

  useEffect(() => {
    fetchPrefs();
  }, []);

  const fetchPrefs = async () => {
    setLoading(true);
    try {
      const data = await getPreferences();
      if (data.preferences) setPrefs(data.preferences);
    } catch {
      setMessage("Could not load preferences");
    } finally {
      setLoading(false);
    }
  };

  const handleChange = (key, value) => {
    setPrefs((prev) => ({ ...prev, [key]: value }));
  };

  const handleSave = async () => {
    setSaving(true);
    setMessage("");
    try {
      const data = await updatePreferences(prefs);
      if (data.preferences) {
        setMessage("Settings saved successfully!");
      } else {
        setMessage("Failed to save settings");
      }
    } catch {
      setMessage("Could not connect to server");
    } finally {
      setSaving(false);
      setTimeout(() => setMessage(""), 3000);
    }
  };

  if (loading) return <div className="settings-container"><p className="empty-state">Loading settings...</p></div>;

  return (
    <div className="settings-container">
      <h1 className="settings-title">Settings</h1>

      <div className="settings-form">

        {/* Theme */}
        <div className="form-group">
          <label className="form-label">Theme</label>
          <select
            className="form-input"
            value={prefs.theme}
            onChange={(e) => handleChange("theme", e.target.value)}
          >
            <option value="dark">Dark</option>
            <option value="light">Light</option>
          </select>
        </div>

        {/* City */}
        <div className="form-group">
          <label className="form-label">Default City (Weather)</label>
          <input
            type="text"
            className="form-input"
            value={prefs.city}
            onChange={(e) => handleChange("city", e.target.value)}
            placeholder="e.g. Nairobi"
          />
        </div>

        {/* AI Model */}
        <div className="form-group">
          <label className="form-label">AI Model</label>
          <select
            className="form-input"
            value={prefs.ai_model}
            onChange={(e) => handleChange("ai_model", e.target.value)}
          >
            <option value="llama3.2:1b">Llama 3.2 1B</option>
            <option value="gemma3:4b">Gemma 3 4B</option>
            <option value="gpt-4o-mini">GPT-4o Mini</option>
          </select>
        </div>

        {/* Language */}
        <div className="form-group">
          <label className="form-label">Language</label>
          <select
            className="form-input"
            value={prefs.language}
            onChange={(e) => handleChange("language", e.target.value)}
          >
            <option value="en">English</option>
            <option value="sw">Swahili</option>
            <option value="fr">French</option>
          </select>
        </div>

        <div className="form-divider"></div>

        {/* Voice */}
        <div className="checkbox-group">
          <input
            type="checkbox"
            className="form-checkbox"
            checked={prefs.voice_enabled}
            onChange={(e) => handleChange("voice_enabled", e.target.checked)}
            id="voice-toggle"
          />
          <label className="checkbox-label" htmlFor="voice-toggle">
            Voice enabled
          </label>
        </div>

        {/* Notifications */}
        <div className="checkbox-group">
          <input
            type="checkbox"
            className="form-checkbox"
            checked={prefs.notifications_on}
            onChange={(e) => handleChange("notifications_on", e.target.checked)}
            id="notifications-toggle"
          />
          <label className="checkbox-label" htmlFor="notifications-toggle">
            Notifications enabled
          </label>
        </div>

        {message && (
          <p style={{ color: message.includes("success") ? "#00ff88" : "#ff5566", fontSize: "13px" }}>
            {message}
          </p>
        )}

        <button className="save-button" onClick={handleSave} disabled={saving}>
          {saving ? "Saving..." : "Save Settings"}
        </button>
      </div>
    </div>
  );
}

export default SettingsPage;
