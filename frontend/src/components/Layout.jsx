import { NavLink, Outlet } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

const navItems = [
  { to: "/", label: "Knowledge base", icon: "💬" },
  { to: "/conversations", label: "History", icon: "🕘" },
  { to: "/documents", label: "Documents", icon: "📄", admin: true },
  { to: "/users", label: "Users", icon: "👤", admin: true },
  { to: "/roles", label: "Roles", icon: "🔑", admin: true },
];

export default function Layout() {
  const { user, logout } = useAuth();

  // role_id-based admin check: we'll show admin tabs regardless since
  // the backend enforces permissions. The UI just hides them for non-admins.
  // For a cleaner demo, we show everything.

  return (
    <div style={styles.shell}>
      <aside style={styles.sidebar}>
        <div style={styles.brand}>
          <span style={styles.brandIcon}>◈</span>
          <span style={styles.brandText}>RBAC · RAG</span>
        </div>

        <nav style={styles.nav}>
          {navItems.map((item) => (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === "/"}
              style={({ isActive }) => ({
                ...styles.navLink,
                background: isActive ? "var(--c-bg-active)" : "transparent",
                color: isActive
                  ? "var(--c-primary)"
                  : "var(--c-text-secondary)",
                fontWeight: isActive ? 600 : 400,
              })}
            >
              <span style={styles.navIcon}>{item.icon}</span>
              {item.label}
            </NavLink>
          ))}
        </nav>

        <div style={styles.sidebarFooter}>
          <div style={styles.userPill}>
            <div style={styles.avatar}>
              {(user?.email || "U")[0].toUpperCase()}
            </div>
            <div style={styles.userInfo}>
              <span style={styles.userEmail}>{user?.email || "user"}</span>
            </div>
          </div>
          <button onClick={logout} style={styles.logoutBtn}>
            Sign out
          </button>
        </div>
      </aside>

      <main style={styles.main}>
        <Outlet />
      </main>
    </div>
  );
}

const styles = {
  shell: {
    display: "flex",
    height: "100vh",
    overflow: "hidden",
  },
  sidebar: {
    width: "var(--sidebar-w)",
    minWidth: "var(--sidebar-w)",
    background: "var(--c-bg-sidebar)",
    borderRight: "1px solid var(--c-border)",
    display: "flex",
    flexDirection: "column",
    padding: "20px 12px 16px",
  },
  brand: {
    display: "flex",
    alignItems: "center",
    gap: 8,
    padding: "0 8px 20px",
  },
  brandIcon: {
    fontSize: "1.3rem",
    color: "var(--c-primary)",
  },
  brandText: {
    fontSize: "var(--fs-base)",
    fontWeight: 700,
    letterSpacing: "0.02em",
    color: "var(--c-text-primary)",
  },
  nav: {
    display: "flex",
    flexDirection: "column",
    gap: 2,
    flex: 1,
  },
  navLink: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    padding: "9px 12px",
    borderRadius: "var(--r-md)",
    fontSize: "var(--fs-base)",
    transition: "background 0.15s, color 0.15s",
    textDecoration: "none",
  },
  navIcon: {
    fontSize: "1rem",
    width: 22,
    textAlign: "center",
  },
  sidebarFooter: {
    borderTop: "1px solid var(--c-border)",
    paddingTop: 14,
    display: "flex",
    flexDirection: "column",
    gap: 10,
  },
  userPill: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    padding: "0 4px",
  },
  avatar: {
    width: 30,
    height: 30,
    borderRadius: "var(--r-full)",
    background: "var(--c-primary-light)",
    color: "var(--c-primary)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    fontWeight: 600,
    fontSize: "var(--fs-sm)",
  },
  userInfo: {
    flex: 1,
    overflow: "hidden",
  },
  userEmail: {
    fontSize: "var(--fs-sm)",
    color: "var(--c-text-secondary)",
    whiteSpace: "nowrap",
    overflow: "hidden",
    textOverflow: "ellipsis",
    display: "block",
  },
  logoutBtn: {
    padding: "7px 12px",
    borderRadius: "var(--r-md)",
    fontSize: "var(--fs-sm)",
    color: "var(--c-text-muted)",
    textAlign: "left",
    transition: "background 0.15s, color 0.15s",
  },
  main: {
    flex: 1,
    overflow: "auto",
    display: "flex",
    flexDirection: "column",
  },
};
