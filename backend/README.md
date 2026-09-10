rbac-rag/
│
├── app/
│   ├── api/                 # API routes/endpoints
│   │   ├── auth.py
│   │   ├── documents.py
│   │   └── chat.py
│   │
│   ├── core/                # Application configuration/security
│   │   ├── config.py
│   │   ├── security.py
│   │   └── dependencies.py
│   │
│   ├── db/                  # Database layer
│   │   ├── database.py
│   │   ├── models.py
│   │   └── repositories/
│   │
│   ├── schemas/              # Pydantic request/response schemas
│   │
│   ├── services/             # Business logic
│   │   ├── auth_service.py
│   │   ├── rbac_service.py
│   │   ├── document_service.py
│   │   └── chat_service.py
│   │
│   ├── rag/                  # RAG pipeline
│   │   ├── loader.py
│   │   ├── chunker.py
│   │   ├── embeddings.py
│   │   ├── retriever.py
│   │   └── generator.py
│   │
│   └── main.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── migrations/               # Alembic database migrations
│
├── data/                     # Local development documents
│
├── docker/
│   └── ...
│
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md