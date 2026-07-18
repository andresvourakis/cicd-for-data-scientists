"""The tests our CI pipeline runs on every push.

They're small and fast on purpose. That's what makes them a good safety net:
they run in seconds, so there's no reason not to run them every single time.
"""

from fastapi.testclient import TestClient

from app.main import app, to_risk_band

client = TestClient(app)


def test_health_ok():
    """The /health endpoint should always respond with a simple ok."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_returns_a_valid_response():
    """A well-formed request should get a probability and a risk band back."""
    response = client.post(
        "/predict",
        json={"age": 34, "income": 38000.0, "tenure_months": 4},
    )
    assert response.status_code == 200

    body = response.json()
    assert 0.0 <= body["churn_probability"] <= 1.0
    assert body["risk_band"] in {"low", "medium", "high"}


def test_predict_rejects_bad_input():
    """Sending the wrong type should be rejected by Pydantic before our
    prediction code ever runs. FastAPI returns a 422 for us."""
    response = client.post(
        "/predict",
        json={"age": "not a number", "income": 38000.0, "tenure_months": 4},
    )
    assert response.status_code == 422


def test_risk_bands():
    """The probability-to-label mapping should hold at each band."""
    assert to_risk_band(0.1) == "low"
    assert to_risk_band(0.5) == "medium"
    assert to_risk_band(0.9) == "high"
