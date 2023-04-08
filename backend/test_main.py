from fastapi.testclient import TestClient

from main import app


client = TestClient(app)

def test_read_main():
    response = client.get("/users/me", headers={"session_id": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoxLCJleHAiOjE2Nzc2OTc4MDd9.3DlQfz2JqJ-w2kEVdbNCWuJoSRPUpQJW87LRtBqnFU4"})
    assert response.status_code == 200
    print(response.json())