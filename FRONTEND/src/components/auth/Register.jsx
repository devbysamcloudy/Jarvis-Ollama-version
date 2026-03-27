import { useState } from "react";
import { registerUser } from "../../api";

export default function Register({ onLogin, switchToLogin }) {
  const [form, setForm] = useState({ username: "", email: "", password: "", confirm: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError("");
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.username || !form.email || !form.password || !form.confirm) {
      setError("Please fill in all fields");
      return;
    }
    if (form.password !== form.confirm) {
      setError("Passwords do not match");
      return;
    }
    if (form.password.length < 4) {
      setError("Password must be at least 4 characters");
      return;
    }
    setLoading(true);
    try {
      const data = await registerUser(form.username, form.email, form.password);
      if (data.token) {
        onLogin(data.user);
      } else {
        setError(data.error || "Registration failed");
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
        <p className="auth-subtitle">Create your account</p>

        <form onSubmit={handleSubmit} className="auth-form">
          <div className="auth-field">
            <label>Username</label>
            <input
              type="text"
              name="username"
              value={form.username}
              onChange={handleChange}
              placeholder="Choose a username"
              autoComplete="username"
            />
          </div>

          <div className="auth-field">
            <label>Email</label>
            <input
              type="email"
              name="email"
              value={form.email}
              onChange={handleChange}
              placeholder="Enter your email"
              autoComplete="email"
            />
          </div>

          <div className="auth-field">
            <label>Password</label>
            <input
              type="password"
              name="password"
              value={form.password}
              onChange={handleChange}
              placeholder="Choose a password"
              autoComplete="new-password"
            />
          </div>

          <div className="auth-field">
            <label>Confirm Password</label>
            <input
              type="password"
              name="confirm"
              value={form.confirm}
              onChange={handleChange}
              placeholder="Repeat your password"
              autoComplete="new-password"
            />
          </div>

          {error && <p className="auth-error">{error}</p>}

          <button type="submit" className="auth-btn" disabled={loading}>
            {loading ? "Creating account..." : "Register"}
          </button>
        </form>

        <p className="auth-switch">
          Already have an account?{" "}
          <span onClick={switchToLogin}>Login here</span>
        </p>
      </div>
    </div>
  );
}
