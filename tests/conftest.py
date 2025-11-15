"""Pytest configuration and fixtures"""
import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities data before each test"""
    # Store original state
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball practice and games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 6:00 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu", "lucas@mergington.edu"]
        },
        "Swimming Club": {
            "description": "Swimming lessons and competitive training",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 20,
            "participants": ["sarah@mergington.edu", "mia@mergington.edu"]
        },
        "Art Studio": {
            "description": "Explore painting, drawing, and mixed media",
            "schedule": "Thursdays, 3:00 PM - 5:00 PM",
            "max_participants": 15,
            "participants": ["emily@mergington.edu", "ava@mergington.edu"]
        },
        "Drama Club": {
            "description": "Acting, stage performance, and theater production",
            "schedule": "Wednesdays, 3:30 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["noah@mergington.edu", "isabella@mergington.edu"]
        },
        "Debate Team": {
            "description": "Develop argumentation and public speaking skills",
            "schedule": "Mondays, 4:00 PM - 5:30 PM",
            "max_participants": 16,
            "participants": ["william@mergington.edu", "charlotte@mergington.edu"]
        },
        "Science Olympiad": {
            "description": "Compete in science and engineering challenges",
            "schedule": "Fridays, 3:00 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["benjamin@mergington.edu", "amelia@mergington.edu"]
        }
    }
    
    # Reset to original state
    activities.clear()
    activities.update(original_activities)
    
    yield
    
    # Clean up after test
    activities.clear()
    activities.update(original_activities)
