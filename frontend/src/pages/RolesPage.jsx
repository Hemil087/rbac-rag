import { useState, useEffect, useCallback } from "react";
import { roles as rolesApi } from "../lib/api";

export default function RolesPage() {
  const [roleList, setRoleList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [editRole, setEditRole] = useState(null);

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const r = await rolesApi.list();
      setRoleList(r);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleCreate = async (data) => {
    try {
      await rolesApi.create(data);
      setShowCreate(false);
      load();
    } catch (e) {
      setError(e.message);
    }
  };

  const handleUpdate = async (id, data) => {
    try {
      await rolesApi.update(id, data);
      setEditRole(null);
      load();
    } catch (e) {
      setError(e.message);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm("Delete this role? This may fail if users or permissions reference it.")) return;
    try {
      await rolesApi.remove(id);
      load();
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div style={s.page}>
      <div style={s.header}>
        <div>
          <h1 style={s.title}>Roles</h1>
          <p style={s.desc}>
            Define roles used for document access control.
          </p>
        </div>
        <button onClick={() => setShowCreate(true)} style={s.primaryBtn}>
          Add role
        </button>
      </div>

      {error && (
        <div style={s.errorBanner}>
          {error}
          <button onClick={() => setError("")} style={s.dismissBtn}>×</button>
        </div>
      )}

      {showCreate && (
        <RoleForm
          onSubmit={handleCreate}
          onCancel={() => setShowCreate(false)}
          title="Add role"
        />
      )}

      {editRole && (
        <RoleForm
          initial={editRole}
          onSubmit={(data) => handleUpdate(editRole.id, data)}
          onCancel={() => setEditRole(null)}
          title="Edit role"
        />
      )}

      {loading ? (
        <p style={s.loading}>Loading…</p>
      ) : (
        <div style={s.grid}>
          {roleList.map((r) => (
            <div key={r.id} style={s.card}>
              <div style={s.cardTop}>
                <span style={s.cardIcon}>🔑</span>
                <h3 style={s.cardName}>{r.role_name}</h3>
              </div>
              <p style={s.cardMeta}>
                Created {new Date(r.created_at).toLocaleDateString()}
              </p>
              <div style={s.cardActions}>
                <button onClick={() => setEditRole(r)} style={s.cardBtn}>
                  Rename
                </button>
                <button
                  onClick={() => handleDelete(r.id)}
                  style={{ ...s.cardBtn, color: "var(--c-danger)" }}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
          {roleList.length === 0 && (
            <p style={s.emptyMsg}>No roles defined.</p>
          )}
        </div>
      )}
    </div>
  );
}

function RoleForm({ initial, onSubmit, onCancel, title }) {
  const [name, setName] = useState(initial?.role_name || "");

  const handle = (e) => {
    e.preventDefault();
    onSubmit({ role_name: name });
  };

  return (
    <div style={s.overlay} onClick={onCancel}>
      <div style={s.modal} onClick={(e) => e.stopPropagation()}>
        <h2 style={s.modalTitle}>{title}</h2>
        <form onSubmit={handle} style={s.form}>
          <label style={s.formLabel}>
            Role name
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
              placeholder="e.g. viewer"
              style={s.formInput}
            />
          </label>
          <div style={s.formActions}>
            <button type="button" onClick={onCancel} style={s.cancelBtn}>
              Cancel
            </button>
            <button type="submit" style={s.primaryBtn}>
              {initial ? "Save" : "Create"}
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
    background: "none", color: "var(--c-danger)", fontSize: "1.1rem", fontWeight: 700,
  },
  loading: { fontSize: "var(--fs-sm)", color: "var(--c-text-muted)", padding: 20 },
  grid: {
    display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(240px, 1fr))", gap: 14,
  },
  card: {
    background: "var(--c-bg-card)", border: "1px solid var(--c-border)",
    borderRadius: "var(--r-lg)", padding: "18px 20px",
    display: "flex", flexDirection: "column", gap: 8,
  },
  cardTop: { display: "flex", alignItems: "center", gap: 8 },
  cardIcon: { fontSize: "1.1rem" },
  cardName: {
    fontSize: "var(--fs-base)", fontWeight: 600, color: "var(--c-text-primary)",
    textTransform: "capitalize",
  },
  cardMeta: { fontSize: "var(--fs-xs)", color: "var(--c-text-muted)" },
  cardActions: { display: "flex", gap: 8, marginTop: 4 },
  cardBtn: {
    padding: "5px 10px", borderRadius: "var(--r-sm)",
    fontSize: "var(--fs-xs)", fontWeight: 500, color: "var(--c-primary)",
    background: "transparent", cursor: "pointer",
  },
  emptyMsg: { fontSize: "var(--fs-sm)", color: "var(--c-text-muted)" },
  overlay: {
    position: "fixed", inset: 0, background: "rgba(0,0,0,0.3)",
    display: "flex", alignItems: "center", justifyContent: "center", zIndex: 100,
  },
  modal: {
    background: "var(--c-bg-card)", borderRadius: "var(--r-lg)",
    padding: "28px 28px 24px", width: "100%", maxWidth: 400,
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
  formActions: { display: "flex", justifyContent: "flex-end", gap: 10, marginTop: 6 },
  cancelBtn: {
    padding: "8px 16px", borderRadius: "var(--r-md)",
    border: "1px solid var(--c-border)", fontSize: "var(--fs-sm)",
    fontWeight: 500, color: "var(--c-text-secondary)",
    background: "var(--c-bg-card)", cursor: "pointer",
  },
};
