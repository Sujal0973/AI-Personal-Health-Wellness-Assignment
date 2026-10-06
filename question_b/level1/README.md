# Question B — Level 1

## Objective

Serve the trained heart-failure risk prediction model through a FastAPI application and provide a simple usable frontend.

## Model

The final model selected in Question A was a Random Forest classifier.

Configuration:

- Model: Random Forest
- Number of trees: 200
- Random seed: 50
- Features: 11 baseline clinical features
- Classification threshold: 0.50

The `time` feature from the original dataset was excluded because it represents follow-up duration rather than a baseline screening input.

## API

The FastAPI application provides:

### `GET /`

Confirms that the API application is running.

### `GET /health`

Returns API health information and confirms that the trained model is loaded.

### `POST /predict`

Accepts the required clinical features and returns:

- Prediction
- Risk label
- Predicted risk probability
- Classification threshold

Example response:

```json
{
  "prediction": 1,
  "risk_label": "High Risk",
  "predicted_risk": 0.51,
  "threshold": 0.5
}