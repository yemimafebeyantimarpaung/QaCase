import pytest
import requests
import os

BASE_URL = "https://api.wemine.com"
REPORTER_TOKEN = "Bearer reporter-token"
PIC_TOKEN = "Bearer pic-token"
REPORTER_USER_ID = "user-001"


# ------------------------------------------
# BATCH 1: LOGIN & TENANT TESTS
# ------------------------------------------

def test_login_success():
    payload = {"username": "valid_miner_user@wemine.com"}
    response = requests.post(f"{BASE_URL}/user/who", json=payload)
    
    assert response.status_code == 200
    assert response.json()["tenantId"] is not None


def test_login_invalid_user():
    payload = {"username": "ghost_user_999@wemine.com"}
    response = requests.post(f"{BASE_URL}/user/who", json=payload)
    
    assert response.status_code == 404


# ------------------------------------------
# BATCH 2: INSPECTION FORM TESTS
# ------------------------------------------

def test_get_form_schema():
    headers = {"Authorization": "Bearer admin-token"}
    response = requests.get(f"{BASE_URL}/form/schema/EQUIPMENT_INSPECTION_50", headers=headers)
    
    assert response.status_code == 200
    assert len(response.json()["fields"]) == 50


def test_radio_limit_options():
    headers = {"Authorization": "Bearer admin-token"}
    payload = {
        "fieldType": "RADIO",
        "options": ["Opt 1", "Opt 2", "Opt 3", "Opt 4", "Opt 5"]
    }
    response = requests.post(f"{BASE_URL}/form/builder/field", json=payload, headers=headers)
    
    assert response.status_code == 400


# ------------------------------------------
# BATCH 3: SAFETY HAZARD & WORKFLOW TESTS
# ------------------------------------------

def test_submit_hazard():
    data = {
        "location": "LOC-001",
        "sublocation": "SUBLOC-A",
        "area": "AREA-12",
        "pic": REPORTER_USER_ID
    }
    files = {"evidence": open("tests/resources/evidence.jpg", "rb")}
    headers = {"Authorization": REPORTER_TOKEN}
    
    response = requests.post(f"{BASE_URL}/safety/hazard", data=data, files=files, headers=headers)
    
    assert response.status_code == 201
    assert response.json()["hazardId"] is not None


def test_submit_hazard_no_evidence():
    data = {
        "location": "LOC-001",
        "sublocation": "SUBLOC-A",
        "area": "AREA-12",
        "pic": REPORTER_USER_ID
    }
    headers = {"Authorization": REPORTER_TOKEN}
    
    response = requests.post(f"{BASE_URL}/safety/hazard", data=data, headers=headers)
    
    assert response.status_code == 400


def test_pic_resolve_task():
    # Step 1: Create a hazard report to get the task ID
    data_initial = {
        "location": "LOC-001",
        "sublocation": "SUBLOC-A",
        "area": "AREA-12",
        "pic": REPORTER_USER_ID
    }
    files_initial = {"evidence": open("tests/resources/evidence.jpg", "rb")}
    resp_initial = requests.post(
        f"{BASE_URL}/safety/hazard", 
        data=data_initial, 
        files=files_initial, 
        headers={"Authorization": REPORTER_TOKEN}
    )
    task_id = resp_initial.json()["followupTaskId"]
    
    # Step 2: PIC resolves the task
    data_resolve = {"resolutionDate": "2026-10-29T10:00:00"}
    files_resolve = {"evidence": open("tests/resources/resolved.jpg", "rb")}
    
    resp_resolve = requests.post(
        f"{BASE_URL}/safety/hazard/followup/{task_id}",
        data=data_resolve,
        files=files_resolve,
        headers={"Authorization": PIC_TOKEN}
    )
    
    assert resp_resolve.status_code == 200
    assert resp_resolve.json()["status"] == "resolved"