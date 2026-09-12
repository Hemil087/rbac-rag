from fastapi import FastAPI
from sqlalchemy import text
from app.api.auth import router as auth_router
from app.api.documents import router as documents_router
from app.db.database import engine
app = FastAPI(
    title = 'RBAC RAG API',
    version = '0.1.0',
)

app.include_router(auth_router)
app.include_router(documents_router)

@app.get('/health')
def health_check():
    return {'status':'ok'}


@app.get('/health/db')
def db_health_check():
    with engine.connect() as conn:
        #print(conn)
        result = conn.execute(text('SELECT 1'))
        value = result.scalar()
        #print(result)
    return {'database':'ok','result':value}