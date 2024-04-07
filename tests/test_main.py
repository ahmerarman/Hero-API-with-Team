import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.db import get_session
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool
from hero_api.model.database import Hero, Team
import os
from dotenv import load_dotenv
#from app import settings

load_dotenv()

connection_string = os.getenv("TEST_DATABASE_URL")
"""connection_string = str(settings.TEST_DATABASE_URL).replace(
    "postgresql", "postgresql+psycopg")"""

if connection_string is None:
    raise EnvironmentError("TEST_DATABASE_URL not found in .env file.")

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(connection_string, echo=True)
    """engine = create_engine(connection_string,
                            connect_args={"sslmode": "require"}, 
                            pool_recycle=300,
                            echo=True
                        )"""
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    # sourcery skip: inline-immediately-yielded-variable
    def get_session_override():
        return session
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

def test_root_path():
    client = TestClient(app=app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"Hello! World. Hero API is running."}

def test_create_hero(client: TestClient):
    response = client.post(
        "/heroes/", json={
            "name": "Tariq bin Arman",
            "secret_name": "TA",
            "age": 75,
            "team_id": 1
        }
    )
    data = response.json()
    
    assert response.status_code == 200
    assert data["name"] == "Tariq bin Arman"
    assert data["secret_name"] == "TA"
    assert data["age"] == 75
    assert data["team_id"] == 1
    assert data["id"] is not None

def test_create_team(client: TestClient):
    response = client.post(
        "/teams/", json={
            "name": "Team 1",
            "headquarters": "Karachi",
        }
    )
    data = response.json()
    
    assert response.status_code == 200
    assert data["name"] == "Team 1"
    assert data["headquarters"] == "Karachi"

def test_create_hero_incomplete(client: TestClient):
    # No secret_name
    response = client.post(
        "/heroes/", json={
            "name": "Tariq bin Arman"
        }
    )
    assert response.status_code == 422

def test_create_team_incomplete(client: TestClient):
    # No headquarters
    response = client.post(
        "/teams/", json={
            "team_name": "Team 1"
        }
    )
    assert response.status_code == 422

def test_create_hero_invalid(client: TestClient):
    # secret_name has an invalid type
    response = client.post(
        "/heroes/",
        json={
            "name": "Tariq bin Arman",
            "secret_name": {"message": "Do you wanna know my secret identity?"},
        },
    )
    assert response.status_code == 422

def test_create_team_invalid(client: TestClient):
    # headquarters has an invalid type
    response = client.post(
        "/teams/",
        json={
            "name": "Team 1",
            "headquarters": {"message": "Do you wanna know my secret identity?"},
        },
    )
    assert response.status_code == 422

def test_read_heroes(session: Session, client: TestClient):
    hero_1 = Hero(name="Tariq bin Arman", secret_name="TA", age=70, team_id=1)
    hero_2 = Hero(name="Syed Shahabuddin", secret_name="SS", age=75, team_id=2)
    session.add(hero_1)
    session.add(hero_2)
    session.commit()

    response = client.get("/heroes/")
    data = response.json()
    length = len(data)

    assert response.status_code == 200

    assert len(data) == length
    assert data[length-2]["name"] == hero_1.name
    assert data[length-2]["secret_name"] == hero_1.secret_name
    assert data[length-2]["age"] == hero_1.age
    assert data[length-2]["id"] == hero_1.id
    assert data[length-2]["team_id"] == hero_1.team_id
    assert data[length-1]["name"] == hero_2.name
    assert data[length-1]["secret_name"] == hero_2.secret_name
    assert data[length-1]["age"] == hero_2.age
    assert data[length-1]["id"] == hero_2.id
    assert data[length-1]["team_id"] == hero_2.team_id

