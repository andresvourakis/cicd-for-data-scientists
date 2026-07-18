"""Pydantic models that define the shape of our request and response.

FastAPI uses these to validate incoming data and to auto-generate the docs.
If someone sends the wrong types, FastAPI rejects the request before your
prediction code ever runs.
"""

from pydantic import BaseModel


class PredictionRequest(BaseModel):
    """The customer features we need to make a churn prediction."""

    age: int
    income: float
    tenure_months: int


class PredictionResponse(BaseModel):
    """What we send back: a probability and a human-friendly risk band."""

    churn_probability: float
    risk_band: str
