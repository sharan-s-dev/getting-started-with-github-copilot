"""
Tests for Mergington High School FastAPI application
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app, activities

client = TestClient(app)


def test_root_redirect():
    response = client.get("/", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "Gym Class" in data


def test_signup_successful():
    test_email = "new_student@mergington.edu"
    response = client.post(f"/activities/Gym%20Class/signup?email={test_email}")
    assert response.status_code == 200
    assert test_email in activities["Gym Class"]["participants"]


def test_signup_duplicate_fails():
    existing_email = "michael@mergington.edu"
    response = client.post(f"/activities/Chess%20Club/signup?email={existing_email}")
    assert response.status_code == 400
    assert response.json()["detail"] == "Student is already signed up"


def test_signup_nonexistent_activity():
    response = client.post("/activities/Unknown%20Club/signup?email=test@mergington.edu")
    assert response.status_code == 404
