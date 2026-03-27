import { useState } from "react";
import { loginUser } from "../../api";

export default function Login({ onLogin, switchToRegister }) {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.username || !form.password) {
      setError("Please fill in all fields");
      return;
    }
    setLoading(true);
    try {
      const data = await loginUser(form.username, form.password);
      if (data.token) {
        onLogin(data.user);
      } else {
        setError(data.error || "Login failed");
      }
    } catch {
      setError("Cannot connect to server");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-wrapper">
      <div className="auth-box">
        <div className="auth-logo">J.A.R.V.I.S</div>
        <p className="auth-subtitle">Just A Rather Very Intelligent System</p>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="auth-field">
            <label>Username</label>
            <input
              type="text"
              name="username"
              value={form.username}
              onChange={handleChange}
              placeholder="Enter username"
              autoComplete="username"
            />
          </div>

          <div className="auth-field">
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              placeholder="Enter password"
              autoComplete="current-password"
            />
          </div>

          {error && <p className="auth-error">{error}</p>}

          <button type="submit" className="auth-btn" disabled={loading}>
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>

        <p className="auth-switch">
          No account?{" "}
          <span onClick={switchToRegister}>Register here</span>
        </p>
      </div>
    </div>
  );
}
