from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql+psycopg://postgres:postgres@localhost:5432/wallet_db"

engine = create_engine(db_url)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit = False)

def get_db():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()