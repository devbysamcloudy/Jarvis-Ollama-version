const BASE_URL = "http://localhost:5000/api";

const getToken = () => localStorage.getItem("token");

const headers = () => ({
  "Content-Type": "application/json",
  Authorization: `Bearer ${getToken()}`,
});

// ─── AUTH ────────────────────────────────────────────────────

export const registerUser = async (username, email, password) => {
  const res = await fetch(`${BASE_URL}/auth/register`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, email, password }),
  });
  return res.json();
};

export const loginUser = async (username, password) => {
  const res = await fetch(`${BASE_URL}/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ username, password }),
  });
  const data = await res.json();
  if (data.token) localStorage.setItem("token", data.token);
  return data;
};

export const logoutUser = async () => {
  await fetch(`${BASE_URL}/auth/logout`, {
    method: "POST",
    headers: headers(),
  });
  localStorage.removeItem("token");
};

export const getMe = async () => {
  const res = await fetch(`${BASE_URL}/auth/me`, { headers: headers() });
  return res.json();
};

// ─── CHAT HISTORY ────────────────────────────────────────────

export const getChatHistory = async (limit = 50) => {
  const res = await fetch(`${BASE_URL}/history/chat?limit=${limit}`, {
    headers: headers(),
  });
  return res.json();
};

export const saveChat = async (user_message, ai_response, mode = "chat", tokens_used = 0, model_used = null) => {
  const res = await fetch(`${BASE_URL}/history/chat`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ user_message, ai_response, mode, tokens_used, model_used }),
  });
  return res.json();
};

// ─── COMMAND HISTORY ─────────────────────────────────────────

export const getCommands = async (limit = 50) => {
  const res = await fetch(`${BASE_URL}/history/commands?limit=${limit}`, {
    headers: headers(),
  });
  return res.json();
};

export const saveCommand = async (command, response, type = "general", success = true) => {
  const res = await fetch(`${BASE_URL}/history/commands`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ command, response, type, success, source: "web" }),
  });
  return res.json();
};

export const clearCommands = async () => {
  const res = await fetch(`${BASE_URL}/history/commands`, {
    method: "DELETE",
    headers: headers(),
  });
  return res.json();
};

// ─── FILE ACTIONS ─────────────────────────────────────────────

export const getFileActions = async () => {
  const res = await fetch(`${BASE_URL}/history/files`, { headers: headers() });
  return res.json();
};

export const saveFileAction = async (action_type, source_path, dest_path, file_category) => {
  const res = await fetch(`${BASE_URL}/history/files`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ action_type, source_path, dest_path, file_category, source: "web" }),
  });
  return res.json();
};

// ─── PREFERENCES ─────────────────────────────────────────────

export const getPreferences = async () => {
  const res = await fetch(`${BASE_URL}/preferences/`, { headers: headers() });
  return res.json();
};

export const updatePreferences = async (prefs) => {
  const res = await fetch(`${BASE_URL}/preferences/`, {
    method: "PATCH",
    headers: headers(),
    body: JSON.stringify(prefs),
  });
  return res.json();
};

export const runCommand = async (command) => {
  const res = await fetch(`${BASE_URL}/commands/run`, {
    method: "POST",
    headers: headers(),
    body: JSON.stringify({ command }),
  });
  return res.json();
};

export const getWeather = async (city = "Nairobi") => {
  const res = await fetch(`${BASE_URL}/weather/?city=${city}`, {
    headers: headers(),
  });
  return res.json();
};