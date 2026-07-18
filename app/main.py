"""The FastAPI service that serves our churn model.

This is the same service from the FastAPI lesson. The only new thing in this
repo is the CI/CD pipeline in .github/workflows/ that runs the tests and (in a
real project) deploys this service automatically on every push.

Run it with:

    uvicorn app.main:app --reload

Then open http://localhost:8000/docs to try it out.
"""

import logging
from pathlib import Path

import joblib
from fastapi import FastAPI

from app.schemas import PredictionRequest, PredictionResponse

# Configure logging once, here, so every prediction shows up in your terminal.
logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

app = FastAPI(title="Churn Prediction Service")

# Load the model ONCE at import time, not on every request. The model ships
# pre-trained in this repo (model/churn_model.pkl) so the service and the tests
# run with no setup. Retrain it any time with: uv run model/train_model.py
MODEL_PATH = Path(__file__).parent.parent / "model" / "churn_model.pkl"
model = joblib.load(MODEL_PATH)


def to_risk_band(probability: float) -> str:
    """Turn a raw probability into a label a human can act on."""
    if probability < 0.33:
        return "low"
    if probability < 0.66:
        return "medium"
    return "high"


@app.get("/health")
def health() -> dict[str, str]:
    """Liveness check: a simple endpoint that says the service is up. This is the
    kind of thing CI (and your hosting platform) can ping to confirm a deploy
    worked."""
    return {"status": "ok"}


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest) -> PredictionResponse:
    """Predict churn probability for a single customer."""
    # The model expects features in the same order they were trained on.
    features = [[request.age, request.income, request.tenure_months]]

    # predict_proba returns [[P(stay), P(churn)]]; we want the churn column.
    probability = float(model.predict_proba(features)[0][1])
    risk_band = to_risk_band(probability)

    logger.info(
        "Prediction made | age=%s income=%s tenure_months=%s -> probability=%.3f band=%s",
        request.age,
        request.income,
        request.tenure_months,
        probability,
        risk_band,
    )

    return PredictionResponse(churn_probability=probability, risk_band=risk_band)
