# Question B — Level 3 Predictions

## Seed

50

## Purpose

These predictions are written before running the required Level 3 robustness
experiments. The results will be compared with these predictions after the
tests are completed.

## Prediction 1 — Missing Model File

**Failure introduced:** Temporarily make the trained model file unavailable
to the FastAPI application.

**Prediction:** I expect the application to fail during startup or model
loading because the `/predict` endpoint depends on the saved Random Forest
model. I expect prediction requests to be unavailable until the missing
model file is restored.

**Expected fix:** Restore the model file to the expected path and restart
the FastAPI application. I expect the `/health` and `/predict` endpoints to
work again after the model is loaded successfully.

## Prediction 2 — Invalid Data Type

**Failure introduced:** Send text instead of a numeric value for one of the
patient inputs, such as `age`.

**Prediction:** I expect FastAPI/Pydantic validation to reject the request
before it reaches the model or database. I expect an HTTP 422 validation
response rather than a prediction being generated or invalid data being
stored.

**Expected fix:** No code change should be required because backend input
validation is already part of the application. The invalid request should
be corrected by sending a valid numeric value.

## Prediction 3 — Approximately 100 Concurrent Users

**Test:** Send approximately 100 prediction requests concurrently to the
`/predict` endpoint using valid patient inputs.

**Prediction:** I expect the application to handle the concurrent requests
without producing incorrect prediction responses. I expect PostgreSQL to
store the requests correctly and the final request count to increase by the
number of successful requests.

I expect the main potential bottleneck to be database connections because
the current implementation opens a database connection for each database
operation. If the baseline test shows connection or throughput problems, I
expect connection management to be the main area requiring improvement.

## What I Will Compare After Testing

For each experiment I will record:

- What actually happened.
- Whether the result matched my prediction.
- The error or failure observed, if any.
- The fix applied.
- The result after the fix.
- For the concurrent test, the number of successful and failed requests
  and the final database request count.