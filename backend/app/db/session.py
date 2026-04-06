import os
from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load the 1987 config
load_dotenv(os.path.join(os.path.dirname(__file__), "../../../.env"))

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://kessel_admin:1987@localhost:5432/kessel_bounty")
engine = create_engine(DATABASE_URL, pool_pre_ping=True)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
