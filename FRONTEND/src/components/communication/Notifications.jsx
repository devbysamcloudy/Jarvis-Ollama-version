import { useState, useEffect } from "react";

const BASE_URL = "http://localhost:5000/api";
const getToken = () => localStorage.getItem("token");
const headers = () => ({
  "Content-Type": "application/json",
  Authorization: `Bearer ${getToken()}`,
});

function Notifications() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => { fetchNotifications(); }, []);

  const fetchNotifications = async () => {
    setLoading(true);
    try {
      const res = await fetch(`${BASE_URL}/notifications/`, { headers: headers() });
      const data = await res.json();
      setNotifications(data.notifications || []);
    } catch {
      setNotifications([]);
    } finally {
      setLoading(false);
    }
  };

  const markRead = async (id) => {
    try {
      await fetch(`${BASE_URL}/notifications/${id}/read`, {
        method: "PATCH",
        headers: headers(),
      });
      setNotifications((prev) =>
        prev.map((n) => (n.id === id ? { ...n, is_read: true } : n))
      );
    } catch {
      setNotifications((prev) =>
        prev.map((n) => (n.id === id ? { ...n, is_read: true } : n))
      );
    }
  };

  const deleteNotification = async (id) => {
    try {
      await fetch(`${BASE_URL}/notifications/${id}`, {
        method: "DELETE",
        headers: headers(),
      });
    } catch {}
    setNotifications((prev) => prev.filter((n) => n.id !== id));
  };

  const clearAll = async () => {
    if (!window.confirm("Clear all notifications?")) return;
    try {
      await fetch(`${BASE_URL}/notifications/`, {
        method: "DELETE",
        headers: headers(),
      });
    } catch {}
    setNotifications([]);
  };

  const getTypeColor = (type) => {
    const colors = { info: "#00d4ff", success: "#00ff88", warning: "#ffaa00", error: "#ff5566" };
    return colors[type] || "#888";
  };

  return (
    <div className="notifications-container">
      <div className="notifications-header">
        <h2 className="notifications-title">
          Notifications
          {notifications.filter((n) => !n.is_read).length > 0 && (
            <span style={{ marginLeft: "8px", background: "#ff5566", color: "#fff", borderRadius: "10px", padding: "2px 8px", fontSize: "12px" }}>
              {notifications.filter((n) => !n.is_read).length}
            </span>
          )}
        </h2>
        <div className="notification-controls">
          <button className="add-button" onClick={fetchNotifications}>Refresh</button>
          <button className="clear-button" onClick={clearAll}>Clear All</button>
        </div>
      </div>

      {loading && <p className="empty-state">Loading notifications...</p>}

      {!loading && notifications.length === 0 && (
        <p className="empty-state">No notifications</p>
      )}

      <div className="notifications-list">
        {notifications.map((n) => (
          <div key={n.id} className={`notification ${!n.is_read ? "notification-unread" : ""}`}>
            <div className="notification-content">
              <div style={{ display: "flex", alignItems: "center", gap: "8px" }}>
                <span style={{ fontSize: "11px", color: getTypeColor(n.type), border: `1px solid ${getTypeColor(n.type)}`, borderRadius: "4px", padding: "1px 6px" }}>
                  {n.type}
                </span>
                <strong style={{ fontSize: "13px" }}>{n.title}</strong>
                {!n.is_read && <span className="badge">new</span>}
              </div>
              {n.message && <p className="notification-message" style={{ margin: "4px 0 0", fontSize: "13px", color: "#888" }}>{n.message}</p>}
              <p style={{ fontSize: "11px", color: "#555570", margin: "4px 0 0" }}>
                {new Date(n.created_at).toLocaleString()}
              </p>
            </div>
            <div className="notification-actions">
              {!n.is_read && (
                <button className="action-button read-button" onClick={() => markRead(n.id)}>Read</button>
              )}
              <button className="action-button delete-button" onClick={() => deleteNotification(n.id)}>Delete</button>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Notifications;
