import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import theme from "./theme";
import "./index.css";

/* Inject theme as CSS custom properties on :root */
const root = document.documentElement;

// Colors
Object.entries(theme.colors).forEach(([key, val]) => {
  const prop = key.replace(/([A-Z])/g, "-$1").toLowerCase();
  root.style.setProperty(`--c-${prop}`, val);
});

// Fonts
root.style.setProperty("--font-body", theme.fonts.body);
root.style.setProperty("--font-mono", theme.fonts.mono);

// Font sizes
Object.entries(theme.fontSizes).forEach(([key, val]) => {
  root.style.setProperty(`--fs-${key}`, val);
});

// Radii
Object.entries(theme.radius).forEach(([key, val]) => {
  root.style.setProperty(`--r-${key}`, val);
});

// Shadows
Object.entries(theme.shadows).forEach(([key, val]) => {
  root.style.setProperty(`--shadow-${key}`, val);
});

// Layout
root.style.setProperty("--sidebar-w", theme.sidebar.width);

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
