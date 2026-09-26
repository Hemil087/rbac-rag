# RBAC RAG — Frontend

React frontend for the RBAC RAG knowledge-base platform.

## Setup

```bash
cd frontend
npm install
npm run dev
```

The dev server starts on `http://localhost:5173` and proxies
`/api` requests to the backend on port 8000.

## Theme customization

All colors, fonts, radii, and shadows are defined in
`src/theme.js`. Edit any value there to change the entire
app's appearance — every component reads from CSS custom
properties that are generated from this file.

## Demo accounts (from seed data)

| Email              | Password    | Role     |
|--------------------|-------------|----------|
| admin@acme.com     | admin123    | admin    |
| manager@acme.com   | manager123  | manager  |
| employee@acme.com  | employee123 | employee |
| admin@globex.com   | admin123    | admin    |
| employee@globex.com| employee123 | employee |

Admin users can access Documents, Users, and Roles pages.
All users can use the Knowledge Base chat and view Conversations.
