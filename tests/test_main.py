"""
Simple test cases for Patient Management System API
"""

import pytest
from fastapi.testclient import TestClient
import os
import sys
import json

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src_path = os.path.join(project_root, 'src')

# Add src to Python path
if src_path not in sys.path:
    sys.path.insert(0, src_path)

try:
    from main import app
    print(f"✅ Successfully imported app from {src_path}")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print(f"Current sys.path: {sys.path}")
    print(f"Looking for main.py in: {src_path}")
    raise

client = TestClient(app)


def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Patient Management System API"}


def test_read_about():
    """Test the about endpoint"""
    response = client.get("/about")
    assert response.status_code == 200
    assert response.json() == {"message": "A fully functional API to manage your patient records"}


def test_get_all_patients():
    """Test getting all patients"""
    response = client.get("/view")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)


def test_get_patient_by_id():
    """Test getting a specific patient by ID"""
    response = client.get("/view/P001")
    assert response.status_code == 200
    data = response.json()
    assert "name" in data
    assert "bmi" in data
    assert "verdict" in data


def test_get_nonexistent_patient():
    """Test getting a patient that doesn't exist"""
    response = client.get("/view/P999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_create_patient():
    """Test creating a new patient"""
    # Use a unique ID that shouldn't exist
    unique_id = "P999"
    
    new_patient = {
        "id": unique_id,
        "name": "Test Patient",
        "city": "Test City",
        "age": 30,
        "gender": "male",
        "height": 1.75,
        "weight": 70.0
    }
    
    # First, check if patient doesn't exist
    response = client.get(f"/view/{unique_id}")
    assert response.status_code == 404, f"Patient {unique_id} should not exist before creation"
    
    # Create the patient
    response = client.post("/create", json=new_patient)
    assert response.status_code == 201, f"Expected 201, got {response.status_code}: {response.json()}"
    
    data = response.json()
    assert "created successfully" in data["message"]
    assert "patient" in data
    
    # Verify the patient was actually created
    response = client.get(f"/view/{unique_id}")
    assert response.status_code == 200, f"Patient {unique_id} should exist after creation"
    
    created_patient = response.json()
    assert created_patient["name"] == "Test Patient"
    assert created_patient["age"] == 30
    assert "bmi" in created_patient
    assert "verdict" in created_patient
    
    # Clean up - delete the test patient
    try:
        response = client.delete(f"/delete/{unique_id}")
        assert response.status_code == 200
    except Exception as e:
        print(f"Warning: Could not clean up test patient {unique_id}: {e}")


def test_sort_patients():
    """Test sorting patients"""
    response = client.get("/sort?sortby=weight&order=asc")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0


if __name__ == "__main__":
    pytest.main([__file__])
