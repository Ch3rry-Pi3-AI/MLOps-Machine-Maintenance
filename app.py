"""
app.py
======
Flask web application for **Smart Manufacturing — Efficiency Prediction**.

Overview
--------
Serves a simple, user-friendly UI that accepts machine context and telemetry
inputs, scales them using a previously-fitted `StandardScaler`, and performs a
classification with a trained model. The result is rendered on the homepage.

Key Artefacts
-------------
- Trained model ............ artifacts/models/model.pkl
- Fitted scaler ............ artifacts/processed/scaler.pkl
- (Optional) feature means . artifacts/processed/feature_means.json

Notes
-----
- The feature **order** must match the order used in training.
- `Operation_Mode` is label-encoded via `OPERATION_MODE_MAP`. Ensure this map
  matches what was used during preprocessing/training (or load the persisted
  encoder/mapping instead).
- Defaults are drawn from `feature_means.json` when present; otherwise sensible
  fallbacks are used (see `DEFAULTS_FALLBACK`).
"""

from __future__ import annotations

import json
import os
from datetime import datetime
from typing import Dict, List, Any

import joblib
import numpy as np
from flask import Flask, render_template, request

# ---------------------------------------------------------------------
# Flask application
# ---------------------------------------------------------------------
app = Flask(__name__)

# ---------------------------------------------------------------------
# Paths to artefacts
# ---------------------------------------------------------------------
MODEL_PATH: str = "artifacts/models/model.pkl"
SCALER_PATH: str = "artifacts/processed/scaler.pkl"
MEANS_PATH: str = "artifacts/processed/feature_means.json"  # optional

# ---------------------------------------------------------------------
# Load artefacts (model + scaler)
# ---------------------------------------------------------------------
model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)

# ---------------------------------------------------------------------
# Feature schema (order must match training)
# ---------------------------------------------------------------------
FEATURES: List[str] = [
    "Operation_Mode",
    "Temperature_C",
    "Vibration_Hz",
    "Power_Consumption_kW",
    "Network_Latency_ms",
    "Packet_Loss_%",
    "Quality_Control_Defect_Rate_%",
    "Production_Speed_units_per_hr",
    "Predictive_Maintenance_Score",
    "Error_Rate_%",
    "Year",
    "Month",
    "Day",
    "Hour",
]

# ---------------------------------------------------------------------
# Label mapping (model output → human-readable class)
# Adjust if training used different class indices.
# ---------------------------------------------------------------------
LABELS: Dict[int, str] = {
    0: "High",
    1: "Low",
    2: "Medium",
}

# ---------------------------------------------------------------------
# Operation mode encoding used during training
# If you persisted encoders/mappings, load them. Otherwise, ensure this map
# matches the one logged/used in preprocessing.
# Example previously observed: {'Idle': 0, 'Active': 1, 'Maintenance': 2}
# ---------------------------------------------------------------------
OPERATION_MODE_MAP: Dict[str, int] = {
    "Idle": 0,
    "Active": 1,
    "Maintenance": 2,
}
OPERATION_MODE_CHOICES: List[str] = list(OPERATION_MODE_MAP.keys())

# ---------------------------------------------------------------------
# Sensible default values (fallback when means file not present)
# ---------------------------------------------------------------------
_now = datetime.now()
DEFAULTS_FALLBACK: Dict[str, Any] = {
    "Operation_Mode": "Active",            # UI label; mapped via OPERATION_MODE_MAP
    "Temperature_C": 65.0,                 # typical operating temperature
    "Vibration_Hz": 50.0,                  # nominal frequency
    "Power_Consumption_kW": 35.0,          # mid-load power
    "Network_Latency_ms": 15.0,            # LAN-ish latency
    "Packet_Loss_%": 0.5,
    "Quality_Control_Defect_Rate_%": 1.0,
    "Production_Speed_units_per_hr": 120.0,
    "Predictive_Maintenance_Score": 55.0,  # 0–100 health score
    "Error_Rate_%": 0.8,
    "Year": _now.year,
    "Month": _now.month,
    "Day": _now.day,
    "Hour": min(_now.hour, 23),
}


def load_feature_means() -> Dict[str, Any]:
    """
    Load per-feature mean defaults if available; otherwise return sensible fallbacks.

    Returns
    -------
    dict
        A dict of {feature_name: default_value} suitable for pre-filling the form.
        The UI-friendly defaults for `Operation_Mode` and date parts are retained.
    """
    if os.path.exists(MEANS_PATH):
        try:
            with open(MEANS_PATH, "r", encoding="utf-8") as f:
                means = json.load(f)

            # Merge into fallbacks to keep non-numeric UI defaults intact
            merged = DEFAULTS_FALLBACK.copy()
            for k, v in means.items():
                if k in merged and isinstance(v, (int, float)):
                    merged[k] = v
            return merged
        except Exception:
            # Silently fall back to baked-in defaults if means file is malformed
            return DEFAULTS_FALLBACK
    return DEFAULTS_FALLBACK


# ---------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Render the main form and (when POSTed) return the model's prediction.

    Workflow
    --------
    1) Build an input vector in the exact `FEATURES` order.
    2) Map `Operation_Mode` (UI label) → encoded integer used during training.
    3) Scale features with the fitted StandardScaler.
    4) Predict with the trained model and map to a human-readable label.

    Returns
    -------
    Flask Response
        Rendered HTML template with optional `prediction`.
    """
    prediction = None
    form_values = load_feature_means()

    if request.method == "POST":
        try:
            values: List[float] = []

            # Build input vector in strict training order
            for feat in FEATURES:
                if feat == "Operation_Mode":
                    # Map UI label → encoder code
                    mode_label = request.form.get("Operation_Mode", OPERATION_MODE_CHOICES[0])
                    mode_code = OPERATION_MODE_MAP.get(mode_label)
                    if mode_code is None:
                        raise ValueError(f"Unknown Operation_Mode '{mode_label}'.")
                    values.append(float(mode_code))
                    form_values["Operation_Mode"] = mode_label
                else:
                    # Pull numeric value (fall back to default) and coerce to float
                    raw_val = request.form.get(feat, str(DEFAULTS_FALLBACK.get(feat, 0.0)))
                    val = float(raw_val)
                    values.append(val)
                    form_values[feat] = val

            # Shape → scale → predict
            input_array = np.array(values, dtype=float).reshape(1, -1)
            scaled_array = scaler.transform(input_array)
            pred_idx = int(model.predict(scaled_array)[0])
            prediction = LABELS.get(pred_idx, f"Unknown ({pred_idx})")

        except Exception as e:
            # Surface error to UI for quick feedback; production apps should log instead
            prediction = f"Error: {e}"

    return render_template(
        "index.html",
        prediction=prediction,
        features=FEATURES,
        defaults=form_values,
        op_modes=OPERATION_MODE_CHOICES,
    )


# ---------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------
if __name__ == "__main__":
    # Debug server for local development
    app.run(debug=True, host="0.0.0.0", port=5000)
