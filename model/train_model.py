"""Train a tiny churn model and save it to disk.

This is intentionally minimal. The goal is "we have a trained model to serve,"
not "we trained a great model." Don't read too much into the accuracy.
"""

from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

# Keep the synthetic data reproducible so everyone trains the same model.
RNG = np.random.default_rng(42)
N = 500

# Build a small synthetic dataset: customers churn more when they're newer
# (low tenure) and lower income. We bake that signal in on purpose.
df = pd.DataFrame(
    {
        "age": RNG.integers(18, 70, size=N),
        "income": RNG.normal(60_000, 15_000, size=N).round(2),
        "tenure_months": RNG.integers(1, 72, size=N),
    }
)
churn_signal = (df["tenure_months"] < 12) | (df["income"] < 45_000)
df["churned"] = (churn_signal & (RNG.random(N) < 0.8)).astype(int)

X = df[["age", "income", "tenure_months"]]
y = df["churned"]

model = LogisticRegression(max_iter=1000)
model.fit(X, y)

# Save next to this script so the path is stable no matter where you run from.
output_path = Path(__file__).parent / "churn_model.pkl"
joblib.dump(model, output_path)

print(f"✅ Model trained and saved to {output_path}")
