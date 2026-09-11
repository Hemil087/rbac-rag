from fastapi import FastAPI
from sqlalchemy import text

from app.db.database import engine
app = FastAPI(
    title = 'RBAC RAG API',
    version = '0.1.0',
)
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