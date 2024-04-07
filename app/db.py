from sqlmodel import create_engine, SQLModel, Session
import os
from dotenv import load_dotenv

load_dotenv()

connection_string = os.getenv("DATABASE_URL")

if connection_string is None:
    raise EnvironmentError("DATABASE_URL not found in .env file.")

engine = create_engine(connection_string, echo=True)

def create_db_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
