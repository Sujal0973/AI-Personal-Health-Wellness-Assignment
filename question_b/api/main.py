from pathlib import Path

import joblib
import pandas as pd

from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from .database import initialize_database, save_prediction, get_stats

# --------------------------------------------------
# Application setup
# --------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    initialize_database()
    yield

app = FastAPI(
    title="Heart Failure Risk Prediction API",
    lifespan=lifespan,
    description="API for predicting heart failure mortality risk.",
    version="1.0.0",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5500",
        "http://localhost:5500",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)


# --------------------------------------------------
# Load trained model
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "heart_failure_rf.joblib"

model_package = joblib.load(MODEL_PATH)

model = model_package["model"]
FEATURES = model_package["features"]
SEED = model_package["seed"]


# --------------------------------------------------
# Input schema
# --------------------------------------------------

class PatientInput(BaseModel):
    age: float = Field(..., gt=0, le=120)
    anaemia: int = Field(..., ge=0, le=1)
    creatinine_phosphokinase: float = Field(..., ge=0)
    diabetes: int = Field(..., ge=0, le=1)
    ejection_fraction: float = Field(..., ge=0, le=100)
    high_blood_pressure: int = Field(..., ge=0, le=1)
    platelets: float = Field(..., ge=0)
    serum_creatinine: float = Field(..., gt=0)
    serum_sodium: float = Field(..., ge=0)
    sex: int = Field(..., ge=0, le=1)
    smoking: int = Field(..., ge=0, le=1)


# --------------------------------------------------
# Routes
# --------------------------------------------------

@app.get("/")
def root():
    return {
        "message": "Heart Failure Risk Prediction API",
        "status": "running",
        "seed": SEED,
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "model_loaded": True,
    }


@app.post("/predict")
def predict(patient: PatientInput):

    # Convert validated input into a DataFrame
    input_data = pd.DataFrame(
        [[
            patient.age,
            patient.anaemia,
            patient.creatinine_phosphokinase,
            patient.diabetes,
            patient.ejection_fraction,
            patient.high_blood_pressure,
            patient.platelets,
            patient.serum_creatinine,
            patient.serum_sodium,
            patient.sex,
            patient.smoking,
        ]],
        columns=FEATURES,
    )

    # Get probability of positive class
    risk_probability = model.predict_proba(input_data)[0][1]

    # Default threshold from Question A
    prediction = int(risk_probability >= 0.50)

    risk_label = (
        "High Risk"
        if prediction == 1
        else "Lower Risk"
    )

    predicted_risk = round(float(risk_probability), 4)
    threshold = 0.50

    save_prediction(
        data=patient,
        predicted_risk=predicted_risk,
        prediction=prediction,
        risk_label=risk_label,
        threshold=threshold,
    )

    return {
        "prediction": prediction,
        "risk_label": risk_label,
        "predicted_risk": predicted_risk,
        "threshold": threshold,
    }

@app.get("/stats")
def stats():
    return get_stats()