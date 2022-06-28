from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_get():
    res = client.get("/")
    assert res.status_code == 200
    assert res.json() == {"message": "Welcome to your FastAPI"}
