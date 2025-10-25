from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


DATABASE_URL = "postgresql+psycopg2://postgres:admin2025@localhost:5432/examfast"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_my_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
