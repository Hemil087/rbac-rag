import { useState, useEffect, useCallback } from "react";
import { users, roles as rolesApi } from "../lib/api";

export default function UsersPage() {
  const [userList, setUserList] = useState([]);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [editUser, setEditUser] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [u, r] = await Promise.all([users.list(), rolesApi.list().catch(() => [])]);
      setUserList(u);
      setRoles(r);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleCreate = async (data) => {
    try {
      await users.create(data);
      setShowCreate(false);
      load();
    } catch (e) {
      setError(e.message);
    }
  };

  const handleUpdate = async (id, data) => {
    try {
      await users.update(id, data);
      setEditUser(null);
      load();
    } catch (e) {
      setError(e.message);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm("Delete this user?")) return;
    try {
      await users.remove(id);
      load();
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div style={s.page}>
      <div style={s.header}>
        <div>
          <h1 style={s.title}>Users</h1>
          <p style={s.desc}>Manage user accounts in your organization.</p>
        </div>
        <button onClick={() => setShowCreate(true)} style={s.primaryBtn}>
          Add user
        </button>
      </div>

      {error && (
        <div style={s.errorBanner}>
          {error}
          <button onClick={() => setError("")} style={s.dismissBtn}>×</button>
        </div>
      )}

      {showCreate && (
        <UserForm
          roles={roles}
          onSubmit={handleCreate}
          onCancel={() => setShowCreate(false)}
          title="Add user"
        />
      )}

      {editUser && (
        <UserForm
          roles={roles}
          initial={editUser}
          onSubmit={(data) => handleUpdate(editUser.id, data)}
          onCancel={() => setEditUser(null)}
          title="Edit user"
        />
      )}

      {loading ? (
        <p style={s.loading}>Loading…</p>
      ) : (
        <div style={s.tableWrap}>
          <table style={s.table}>
            <thead>
              <tr>
                <th style={s.th}>Email</th>
                <th style={s.th}>Role</th>
                <th style={s.th}>Created</th>
                <th style={{ ...s.th, textAlign: "right" }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {userList.map((u) => (
                <tr key={u.id} style={s.tr}>
                  <td style={s.td}>
                    <span style={s.email}>{u.email}</span>
                  </td>
                  <td style={s.td}>
                    <span style={s.badge}>{u.role_name || `#${u.role_id}`}</span>
                  </td>
                  <td style={s.td}>
                    {new Date(u.created_at).toLocaleDateString()}
                  </td>
                  <td style={{ ...s.td, textAlign: "right" }}>
                    <div style={s.actions}>
                      <button onClick={() => setEditUser(u)} style={s.actionBtn}>
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(u.id)}
                        style={{ ...s.actionBtn, color: "var(--c-danger)" }}
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
              {userList.length === 0 && (
                <tr>
                  <td colSpan={4} style={{ ...s.td, textAlign: "center" }}>
                    No users found.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}

function UserForm({ initial, roles, onSubmit, onCancel, title }) {
  const [email, setEmail] = useState(initial?.email || "");
  const [password, setPassword] = useState("");
  const [roleId, setRoleId] = useState(initial?.role_id?.toString() || "");

  const handle = (e) => {
    e.preventDefault();
    const data = {};
    if (email) data.email = email;
    if (password) data.password = password;
    if (roleId) data.role_id = parseInt(roleId);
    onSubmit(data);
  };

  return (
    <div style={s.overlay} onClick={onCancel}>
      <div style={s.modal} onClick={(e) => e.stopPropagation()}>
        <h2 style={s.modalTitle}>{title}</h2>
        <form onSubmit={handle} style={s.form}>
          <label style={s.formLabel}>
            Email
            <input
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required={!initial}
              style={s.formInput}
            />
          </label>
          <label style={s.formLabel}>
            Password {initial && "(leave blank to keep current)"}
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required={!initial}
              minLength={6}
              style={s.formInput}
            />
          </label>
          <label style={s.formLabel}>
            Role
            <select
              value={roleId}
              onChange={(e) => setRoleId(e.target.value)}
              required={!initial}
              style={s.formInput}
            >
              <option value="">Select role…</option>
              {roles.map((r) => (
                <option key={r.id} value={r.id}>
                  {r.role_name}
                </option>
              ))}
            </select>
          </label>
          <div style={s.formActions}>
            <button type="button" onClick={onCancel} style={s.cancelBtn}>
              Cancel
            </button>
            <button type="submit" style={s.primaryBtn}>
              {initial ? "Save changes" : "Create"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

const s = {
  page: { padding: "28px 32px", maxWidth: 1000, margin: "0 auto" },
  header: {
    display: "flex", justifyContent: "space-between",
    alignItems: "flex-start", marginBottom: 24,
  },
  title: { fontSize: "var(--fs-xxl)", fontWeight: 700, color: "var(--c-text-primary)" },
  desc: { fontSize: "var(--fs-sm)", color: "var(--c-text-muted)", marginTop: 4 },
  primaryBtn: {
    padding: "8px 18px", borderRadius: "var(--r-md)",
    background: "var(--c-primary)", color: "var(--c-text-on-primary)",
    fontWeight: 500, fontSize: "var(--fs-sm)",
  },
  errorBanner: {
    display: "flex", justifyContent: "space-between", alignItems: "center",
    padding: "10px 14px", borderRadius: "var(--r-md)",
    background: "var(--c-danger-light)", color: "var(--c-danger)",
    fontSize: "var(--fs-sm)", marginBottom: 16,
  },
  dismissBtn: {
    background: "none", color: "var(--c-danger)",
    fontSize: "1.1rem", fontWeight: 700,
  },
  loading: { fontSize: "var(--fs-sm)", color: "var(--c-text-muted)", padding: 20 },
  tableWrap: {
    background: "var(--c-bg-card)", borderRadius: "var(--r-lg)",
    border: "1px solid var(--c-border)", overflow: "hidden",
  },
  table: { width: "100%", borderCollapse: "collapse" },
  th: {
    textAlign: "left", padding: "10px 16px",
    fontSize: "var(--fs-xs)", fontWeight: 600,
    color: "var(--c-text-muted)", borderBottom: "1px solid var(--c-border)",
    textTransform: "uppercase", letterSpacing: "0.04em",
  },
  tr: { borderBottom: "1px solid var(--c-border)" },
  td: {
    padding: "12px 16px", fontSize: "var(--fs-sm)",
    color: "var(--c-text-secondary)", verticalAlign: "middle",
  },
  email: { fontWeight: 500, color: "var(--c-text-primary)" },
  badge: {
    display: "inline-block", padding: "2px 8px",
    borderRadius: "var(--r-full)", background: "var(--c-primary-light)",
    color: "var(--c-primary)", fontSize: "var(--fs-xs)", fontWeight: 500,
  },
  actions: { display: "flex", gap: 6, justifyContent: "flex-end" },
  actionBtn: {
    padding: "5px 10px", borderRadius: "var(--r-sm)",
    fontSize: "var(--fs-xs)", fontWeight: 500, color: "var(--c-primary)",
    background: "transparent", cursor: "pointer",
  },
  overlay: {
    position: "fixed", inset: 0, background: "rgba(0,0,0,0.3)",
    display: "flex", alignItems: "center", justifyContent: "center", zIndex: 100,
  },
  modal: {
    background: "var(--c-bg-card)", borderRadius: "var(--r-lg)",
    padding: "28px 28px 24px", width: "100%", maxWidth: 440,
    boxShadow: "var(--shadow-lg)",
  },
  modalTitle: {
    fontSize: "var(--fs-lg)", fontWeight: 600,
    color: "var(--c-text-primary)", marginBottom: 20,
  },
  form: { display: "flex", flexDirection: "column", gap: 14 },
  formLabel: {
    display: "flex", flexDirection: "column", gap: 4,
    fontSize: "var(--fs-sm)", fontWeight: 500, color: "var(--c-text-secondary)",
  },
  formInput: {
    padding: "8px 12px", borderRadius: "var(--r-md)",
    border: "1px solid var(--c-border)", fontSize: "var(--fs-base)", outline: "none",
  },
  formActions: {
    display: "flex", justifyContent: "flex-end", gap: 10, marginTop: 6,
  },
  cancelBtn: {
    padding: "8px 16px", borderRadius: "var(--r-md)",
    border: "1px solid var(--c-border)", fontSize: "var(--fs-sm)",
    fontWeight: 500, color: "var(--c-text-secondary)",
    background: "var(--c-bg-card)", cursor: "pointer",
  },
};
