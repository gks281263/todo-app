import { useState } from "react";
import * as api from "../api";

export default function Auth({ onLogin }) {
  const [isLogin, setIsLogin] = useState(true);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);

    try {
      if (isLogin) {
        const res = await api.login(email, password);
        onLogin(res.access_token, res.user);
      } else {
        await api.register(email, password);
        // automatically login after register
        const res = await api.login(email, password);
        onLogin(res.access_token, res.user);
      }
    } catch (err) {
      setError(err.message || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-container">
      <h2>{isLogin ? "Sign In" : "Create Account"}</h2>
      {error && <div className="error-banner">{error}</div>}
      
      <form onSubmit={handleSubmit} className="auth-form">
        <div className="form-group">
          <label>Email</label>
          <input
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
            autoFocus
          />
        </div>
        <div className="form-group">
          <label>Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={6}
          />
        </div>
        
        <button type="submit" disabled={loading} className="btn-primary">
          {loading ? "Please wait..." : isLogin ? "Login" : "Register"}
        </button>
      </form>

      <p className="auth-switch">
        {isLogin ? "Don't have an account? " : "Already have an account? "}
        <button
          type="button"
          className="btn-link"
          onClick={() => {
            setIsLogin(!isLogin);
            setError("");
          }}
        >
          {isLogin ? "Sign up" : "Log in"}
        </button>
      </p>
    </div>
  );
}