def test_read_teams(session: Session, client: TestClient):
    team_1 = Team(name="Team 1", headquarters="Karachi")
    team_2 = Team(name="Team 2", headquarters="Lahore")
    session.add(team_1)
    session.add(team_2)
    session.commit()

    response = client.get("/teams/")
    data = response.json()
    length = len(data)

    assert response.status_code == 200

    assert len(data) == length
    assert data[length-2]["name"] == team_1.name
    assert data[length-2]["headquarters"] == team_1.headquarters
    assert data[length-2]["id"] == team_1.id
    assert data[length-1]["name"] == team_2.name
    assert data[length-1]["headquarters"] == team_2.headquarters
    assert data[length-1]["id"] == team_2.id

def test_read_hero(session: Session, client: TestClient):
    hero_1 = Hero(name="Tariq bin Arman", secret_name="TA", age=70, team_id=1)
    session.add(hero_1)
    session.commit()

    response = client.get(f"/heroes/{hero_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == hero_1.name
    assert data["secret_name"] == hero_1.secret_name
    assert data["age"] == hero_1.age
    assert data["team_id"] == hero_1.team_id
    assert data["id"] == hero_1.id

def test_read_team(session: Session, client: TestClient):
    team_1 = Team(name="Team 1", headquarters="Karachi")
    session.add(team_1)
    session.commit()

    response = client.get(f"/teams/{team_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == team_1.name
    assert data["headquarters"] == team_1.headquarters
    assert data["id"] == team_1.id

def test_update_hero(session: Session, client: TestClient):
    hero_1 = Hero(name="Tariq bin Arman", secret_name="TA", age=70, team_id=1)
    session.add(hero_1)
    session.commit()

    response = client.patch(f"/heroes/{hero_1.id}", json={"name": "Tariq Arman"})
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Tariq Arman"
    assert data["secret_name"] == hero_1.secret_name
    assert data["age"] == hero_1.age
    assert data["team_id"] == hero_1.team_id
    assert data["id"] == hero_1.id

def test_update_team(session: Session, client: TestClient):
    team_1 = Team(name="Team 1", headquarters="Karachi")
    session.add(team_1)
    session.commit()

    response = client.patch(f"/teams/{team_1.id}", json={"headquarters": "Lahore"})
    data = response.json()

    assert response.status_code == 200
    assert data["id"] == team_1.id
    assert data["name"] == team_1.name
    assert data["headquarters"] == "Lahore"

def test_change_heroes(session: Session, client: TestClient):
    hero_1 = Hero(name="Tariq bin Arman", secret_name="TA", age=70, team_id=1)
    session.add(hero_1)
    session.commit()

    response = client.patch(f"/heroes/{hero_1.id}", json={"name": "Tariq Arman",
                                                            "secret_name": "TT",
                                                            "age": 71,
                                                            "team_id": 1})
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Tariq Arman"
    assert data["secret_name"] == "TT"
    assert data["age"] == 71
    assert data["team_id"] == 1
    assert data["id"] == hero_1.id

def test_change_teams(session: Session, client: TestClient):
    team_1 = Team(name="Team 1", headquarters="Karachi")
    session.add(team_1)
    session.commit()

    response = client.patch(f"/teams/{team_1.id}", json={"name": "Team 1",
                                                            "headquarters": "Lahore"})
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == "Team 1"
    assert data["headquarters"] == "Lahore"
    assert data["id"] == team_1.id

def test_delete_hero(session: Session, client: TestClient):
    hero_1 = Hero(name="Tariq bin Arman", secret_name="TA", age=70, team_id=1)
    session.add(hero_1)
    session.commit()

    response = client.delete(f"/heroes/{hero_1.id}")

    hero_in_db = session.get(Hero, hero_1.id)

    assert response.status_code == 200

    assert hero_in_db is None

def test_delete_team(session: Session, client: TestClient):
    team_1 = Team(name="Team 1", headquarters="Karachi")
    session.add(team_1)
    session.commit()

    response = client.delete(f"/teams/{team_1.id}")

    team_in_db = session.get(Team, team_1.id)

    assert response.status_code == 200

    assert team_in_db is None
