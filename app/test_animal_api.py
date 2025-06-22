import pytest
from fastapi.testclient import TestClient
from animal_api import app, ANIMALS, PAGE_SIZE

client = TestClient(app)

def test_get_animals_first_page():
    response = client.get("/animals/v1/animals?page=1")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert "page" in data
    assert "total_pages" in data
    assert isinstance(data["items"], list)
    assert data["page"] == 1
    assert len(data["items"]) <= PAGE_SIZE

def test_get_animal_by_id():
    animal_id = 0
    response = client.get(f"/animals/v1/animals/{animal_id}")
    assert response.status_code == 200
    animal = response.json()
    assert "id" in animal
    assert "name" in animal
    assert "friends" in animal
    assert isinstance(animal["friends"], list)
    # born_at can be None or ISO8601 string
    assert "born_at" in animal

def test_post_animals_home_success():
    animals = [
        {
            "id": 9999,
            "name": "TestAnimal",
            "born_at": "2020-01-01T12:00:00",
            "friends": ["Lion", "Bear"]
        }
        for _ in range(5)
    ]
    response = client.post("/animals/v1/home", json=animals)
    assert response.status_code == 200
    assert response.json()["message"] == "Helped 5 find home"

def test_post_animals_home_too_many():
    animals = [
        {
            "id": 10000 + i,
            "name": "TestAnimal",
            "born_at": "2020-01-01T12:00:00",
            "friends": ["Lion", "Bear"]
        }
        for i in range(101)
    ]
    response = client.post("/animals/v1/home", json=animals)
    assert response.status_code == 400
    assert "only 100 animals" in response.json()["detail"]

def test_index():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == "Hello!" or response.text == '"Hello!"' 