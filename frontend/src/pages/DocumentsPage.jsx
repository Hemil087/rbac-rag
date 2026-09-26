import { useState, useEffect, useCallback } from "react";
import { documents, roles as rolesApi } from "../lib/api";

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1048576) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / 1048576).toFixed(1)} MB`;
}

export default function DocumentsPage() {
  const [docs, setDocs] = useState([]);
  const [roles, setRoles] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [showCreate, setShowCreate] = useState(false);
  const [editDoc, setEditDoc] = useState(null);
  const [permsDoc, setPermsDoc] = useState(null);
  const [perms, setPerms] = useState([]);
  const [permRole, setPermRole] = useState("");

  const load = useCallback(async () => {
    setLoading(true);
    try {
      const [d, r] = await Promise.all([
        documents.listAll().catch(() => documents.list()),
        rolesApi.list().catch(() => []),
      ]);
      setDocs(d);
      setRoles(r);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => { load(); }, [load]);

  const handleCreate = async (file) => {
    try {
      await documents.upload(file);
      setShowCreate(false);
      load();
    } catch (e) {
      setError(e.message);
    }
  };

  const handleUpdate = async (id, data) => {
    try {
      await documents.update(id, data);
      setEditDoc(null);
      load();
    } catch (e) {
      setError(e.message);
    }
  };

  const handleDelete = async (id) => {
    if (!confirm("Delete this document?")) return;
    try {
      await documents.remove(id);
      load();
    } catch (e) {
      setError(e.message);
    }
  };

  const openPerms = async (doc) => {
    setPermsDoc(doc);
    try {
      const p = await documents.getPerms(doc.id);
      setPerms(p);
    } catch {
      setPerms([]);
    }
  };

  const addPerm = async () => {
    if (!permRole || !permsDoc) return;
    try {
      await documents.addPerm(permsDoc.id, parseInt(permRole));
      const p = await documents.getPerms(permsDoc.id);
      setPerms(p);
      setPermRole("");
    } catch (e) {
      setError(e.message);
    }
  };

  const removePerm = async (roleId) => {
    try {
      await documents.removePerm(permsDoc.id, roleId);
      const p = await documents.getPerms(permsDoc.id);
      setPerms(p);
    } catch (e) {
      setError(e.message);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.header}>
        <div>
          <h1 style={styles.title}>Documents</h1>
          <p style={styles.desc}>
            Manage your organization's documents and their role-based access.
          </p>
        </div>
        <button onClick={() => setShowCreate(true)} style={styles.primaryBtn}>
          Add document
        </button>
      </div>

      {error && (
        <div style={styles.errorBanner}>
          {error}
          <button onClick={() => setError("")} style={styles.dismissBtn}>×</button>
        </div>
      )}

      {/* Create modal */}
      {showCreate && (
        <UploadModal
          onUpload={handleCreate}
          onCancel={() => setShowCreate(false)}
        />
      )}

      {/* Edit modal */}
      {editDoc && (
        <DocForm
          roles={roles}
          initial={editDoc}
          onSubmit={(data) => handleUpdate(editDoc.id, data)}
          onCancel={() => setEditDoc(null)}
          title="Edit document"
        />
      )}

      {/* Permissions panel */}
      {permsDoc && (
        <div style={styles.overlay} onClick={() => setPermsDoc(null)}>
          <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
            <h2 style={styles.modalTitle}>
              Permissions — {permsDoc.filename}
            </h2>
            <div style={styles.permsList}>
              {perms.length === 0 && (
                <p style={styles.emptyMsg}>No roles have access.</p>
              )}
              {perms.map((p) => (
                <div key={p.role_id} style={styles.permRow}>
                  <span style={styles.permName}>
                    {p.role_name || `Role #${p.role_id}`}
                  </span>
                  <button
                    onClick={() => removePerm(p.role_id)}
                    style={styles.removeBtn}
                  >
                    Revoke
                  </button>
                </div>
              ))}
            </div>
            <div style={styles.permAdd}>
              <select
                value={permRole}
                onChange={(e) => setPermRole(e.target.value)}
                style={styles.select}
              >
                <option value="">Select role…</option>
                {roles
                  .filter((r) => !perms.find((p) => p.role_id === r.id))
                  .map((r) => (
                    <option key={r.id} value={r.id}>
                      {r.role_name}
                    </option>
                  ))}
              </select>
              <button onClick={addPerm} style={styles.primaryBtnSm}>
                Grant access
              </button>
            </div>
            <button
              onClick={() => setPermsDoc(null)}
              style={styles.closeBtn}
            >
              Done
            </button>
          </div>
        </div>
      )}

      {/* Table */}
      {loading ? (
        <p style={styles.loading}>Loading…</p>
      ) : (
        <div style={styles.tableWrap}>
          <table style={styles.table}>
            <thead>
              <tr>
                <th style={styles.th}>Filename</th>
                <th style={styles.th}>Type</th>
                <th style={styles.th}>Size</th>
                <th style={styles.th}>Created</th>
                <th style={{ ...styles.th, textAlign: "right" }}>Actions</th>
              </tr>
            </thead>
            <tbody>
              {docs.map((d) => (
                <tr key={d.id} style={styles.tr}>
                  <td style={styles.td}>
                    <span style={styles.filename}>{d.filename}</span>
                  </td>
                  <td style={styles.td}>
                    <span style={styles.badge}>{d.file_type}</span>
                  </td>
                  <td style={styles.td}>{formatBytes(d.file_size)}</td>
                  <td style={styles.td}>
                    {new Date(d.created_at).toLocaleDateString()}
                  </td>
                  <td style={{ ...styles.td, textAlign: "right" }}>
                    <div style={styles.actions}>
                      <button
                        onClick={() => openPerms(d)}
                        style={styles.actionBtn}
                      >
                        Permissions
                      </button>
                      <button
                        onClick={() => setEditDoc(d)}
                        style={styles.actionBtn}
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDelete(d.id)}
                        style={{ ...styles.actionBtn, color: "var(--c-danger)" }}
                      >
                        Delete
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
              {docs.length === 0 && (
                <tr>
                  <td colSpan={5} style={{ ...styles.td, textAlign: "center" }}>
                    No documents found.
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
function UploadModal({ onUpload, onCancel }) {
  const [file, setFile] = useState(null);
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState("");

  const selectFile = (selectedFile) => {
    if (!selectedFile) return;

    if (selectedFile.type !== "application/pdf") {
      setError("Only PDF files are supported.");
      return;
    }

    if (selectedFile.size > 10 * 1024 * 1024) {
      setError("File size must not exceed 10 MB.");
      return;
    }

    setError("");
    setFile(selectedFile);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);

    const droppedFile = e.dataTransfer.files?.[0];
    selectFile(droppedFile);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setError("Please select a PDF.");
      return;
    }

    setUploading(true);
    setError("");

    try {
      await onUpload(file);
    } catch (err) {
      setError(err.message);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div style={styles.overlay} onClick={onCancel}>
      <div
        style={styles.modal}
        onClick={(e) => e.stopPropagation()}
      >
        <h2 style={styles.modalTitle}>
          Add document
        </h2>

        <form onSubmit={handleSubmit}>
          {/* Drop zone */}
          <label
            style={{
              ...styles.dropZone,
              ...(dragging ? styles.dropZoneDragging : {}),
            }}
            onDragOver={(e) => {
              e.preventDefault();
              setDragging(true);
            }}
            onDragLeave={() => setDragging(false)}
            onDrop={handleDrop}
          >
            <input
              type="file"
              accept="application/pdf,.pdf"
              onChange={(e) =>
                selectFile(e.target.files?.[0])
              }
              style={{ display: "none" }}
            />

            <div style={styles.uploadIcon}>
              📄
            </div>

            <div style={styles.dropTitle}>
              Drag & drop your PDF here
            </div>

            <div style={styles.dropSubtitle}>
              or <span style={styles.browseText}>browse files</span>
            </div>

            <div style={styles.dropHint}>
              PDF files up to 10 MB
            </div>
          </label>

          {/* Selected file */}
          {file && (
            <div style={styles.selectedFile}>
              <div style={styles.fileIcon}>
                📄
              </div>

              <div style={styles.fileInfo}>
                <div style={styles.fileName}>
                  {file.name}
                </div>

                <div style={styles.fileSize}>
                  {formatBytes(file.size)}
                </div>
              </div>

              <button
                type="button"
                onClick={() => setFile(null)}
                style={styles.fileRemove}
              >
                ×
              </button>
            </div>
          )}

          {error && (
            <div style={styles.uploadError}>
              {error}
            </div>
          )}

          <div style={styles.formActions}>
            <button
              type="button"
              onClick={onCancel}
              disabled={uploading}
              style={styles.cancelBtn}
            >
              Cancel
            </button>

            <button
              type="submit"
              disabled={!file || uploading}
              style={{
                ...styles.primaryBtn,
                opacity: !file || uploading ? 0.5 : 1,
              }}
            >
              {uploading ? "Uploading…" : "Upload"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
/* Inline form component for create / edit */
function DocForm({ initial, onSubmit, onCancel, title }) {
  const [filename, setFilename] = useState(initial?.filename || "");
  const [storagePath, setStoragePath] = useState(initial?.storage_path || "");
  const [fileType, setFileType] = useState(initial?.file_type || "pdf");
  const [fileSize, setFileSize] = useState(initial?.file_size || 0);

  const handle = (e) => {
    e.preventDefault();
    onSubmit({
      filename,
      storage_path: storagePath,
      file_type: fileType,
      file_size: parseInt(fileSize),
    });
  };

  return (
    <div style={styles.overlay} onClick={onCancel}>
      <div style={styles.modal} onClick={(e) => e.stopPropagation()}>
        <h2 style={styles.modalTitle}>{title}</h2>
        <form onSubmit={handle} style={styles.form}>
          <label style={styles.formLabel}>
            Filename
            <input
              value={filename}
              onChange={(e) => setFilename(e.target.value)}
              required
              style={styles.formInput}
            />
          </label>
          <label style={styles.formLabel}>
            Storage path
            <input
              value={storagePath}
              onChange={(e) => setStoragePath(e.target.value)}
              required
              style={styles.formInput}
            />
          </label>
          <div style={styles.formRow}>
            <label style={{ ...styles.formLabel, flex: 1 }}>
              File type
              <input
                value={fileType}
                onChange={(e) => setFileType(e.target.value)}
                required
                style={styles.formInput}
              />
            </label>
            <label style={{ ...styles.formLabel, flex: 1 }}>
              Size (bytes)
              <input
                type="number"
                value={fileSize}
                onChange={(e) => setFileSize(e.target.value)}
                required
                style={styles.formInput}
              />
            </label>
          </div>
          <div style={styles.formActions}>
            <button type="button" onClick={onCancel} style={styles.cancelBtn}>
              Cancel
            </button>
            <button type="submit" style={styles.primaryBtn}>
              {initial ? "Save changes" : "Create"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

const styles = {
  page: { padding: "28px 32px", maxWidth: 1000, margin: "0 auto" },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "flex-start",
    marginBottom: 24,
  },
  title: { fontSize: "var(--fs-xxl)", fontWeight: 700, color: "var(--c-text-primary)" },
  desc: { fontSize: "var(--fs-sm)", color: "var(--c-text-muted)", marginTop: 4 },
  primaryBtn: {
    padding: "8px 18px",
    borderRadius: "var(--r-md)",
    background: "var(--c-primary)",
    color: "var(--c-text-on-primary)",
    fontWeight: 500,
    fontSize: "var(--fs-sm)",
  },
  primaryBtnSm: {
    padding: "7px 14px",
    borderRadius: "var(--r-md)",
    background: "var(--c-primary)",
    color: "var(--c-text-on-primary)",
    fontWeight: 500,
    fontSize: "var(--fs-sm)",
  },
  errorBanner: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "10px 14px",
    borderRadius: "var(--r-md)",
    background: "var(--c-danger-light)",
    color: "var(--c-danger)",
    fontSize: "var(--fs-sm)",
    marginBottom: 16,
  },
  dismissBtn: {
    background: "none",
    color: "var(--c-danger)",
    fontSize: "1.1rem",
    fontWeight: 700,
    cursor: "pointer",
  },
  loading: { fontSize: "var(--fs-sm)", color: "var(--c-text-muted)", padding: 20 },
  tableWrap: {
    background: "var(--c-bg-card)",
    borderRadius: "var(--r-lg)",
    border: "1px solid var(--c-border)",
    overflow: "hidden",
  },
  table: { width: "100%", borderCollapse: "collapse" },
  th: {
    textAlign: "left",
    padding: "10px 16px",
    fontSize: "var(--fs-xs)",
    fontWeight: 600,
    color: "var(--c-text-muted)",
    borderBottom: "1px solid var(--c-border)",
    textTransform: "uppercase",
    letterSpacing: "0.04em",
  },
  tr: { borderBottom: "1px solid var(--c-border)" },
  td: {
    padding: "12px 16px",
    fontSize: "var(--fs-sm)",
    color: "var(--c-text-secondary)",
    verticalAlign: "middle",
  },
  filename: { fontWeight: 500, color: "var(--c-text-primary)" },
  badge: {
    display: "inline-block",
    padding: "2px 8px",
    borderRadius: "var(--r-full)",
    background: "var(--c-primary-light)",
    color: "var(--c-primary)",
    fontSize: "var(--fs-xs)",
    fontWeight: 500,
  },
  actions: { display: "flex", gap: 6, justifyContent: "flex-end" },
  actionBtn: {
    padding: "5px 10px",
    borderRadius: "var(--r-sm)",
    fontSize: "var(--fs-xs)",
    fontWeight: 500,
    color: "var(--c-primary)",
    background: "transparent",
    cursor: "pointer",
    transition: "background 0.1s",
  },
  overlay: {
    position: "fixed",
    inset: 0,
    background: "rgba(0,0,0,0.3)",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    zIndex: 100,
  },
  modal: {
    background: "var(--c-bg-card)",
    borderRadius: "var(--r-lg)",
    padding: "28px 28px 24px",
    width: "100%",
    maxWidth: 480,
    boxShadow: "var(--shadow-lg)",
  },
  modalTitle: {
    fontSize: "var(--fs-lg)",
    fontWeight: 600,
    color: "var(--c-text-primary)",
    marginBottom: 20,
  },
  form: { display: "flex", flexDirection: "column", gap: 14 },
  formLabel: {
    display: "flex",
    flexDirection: "column",
    gap: 4,
    fontSize: "var(--fs-sm)",
    fontWeight: 500,
    color: "var(--c-text-secondary)",
  },
  formInput: {
    padding: "8px 12px",
    borderRadius: "var(--r-md)",
    border: "1px solid var(--c-border)",
    fontSize: "var(--fs-base)",
    outline: "none",
  },
  formRow: { display: "flex", gap: 12 },
  formActions: { display: "flex", justifyContent: "flex-end", gap: 10, marginTop: 6 },
  cancelBtn: {
    padding: "8px 16px",
    borderRadius: "var(--r-md)",
    border: "1px solid var(--c-border)",
    fontSize: "var(--fs-sm)",
    fontWeight: 500,
    color: "var(--c-text-secondary)",
    background: "var(--c-bg-card)",
    cursor: "pointer",
  },
  permsList: {
    display: "flex",
    flexDirection: "column",
    gap: 6,
    marginBottom: 16,
    maxHeight: 200,
    overflowY: "auto",
  },
  emptyMsg: { fontSize: "var(--fs-sm)", color: "var(--c-text-muted)", padding: 8 },
  permRow: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "8px 12px",
    borderRadius: "var(--r-md)",
    background: "var(--c-bg-hover)",
  },
  permName: { fontSize: "var(--fs-sm)", fontWeight: 500, color: "var(--c-text-primary)" },
  removeBtn: {
    padding: "4px 10px",
    borderRadius: "var(--r-sm)",
    fontSize: "var(--fs-xs)",
    fontWeight: 500,
    color: "var(--c-danger)",
    background: "var(--c-danger-light)",
    cursor: "pointer",
  },
  permAdd: { display: "flex", gap: 8, marginBottom: 16 },
  select: {
    flex: 1,
    padding: "8px 12px",
    borderRadius: "var(--r-md)",
    border: "1px solid var(--c-border)",
    fontSize: "var(--fs-sm)",
    outline: "none",
  },
  closeBtn: {
    width: "100%",
    padding: "9px",
    borderRadius: "var(--r-md)",
    border: "1px solid var(--c-border)",
    fontSize: "var(--fs-sm)",
    fontWeight: 500,
    color: "var(--c-text-secondary)",
    background: "var(--c-bg-card)",
    cursor: "pointer",
  },
  dropZone: {
    border: "2px dashed var(--c-border)",
    borderRadius: "var(--r-lg)",
    padding: "36px 20px",
    textAlign: "center",
    cursor: "pointer",
    transition: "all 0.15s ease",
    background: "var(--c-bg-hover)",
  },

  dropZoneDragging: {
    borderColor: "var(--c-primary)",
    background: "var(--c-primary-light)",
  },

  uploadIcon: {
    fontSize: "32px",
    marginBottom: 10,
  },

  dropTitle: {
    fontSize: "var(--fs-base)",
    fontWeight: 600,
    color: "var(--c-text-primary)",
  },

  dropSubtitle: {
    marginTop: 4,
    fontSize: "var(--fs-sm)",
    color: "var(--c-text-muted)",
  },

  browseText: {
    color: "var(--c-primary)",
    fontWeight: 600,
  },

  dropHint: {
    marginTop: 12,
    fontSize: "var(--fs-xs)",
    color: "var(--c-text-muted)",
  },

  selectedFile: {
    display: "flex",
    alignItems: "center",
    gap: 10,
    marginTop: 14,
    padding: "10px 12px",
    borderRadius: "var(--r-md)",
    border: "1px solid var(--c-border)",
    background: "var(--c-bg-card)",
  },

  fileIcon: {
    fontSize: "22px",
  },

  fileInfo: {
    flex: 1,
    minWidth: 0,
  },

  fileName: {
    fontSize: "var(--fs-sm)",
    fontWeight: 500,
    color: "var(--c-text-primary)",
    overflow: "hidden",
    textOverflow: "ellipsis",
    whiteSpace: "nowrap",
  },

  fileSize: {
    fontSize: "var(--fs-xs)",
    color: "var(--c-text-muted)",
    marginTop: 2,
  },

  fileRemove: {
    fontSize: "20px",
    color: "var(--c-text-muted)",
    cursor: "pointer",
  },

  uploadError: {
    marginTop: 12,
    padding: "8px 10px",
    borderRadius: "var(--r-md)",
    background: "var(--c-danger-light)",
    color: "var(--c-danger)",
    fontSize: "var(--fs-sm)",
  },
};
