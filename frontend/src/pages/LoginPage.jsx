import { useState } from "react";
import { useAuth } from "../hooks/useAuth";

export default function LoginPage() {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(email, password);
    } catch (err) {
      setError(err.message || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <div style={styles.header}>
          <span style={styles.logo}>◈</span>
          <h1 style={styles.title}>RBAC · RAG</h1>
          <p style={styles.subtitle}>
            Sign in to your knowledge base
          </p>
        </div>

        <form onSubmit={handleSubmit} style={styles.form}>
          {error && <div style={styles.error}>{error}</div>}

          <label style={styles.label}>
            Email
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              placeholder="admin@acme.com"
              required
              style={styles.input}
            />
          </label>

          <label style={styles.label}>
            Password
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="Enter password"
              required
              style={styles.input}
            />
          </label>

          <button
            type="submit"
            disabled={loading}
            style={{
              ...styles.btn,
              opacity: loading ? 0.7 : 1,
            }}
          >
            {loading ? "Signing in…" : "Sign in"}
          </button>
        </form>

        <div style={styles.hint}>
          <p style={styles.hintTitle}>Demo accounts</p>
          <p style={styles.hintRow}>admin@acme.com / admin123</p>
          <p style={styles.hintRow}>manager@acme.com / manager123</p>
          <p style={styles.hintRow}>employee@acme.com / employee123</p>
        </div>
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    background: "var(--c-bg-app)",
    padding: 20,
  },
  card: {
    width: "100%",
    maxWidth: 400,
    background: "var(--c-bg-card)",
    borderRadius: "var(--r-lg)",
    border: "1px solid var(--c-border)",
    padding: "36px 32px 28px",
    boxShadow: "var(--shadow-lg)",
  },
  header: {
    textAlign: "center",
    marginBottom: 28,
  },
  logo: {
    fontSize: "2rem",
    color: "var(--c-primary)",
    display: "block",
    marginBottom: 8,
  },
  title: {
    fontSize: "var(--fs-xl)",
    fontWeight: 700,
    color: "var(--c-text-primary)",
    letterSpacing: "0.02em",
  },
  subtitle: {
    fontSize: "var(--fs-sm)",
    color: "var(--c-text-muted)",
    marginTop: 4,
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: 16,
  },
  label: {
    display: "flex",
    flexDirection: "column",
    gap: 5,
    fontSize: "var(--fs-sm)",
    fontWeight: 500,
    color: "var(--c-text-secondary)",
  },
  input: {
    padding: "10px 12px",
    borderRadius: "var(--r-md)",
    border: "1px solid var(--c-border)",
    background: "var(--c-bg-input)",
    fontSize: "var(--fs-base)",
    outline: "none",
    transition: "border-color 0.15s",
  },
  btn: {
    padding: "11px",
    borderRadius: "var(--r-md)",
    background: "var(--c-primary)",
    color: "var(--c-text-on-primary)",
    fontWeight: 600,
    fontSize: "var(--fs-base)",
    border: "none",
    cursor: "pointer",
    marginTop: 4,
    transition: "background 0.15s",
  },
  error: {
    padding: "10px 12px",
    borderRadius: "var(--r-md)",
    background: "var(--c-danger-light)",
    color: "var(--c-danger)",
    fontSize: "var(--fs-sm)",
  },
  hint: {
    marginTop: 20,
    padding: "14px",
    borderRadius: "var(--r-md)",
    background: "var(--c-bg-hover)",
  },
  hintTitle: {
    fontSize: "var(--fs-xs)",
    fontWeight: 600,
    color: "var(--c-text-muted)",
    textTransform: "uppercase",
    letterSpacing: "0.05em",
    marginBottom: 6,
  },
  hintRow: {
    fontSize: "var(--fs-xs)",
    color: "var(--c-text-secondary)",
    fontFamily: "var(--font-mono)",
    lineHeight: 1.7,
  },
};
