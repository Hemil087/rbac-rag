/**
 * ─── THEME CONFIGURATION ───────────────────────────────────────
 * Edit the values below to change the look of the entire app.
 * Every color, radius, shadow, and font is pulled from here.
 * ────────────────────────────────────────────────────────────────
 */

const theme = {
  /* ── Brand palette ─────────────────────────────────── */
  colors: {
    // Primary action color (buttons, links, active states)
    primary:      "#2563EB",
    primaryHover: "#1D4ED8",
    primaryLight: "#DBEAFE",

    // Danger / destructive actions
    danger:       "#DC2626",
    dangerHover:  "#B91C1C",
    dangerLight:  "#FEE2E2",

    // Success indicators
    success:      "#16A34A",
    successLight: "#DCFCE7",

    // Warning indicators
    warning:      "#D97706",
    warningLight: "#FEF3C7",

    // Surfaces
    bgApp:        "#F8FAFC",   // page background
    bgSidebar:    "#FFFFFF",   // sidebar background
    bgCard:       "#FFFFFF",   // cards / panels
    bgInput:      "#FFFFFF",   // form inputs
    bgHover:      "#F1F5F9",   // hover rows / items
    bgActive:     "#EFF6FF",   // selected / active sidebar items

    // Borders
    border:       "#E2E8F0",
    borderFocus:  "#2563EB",

    // Text
    textPrimary:  "#0F172A",
    textSecondary:"#475569",
    textMuted:    "#94A3B8",
    textOnPrimary:"#FFFFFF",

    // Chat-specific
    chatUser:     "#EFF6FF",    // user message bubble
    chatAssistant:"#F1F5F9",   // assistant message bubble
  },

  /* ── Typography ────────────────────────────────────── */
  fonts: {
    body: "'Inter', -apple-system, BlinkMacSystemFont, sans-serif",
    mono: "'SF Mono', 'Fira Code', 'Fira Mono', monospace",
  },

  fontSizes: {
    xs:   "0.75rem",
    sm:   "0.8125rem",
    base: "0.875rem",
    lg:   "1rem",
    xl:   "1.25rem",
    xxl:  "1.5rem",
  },

  /* ── Spacing & radii ───────────────────────────────── */
  radius: {
    sm:   "6px",
    md:   "8px",
    lg:   "12px",
    full: "9999px",
  },

  shadows: {
    sm:   "0 1px 2px rgba(0,0,0,0.05)",
    md:   "0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.04)",
    lg:   "0 4px 12px rgba(0,0,0,0.08)",
  },

  /* ── Layout ────────────────────────────────────────── */
  sidebar: {
    width:          "260px",
    collapsedWidth: "0px",
  },
};

export default theme;
