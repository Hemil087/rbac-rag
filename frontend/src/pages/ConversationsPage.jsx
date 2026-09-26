import { useState, useEffect, useCallback } from "react";
import { conversations } from "../lib/api";

export default function ConversationsPage() {
  const [convList, setConvList] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [viewConv, setViewConv] = useState(null);
  const [messages, setMessages] = useState([]);
  const [editConv, setEditConv] = useState(null);
  const [editTitle, setEditTitle] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const c = await conversations.list();
      setConvList(c);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const openConv = async (conv) => {
    setViewConv(conv);
    try {
      const msgs = await conversations.messages(conv.id);
      setMessages(msgs);
    } catch {
      setMessages([]);
    }
  };

  const handleRename = async () => {
    if (!editConv || !editTitle.trim()) return;
    try {
      await conversations.update(editConv.id, { title: editTitle.trim() });
      setEditConv(null);
      load();
    } catch (e) {
      setError(e.message);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm("Delete this conversation and all its messages?")) return;
    try {
      await conversations.remove(id);
      if (viewConv?.id === id) {
        setViewConv(null);
        setMessages([]);
      }
      load();
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div style={s.page}>
      <div style={s.header}>
        <div>
          <h1 style={s.title}>Conversation history</h1>
          <p style={s.desc}>
            Review and manage your past knowledge-base queries.
          </p>
        </div>
      </div>

      {error && (
        <div style={s.errorBanner}>
          {error}
          <button onClick={() => setError("")} style={s.dismissBtn}>×</button>
        </div>
      )}

      {/* Rename modal */}
      {editConv && (
        <div style={s.overlay} onClick={() => setEditConv(null)}>
          <div style={s.modal} onClick={(e) => e.stopPropagation()}>
            <h2 style={s.modalTitle}>Rename conversation</h2>
            <input
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && handleRename()}
              autoFocus
              style={s.formInput}
            />
            <div style={s.formActions}>
              <button onClick={() => setEditConv(null)} style={s.cancelBtn}>
                Cancel
              </button>
              <button onClick={handleRename} style={s.primaryBtn}>
                Save
              </button>
            </div>
          </div>
        </div>
      )}

      {/* Messages viewer */}
      {viewConv && (
        <div style={s.overlay} onClick={() => setViewConv(null)}>
          <div style={s.msgModal} onClick={(e) => e.stopPropagation()}>
            <div style={s.msgModalHeader}>
              <h2 style={s.modalTitle}>{viewConv.title}</h2>
              <button onClick={() => setViewConv(null)} style={s.closeX}>×</button>
            </div>
            <div style={s.msgList}>
              {messages
                .filter((m) => m.role !== "system")
                .map((m) => (
                  <div key={m.id} style={s.msgItem}>
                    <span style={s.msgRole}>
                      {m.role === "user" ? "You" : "Knowledge Base"}
                    </span>
                    <p style={s.msgContent}>{m.content}</p>
                    <span style={s.msgTime}>
                      {new Date(m.created_at).toLocaleString()}
                    </span>
                  </div>
                ))}
              {messages.length === 0 && (
                <p style={s.emptyMsg}>No messages in this conversation.</p>
              )}
            </div>
          </div>
        </div>
      )}

      {loading ? (
        <p style={s.loading}>Loading…</p>
      ) : (
        <div style={s.list}>
          {convList.map((c) => (
            <div key={c.id} style={s.card}>
              <div
                style={s.cardBody}
                onClick={() => openConv(c)}
                role="button"
                tabIndex={0}
              >
                <h3 style={s.cardTitle}>{c.title}</h3>
                <p style={s.cardMeta}>
                  Last activity: {new Date(c.updated_at).toLocaleString()}
                </p>
              </div>
              <div style={s.cardActions}>
                <button
                  onClick={() => {
                    setEditConv(c);
                    setEditTitle(c.title);
                  }}
                  style={s.actionBtn}
                >
                  Rename
                </button>
                <button
                  onClick={() => handleDelete(c.id)}
                  style={{ ...s.actionBtn, color: "var(--c-danger)" }}
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
          {convList.length === 0 && (
            <div style={s.empty}>
              <p style={s.emptyTitle}>No conversations yet</p>
              <p style={s.emptyDesc}>
                Start querying the knowledge base to create conversations.
              </p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}

const s = {
  page: { padding: "28px 32px", maxWidth: 800, margin: "0 auto" },
  header: {
    display: "flex", justifyContent: "space-between",
    alignItems: "flex-start", marginBottom: 24,
  },
  title: { fontSize: "var(--fs-xxl)", fontWeight: 700, color: "var(--c-text-primary)" },
  desc: { fontSize: "var(--fs-sm)", color: "var(--c-text-muted)", marginTop: 4 },
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
  list: { display: "flex", flexDirection: "column", gap: 10 },
  card: {
    background: "var(--c-bg-card)", border: "1px solid var(--c-border)",
    borderRadius: "var(--r-lg)", display: "flex", justifyContent: "space-between",
    alignItems: "center", padding: "16px 20px",
    transition: "box-shadow 0.15s",
  },
  cardBody: { flex: 1, cursor: "pointer" },
  cardTitle: { fontSize: "var(--fs-base)", fontWeight: 500, color: "var(--c-text-primary)" },
  cardMeta: { fontSize: "var(--fs-xs)", color: "var(--c-text-muted)", marginTop: 3 },
  cardActions: { display: "flex", gap: 6 },
  actionBtn: {
    padding: "5px 10px", borderRadius: "var(--r-sm)",
    fontSize: "var(--fs-xs)", fontWeight: 500, color: "var(--c-primary)",
    background: "transparent", cursor: "pointer",
  },
  empty: { textAlign: "center", padding: 40 },
  emptyTitle: { fontSize: "var(--fs-lg)", fontWeight: 600, color: "var(--c-text-primary)" },
  emptyDesc: { fontSize: "var(--fs-sm)", color: "var(--c-text-muted)", marginTop: 4 },
  emptyMsg: { fontSize: "var(--fs-sm)", color: "var(--c-text-muted)", padding: 20 },

  overlay: {
    position: "fixed", inset: 0, background: "rgba(0,0,0,0.3)",
    display: "flex", alignItems: "center", justifyContent: "center", zIndex: 100,
  },
  modal: {
    background: "var(--c-bg-card)", borderRadius: "var(--r-lg)",
    padding: "28px 28px 24px", width: "100%", maxWidth: 400,
    boxShadow: "var(--shadow-lg)",
    display: "flex", flexDirection: "column", gap: 14,
  },
  msgModal: {
    background: "var(--c-bg-card)", borderRadius: "var(--r-lg)",
    width: "100%", maxWidth: 600, maxHeight: "80vh",
    boxShadow: "var(--shadow-lg)", display: "flex", flexDirection: "column",
    overflow: "hidden",
  },
  msgModalHeader: {
    display: "flex", justifyContent: "space-between", alignItems: "center",
    padding: "20px 24px 0",
  },
  closeX: {
    width: 30, height: 30, borderRadius: "var(--r-md)",
    display: "flex", alignItems: "center", justifyContent: "center",
    fontSize: "1.2rem", color: "var(--c-text-muted)", cursor: "pointer",
  },
  modalTitle: {
    fontSize: "var(--fs-lg)", fontWeight: 600, color: "var(--c-text-primary)",
  },
  msgList: {
    flex: 1, overflowY: "auto", padding: "16px 24px 24px",
    display: "flex", flexDirection: "column", gap: 14,
  },
  msgItem: {
    padding: "12px 14px", borderRadius: "var(--r-md)",
    background: "var(--c-bg-hover)",
  },
  msgRole: {
    display: "block", fontSize: "var(--fs-xs)", fontWeight: 600,
    color: "var(--c-text-muted)", marginBottom: 4,
    textTransform: "uppercase", letterSpacing: "0.03em",
  },
  msgContent: {
    fontSize: "var(--fs-sm)", color: "var(--c-text-primary)", lineHeight: 1.6,
    whiteSpace: "pre-wrap",
  },
  msgTime: {
    display: "block", fontSize: "var(--fs-xs)", color: "var(--c-text-muted)",
    marginTop: 6, fontFamily: "var(--font-mono)",
  },
  formInput: {
    padding: "8px 12px", borderRadius: "var(--r-md)",
    border: "1px solid var(--c-border)", fontSize: "var(--fs-base)",
    outline: "none", width: "100%",
  },
  formActions: { display: "flex", justifyContent: "flex-end", gap: 10 },
  cancelBtn: {
    padding: "8px 16px", borderRadius: "var(--r-md)",
    border: "1px solid var(--c-border)", fontSize: "var(--fs-sm)",
    fontWeight: 500, color: "var(--c-text-secondary)",
    background: "var(--c-bg-card)", cursor: "pointer",
  },
  primaryBtn: {
    padding: "8px 18px", borderRadius: "var(--r-md)",
    background: "var(--c-primary)", color: "var(--c-text-on-primary)",
    fontWeight: 500, fontSize: "var(--fs-sm)",
  },
};
