from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = "postgresql+psycopg://postgres:postgres@localhost:5432/db_name"

engine = create_engine(db_url)

session = sessionmaker(bind=engine, autoflush=False, autocommit = False)