import pytest
from app import app
from database import init_db


@pytest.fixture()
def client(tmp_path, monkeypatch):
    import database
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    init_db()
    app.config.update(TESTING=True, SECRET_KEY="test")
    with app.test_client() as test_client:
        yield test_client


def test_home_loads(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Voyage Beyond" in response.data


def test_explorer_search(client):
    response = client.get("/explorer?q=Jupiter")
    assert response.status_code == 200
    assert b"Jupiter" in response.data
    assert b"Mercury" not in response.data


def test_analytics_loads(client):
    response = client.get("/analytics")
    assert response.status_code == 200
    assert b"Diameter ranking" in response.data


def test_quiz_saves_attempt(client):
    response = client.post("/quiz", data={
        "player_name": "Test Explorer",
        "q0": "Jupiter",
        "q1": "Mercury",
        "q2": "Saturn",
        "q3": "Dwarf planet",
        "q4": "Earth",
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b"5/5" in response.data
    import database
    with database.get_connection() as connection:
        row = connection.execute("SELECT player_name, score FROM quiz_attempts").fetchone()
    assert row["player_name"] == "Test Explorer"
    assert row["score"] == 5


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json["status"] == "ok"
