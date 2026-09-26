const BASE = "/api/v1";

function authHeaders() {
  const token = localStorage.getItem("token");
  return token ? { Authorization: `Bearer ${token}` } : {};
}

async function request(path, options = {}) {
  const res = await fetch(`${BASE}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...authHeaders(),
      ...options.headers,
    },
  });

  if (res.status === 401) {
    localStorage.removeItem("token");
    window.location.href = "/login";
    throw new Error("Unauthorized");
  }

  if (res.status === 204) return null;

  const data = await res.json();

  if (!res.ok) {
    throw new Error(data.detail || `Request failed (${res.status})`);
  }
  return data;
}

/* ── Auth ─────────────────────────────────────── */
export const auth = {
  login: (email, password) =>
    request("/auth/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    }),
  me: () => request("/auth/me"),
};

/* ── Documents ────────────────────────────────── */
export const documents = {
  list: () => request("/documents/"),
  listAll: () => request("/documents/all"),
  get: (id) => request(`/documents/${id}`),
  create: (data) =>
    request("/documents/", {
      method: "POST",
      body: JSON.stringify(data),
    }),
  update: (id, data) =>
    request(`/documents/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  remove: (id) => request(`/documents/${id}`, { method: "DELETE" }),

  getPerms: (id) => request(`/documents/${id}/permissions`),
  addPerm: (id, role_id) =>
    request(`/documents/${id}/permissions`, {
      method: "POST",
      body: JSON.stringify({ role_id }),
    }),
  removePerm: (id, role_id) =>
    request(`/documents/${id}/permissions/${role_id}`, { method: "DELETE" }),
  upload: async (file) => {
    const token = localStorage.getItem("token");

    const formData = new FormData();
    formData.append("file", file);

    const res = await fetch(`${BASE}/documents/upload`, {
      method: "POST",
      headers: token
        ? { Authorization: `Bearer ${token}` }
        : {},
      body: formData,
    });

    if (res.status === 401) {
      localStorage.removeItem("token");
      window.location.href = "/login";
      throw new Error("Unauthorized");
    }

    const data = await res.json();

    if (!res.ok) {
      throw new Error(data.detail || `Upload failed (${res.status})`);
    }

    return data;
  },
};

/* ── Users ────────────────────────────────────── */
export const users = {
  list: () => request("/users/"),
  get: (id) => request(`/users/${id}`),
  create: (data) =>
    request("/users/", { method: "POST", body: JSON.stringify(data) }),
  update: (id, data) =>
    request(`/users/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  remove: (id) => request(`/users/${id}`, { method: "DELETE" }),
};

/* ── Roles ────────────────────────────────────── */
export const roles = {
  list: () => request("/roles/"),
  get: (id) => request(`/roles/${id}`),
  create: (data) =>
    request("/roles/", { method: "POST", body: JSON.stringify(data) }),
  update: (id, data) =>
    request(`/roles/${id}`, { method: "PATCH", body: JSON.stringify(data) }),
  remove: (id) => request(`/roles/${id}`, { method: "DELETE" }),
};

/* ── Chat ─────────────────────────────────────── */
export const chat = {
  send: (question, conversation_id = null) =>
    request("/chat/", {
      method: "POST",
      body: JSON.stringify({ question, conversation_id }),
    }),
};

/* ── Conversations ────────────────────────────── */
export const conversations = {
  list: () => request("/conversations/"),
  get: (id) => request(`/conversations/${id}`),
  update: (id, data) =>
    request(`/conversations/${id}`, {
      method: "PATCH",
      body: JSON.stringify(data),
    }),
  remove: (id) => request(`/conversations/${id}`, { method: "DELETE" }),
  messages: (id) => request(`/conversations/${id}/messages`),
};
