from fastapi.testclient import TestClient

from question_b.api.main import app


client = TestClient(app)


VALID_PATIENT = {
    "age": 60,
    "anaemia": 1,
    "creatinine_phosphokinase": 582,
    "diabetes": 0,
    "ejection_fraction": 30,
    "high_blood_pressure": 1,
    "platelets": 263358,
    "serum_creatinine": 1.9,
    "serum_sodium": 136,
    "sex": 1,
    "smoking": 0,
}


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_predict_valid_input():
    response = client.post("/predict", json=VALID_PATIENT)

    assert response.status_code == 200

    data = response.json()

    assert "prediction" in data
    assert "risk_label" in data
    assert "predicted_risk" in data
    assert "threshold" in data

    assert data["prediction"] in [0, 1]
    assert 0 <= data["predicted_risk"] <= 1


def test_predict_invalid_input():
    invalid_patient = VALID_PATIENT.copy()

    # Invalid because age must be greater than 0
    invalid_patient["age"] = -5

    response = client.post(
        "/predict",
        json=invalid_patient,
    )

    assert response.status_code == 422