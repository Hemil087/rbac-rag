import { useState, useRef, useEffect } from "react";
import ReactMarkdown from "react-markdown";
import { chat, conversations } from "../lib/api";

export default function ChatPage() {
  const [convId, setConvId] = useState(null);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [sending, setSending] = useState(false);
  const [history, setHistory] = useState([]);
  const [showHistory, setShowHistory] = useState(false);
  const bottomRef = useRef(null);

  useEffect(() => {
    conversations.list().then(setHistory).catch(() => {});
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const loadConversation = async (id) => {
    try {
      const msgs = await conversations.messages(id);
      setMessages(
        msgs
          .filter((m) => m.role !== "system")
          .map((m) => ({ role: m.role, content: m.content }))
      );
      setConvId(id);
      setShowHistory(false);
    } catch {
      /* ignore */
    }
  };

  const handleSend = async () => {
    const q = input.trim();
    if (!q || sending) return;

    setMessages((prev) => [...prev, { role: "user", content: q }]);
    setInput("");
    setSending(true);

    try {
      const res = await chat.send(q, convId);
      setConvId(res.conversation_id);
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: res.answer,
          sources: res.sources,
        },
      ]);
      conversations.list().then(setHistory).catch(() => {});
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: `Error: ${err.message}` },
      ]);
    } finally {
      setSending(false);
    }
  };

  const startNew = () => {
    setConvId(null);
    setMessages([]);
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <div style={styles.container}>
      {/* Top bar */}
      <div style={styles.topbar}>
        <div style={styles.topLeft}>
          <button onClick={startNew} style={styles.newBtn}>
            + New query
          </button>
          <button
            onClick={() => setShowHistory(!showHistory)}
            style={styles.histBtn}
          >
            {showHistory ? "Hide history" : "Recent"}
          </button>
        </div>
        {convId && (
          <span style={styles.convLabel}>Conversation #{convId}</span>
        )}
      </div>

      {/* History dropdown */}
      {showHistory && history.length > 0 && (
        <div style={styles.historyPanel}>
          {history.slice(0, 20).map((c) => (
            <button
              key={c.id}
              onClick={() => loadConversation(c.id)}
              style={{
                ...styles.histItem,
                background:
                  c.id === convId ? "var(--c-bg-active)" : "transparent",
              }}
            >
              <span style={styles.histTitle}>{c.title}</span>
              <span style={styles.histDate}>
                {new Date(c.updated_at).toLocaleDateString()}
              </span>
            </button>
          ))}
        </div>
      )}

      {/* Messages area */}
      <div style={styles.messagesWrap}>
        {messages.length === 0 && (
          <div style={styles.empty}>
            <div style={styles.emptyIcon}>◈</div>
            <p style={styles.emptyTitle}>Query your knowledge base</p>
            <p style={styles.emptyDesc}>
              Ask a question about documents you have access to.
              Answers are grounded in your organization's files and
              scoped to your role permissions.
            </p>
          </div>
        )}

        {messages.map((m, i) => (
          <div
            key={i}
            style={{
              ...styles.msgRow,
              justifyContent:
                m.role === "user" ? "flex-end" : "flex-start",
            }}
          >
            <div
              style={{
                ...styles.bubble,
                background:
                  m.role === "user"
                    ? "var(--c-chat-user)"
                    : "var(--c-chat-assistant)",
                borderBottomRightRadius:
                  m.role === "user" ? "4px" : "var(--r-lg)",
                borderBottomLeftRadius:
                  m.role === "user" ? "var(--r-lg)" : "4px",
              }}
            >
              <span style={styles.roleTag}>
                {m.role === "user" ? "You" : "Knowledge Base"}
              </span>
              <div style={styles.msgText}>
                <ReactMarkdown
                  components={{
                    p: ({ children }) => (
                      <p style={styles.mdParagraph}>{children}</p>
                    ),

                    h1: ({ children }) => (
                      <h1 style={styles.mdHeading1}>{children}</h1>
                    ),

                    h2: ({ children }) => (
                      <h2 style={styles.mdHeading2}>{children}</h2>
                    ),

                    h3: ({ children }) => (
                      <h3 style={styles.mdHeading3}>{children}</h3>
                    ),

                    ul: ({ children }) => (
                      <ul style={styles.mdUnorderedList}>{children}</ul>
                    ),

                    ol: ({ children }) => (
                      <ol style={styles.mdOrderedList}>{children}</ol>
                    ),

                    li: ({ children }) => (
                      <li style={styles.mdListItem}>{children}</li>
                    ),

                    blockquote: ({ children }) => (
                      <blockquote style={styles.mdBlockquote}>
                        {children}
                      </blockquote>
                    ),

                    code: ({ inline, children }) =>
                      inline ? (
                        <code style={styles.mdInlineCode}>
                          {children}
                        </code>
                      ) : (
                        <code style={styles.mdCodeBlock}>
                          {children}
                        </code>
                      ),

                    strong: ({ children }) => (
                      <strong style={styles.mdStrong}>{children}</strong>
                    ),

                    em: ({ children }) => (
                      <em style={styles.mdEm}>{children}</em>
                    ),
                  }}
                >
                  {m.content}
                </ReactMarkdown>
              </div>
              {m.sources && m.sources.length > 0 && (
                <div style={styles.sources}>
                  {m.sources.map((s, j) => (
                    <span key={j} style={styles.sourceTag}>
                      Doc {s.document_id} · Chunk {s.chunk_index}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>
        ))}

        {sending && (
          <div style={{ ...styles.msgRow, justifyContent: "flex-start" }}>
            <div
              style={{
                ...styles.bubble,
                background: "var(--c-chat-assistant)",
                borderBottomLeftRadius: "4px",
              }}
            >
              <span style={styles.roleTag}>Knowledge Base</span>
              <p style={{ ...styles.msgText, color: "var(--c-text-muted)" }}>
                Searching documents…
              </p>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input area */}
      <div style={styles.inputBar}>
        <div style={styles.inputWrap}>
          <textarea
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="Ask a question…"
            rows={1}
            style={styles.textarea}
          />
          <button
            onClick={handleSend}
            disabled={sending || !input.trim()}
            style={{
              ...styles.sendBtn,
              opacity: sending || !input.trim() ? 0.4 : 1,
            }}
          >
            ↑
          </button>
        </div>
      </div>
    </div>
  );
}

const styles = {
  container: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    height: "100%",
  },
  topbar: {
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "12px 20px",
    borderBottom: "1px solid var(--c-border)",
    background: "var(--c-bg-card)",
  },
  topLeft: {
    display: "flex",
    gap: 8,
  },
  newBtn: {
    padding: "6px 14px",
    borderRadius: "var(--r-md)",
    background: "var(--c-primary)",
    color: "var(--c-text-on-primary)",
    fontSize: "var(--fs-sm)",
    fontWeight: 500,
  },
  histBtn: {
    padding: "6px 14px",
    borderRadius: "var(--r-md)",
    border: "1px solid var(--c-border)",
    fontSize: "var(--fs-sm)",
    color: "var(--c-text-secondary)",
    background: "var(--c-bg-card)",
  },
  convLabel: {
    fontSize: "var(--fs-xs)",
    color: "var(--c-text-muted)",
    fontFamily: "var(--font-mono)",
  },
  historyPanel: {
    borderBottom: "1px solid var(--c-border)",
    background: "var(--c-bg-card)",
    padding: "8px 12px",
    maxHeight: 240,
    overflowY: "auto",
    display: "flex",
    flexDirection: "column",
    gap: 2,
  },
  histItem: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "8px 12px",
    borderRadius: "var(--r-md)",
    cursor: "pointer",
    border: "none",
    textAlign: "left",
    width: "100%",
    transition: "background 0.1s",
  },
  histTitle: {
    fontSize: "var(--fs-sm)",
    color: "var(--c-text-primary)",
    overflow: "hidden",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",
    flex: 1,
  },
  histDate: {
    fontSize: "var(--fs-xs)",
    color: "var(--c-text-muted)",
    marginLeft: 12,
    whiteSpace: "nowrap",
  },

  messagesWrap: {
    flex: 1,
    overflowY: "auto",
    padding: "24px 20px",
    display: "flex",
    flexDirection: "column",
    gap: 12,
  },
  empty: {
    flex: 1,
    display: "flex",
    flexDirection: "column",
    alignItems: "center",
    justifyContent: "center",
    textAlign: "center",
    gap: 8,
    padding: 40,
  },
  emptyIcon: {
    fontSize: "2.5rem",
    color: "var(--c-primary)",
    marginBottom: 8,
  },
  emptyTitle: {
    fontSize: "var(--fs-lg)",
    fontWeight: 600,
    color: "var(--c-text-primary)",
  },
  emptyDesc: {
    fontSize: "var(--fs-sm)",
    color: "var(--c-text-muted)",
    maxWidth: 400,
    lineHeight: 1.6,
  },
  msgRow: {
    display: "flex",
  },
  bubble: {
    maxWidth: "72%",
    padding: "12px 16px",
    borderRadius: "var(--r-lg)",
  },
  roleTag: {
    display: "block",
    fontSize: "var(--fs-xs)",
    fontWeight: 600,
    color: "var(--c-text-muted)",
    marginBottom: 4,
    textTransform: "uppercase",
    letterSpacing: "0.03em",
  },
  msgText: {
    fontSize: "var(--fs-base)",
    color: "var(--c-text-primary)",
    lineHeight: 1.6,
    maxWidth: "900px",
    overflowWrap: "break-word",
  },
  sources: {
    display: "flex",
    flexWrap: "wrap",
    gap: 6,
    marginTop: 8,
  },
  sourceTag: {
    padding: "3px 8px",
    borderRadius: "var(--r-sm)",
    background: "var(--c-bg-app)",
    fontSize: "var(--fs-xs)",
    color: "var(--c-text-muted)",
    fontFamily: "var(--font-mono)",
  },

  inputBar: {
    borderTop: "1px solid var(--c-border)",
    padding: "14px 20px",
    background: "var(--c-bg-card)",
  },
  inputWrap: {
    display: "flex",
    alignItems: "flex-end",
    gap: 10,
    maxWidth: 720,
    margin: "0 auto",
    border: "1px solid var(--c-border)",
    borderRadius: "var(--r-lg)",
    padding: "6px 6px 6px 16px",
    background: "var(--c-bg-input)",
  },
  textarea: {
    flex: 1,
    border: "none",
    outline: "none",
    resize: "none",
    background: "transparent",
    fontSize: "var(--fs-base)",
    lineHeight: 1.5,
    padding: "6px 0",
    maxHeight: 120,
  },
  sendBtn: {
    width: 34,
    height: 34,
    borderRadius: "var(--r-md)",
    background: "var(--c-primary)",
    color: "var(--c-text-on-primary)",
    fontSize: "1.1rem",
    fontWeight: 700,
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    flexShrink: 0,
    transition: "opacity 0.15s",
  },
  mdParagraph: {
    margin: "0 0 14px 0",
    lineHeight: 1.65,
  },

  mdHeading1: {
    margin: "20px 0 10px 0",
    fontSize: "22px",
    lineHeight: 1.3,
    fontWeight: 700,
  },

  mdHeading2: {
    margin: "18px 0 8px 0",
    fontSize: "19px",
    lineHeight: 1.35,
    fontWeight: 700,
  },

  mdHeading3: {
    margin: "16px 0 7px 0",
    fontSize: "17px",
    lineHeight: 1.4,
    fontWeight: 650,
  },

  mdUnorderedList: {
    margin: "8px 0 16px 0",
    paddingLeft: "24px",
  },

  mdOrderedList: {
    margin: "8px 0 16px 0",
    paddingLeft: "28px",
  },

  mdListItem: {
    margin: "5px 0",
    paddingLeft: "4px",
    lineHeight: 1.6,
  },

  mdStrong: {
    fontWeight: 700,
  },

  mdEm: {
    fontStyle: "italic",
  },

  mdInlineCode: {
    padding: "2px 6px",
    borderRadius: "5px",
    background: "var(--c-bg-app)",
    fontFamily: "var(--font-mono)",
    fontSize: "0.9em",
  },

  mdCodeBlock: {
    display: "block",
    margin: "12px 0",
    padding: "14px 16px",
    borderRadius: "8px",
    background: "var(--c-bg-app)",
    overflowX: "auto",
    fontFamily: "var(--font-mono)",
    fontSize: "13px",
    lineHeight: 1.55,
  },

  mdBlockquote: {
    margin: "14px 0",
    padding: "8px 16px",
    borderLeft: "3px solid var(--c-primary)",
    color: "var(--c-text-muted)",
    lineHeight: 1.6,
  },
};
