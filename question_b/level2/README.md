# Question B — Level 2: Database Persistence, Hand-Written SQL & Automated Testing

## 1. Objective

Implement database persistence for all incoming prediction requests and model results, expose an aggregation endpoint (`/stats`) computed strictly via **hand-written SQL without an ORM**, implement comprehensive input boundary validation with explicit error responses, and build an automated test suite with **pytest** covering valid, invalid, and health endpoints.

---

## 2. Relational Database Schema & Persistence

All prediction transactions are persisted in a relational database (`health_wellness`).

### DDL Table Definition (`predictions`):
```sql
CREATE TABLE IF NOT EXISTS predictions (
    id SERIAL PRIMARY KEY,
    age DOUBLE PRECISION NOT NULL,
    anaemia INTEGER NOT NULL,
    creatinine_phosphokinase DOUBLE PRECISION NOT NULL,
    diabetes INTEGER NOT NULL,
    ejection_fraction DOUBLE PRECISION NOT NULL,
    high_blood_pressure INTEGER NOT NULL,
    platelets DOUBLE PRECISION NOT NULL,
    serum_creatinine DOUBLE PRECISION NOT NULL,
    serum_sodium DOUBLE PRECISION NOT NULL,
    sex INTEGER NOT NULL,
    smoking INTEGER NOT NULL,
    predicted_risk DOUBLE PRECISION NOT NULL,
    prediction INTEGER NOT NULL,
    risk_label VARCHAR(20) NOT NULL,
    threshold DOUBLE PRECISION NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Parameterized SQL Insert (Zero ORM & SQL Injection Prevention):
```python
insert_sql = """
INSERT INTO predictions (
    age, anaemia, creatinine_phosphokinase, diabetes, ejection_fraction,
    high_blood_pressure, platelets, serum_creatinine, serum_sodium,
    sex, smoking, predicted_risk, prediction, risk_label, threshold
)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
"""
cursor.execute(insert_sql, values)
```
*Security note:* Inputs are passed as parameterized tuples (`%s`), strictly preventing SQL injection vulnerabilities.

---

## 3. Hand-Written Aggregation Query (`GET /stats`)

The `/stats` endpoint computes system-wide telemetry directly inside the database engine without loading rows into Python memory or using ORMs:

```sql
SELECT
    COUNT(*) AS total_requests,
    COALESCE(AVG(predicted_risk), 0) AS average_predicted_risk,
    COALESCE(
        AVG(
            CASE
                WHEN prediction = 1 THEN 1.0
                ELSE 0.0
            END
        ),
        0
    ) AS high_risk_share
FROM predictions;
```

### Verified API Response:
```json
{
  "total_requests": 105,
  "average_predicted_risk": 0.084,
  "high_risk_share": 0.0286
}
```

---

## 4. Input Validation & Error Handling

Input validation is enforced at the API boundary using **Pydantic** (`BaseModel`):

| Feature | Data Type | Validation Rules | Clinical Rationale / Error Behavior |
|---|:---:|:---:|---|
| `age` | `float` | `0 < age <= 120` | Rejects non-positive or biologically impossible ages |
| `anaemia` | `int` | `0 <= anaemia <= 1` | Strictly binary flag (0 or 1) |
| `creatinine_phosphokinase` | `float` | `cpk >= 0` | Enzyme level cannot be negative |
| `diabetes` | `int` | `0 <= diabetes <= 1` | Strictly binary flag (0 or 1) |
| `ejection_fraction` | `float` | `0 <= ef <= 100` | Percentage of pumped blood must be within 0–100% |
| `high_blood_pressure` | `int` | `0 <= hbp <= 1` | Strictly binary flag (0 or 1) |
| `platelets` | `float` | `platelets >= 0` | Cell count cannot be negative |
| `serum_creatinine` | `float` | `cr > 0` | Blood level must be positive |
| `serum_sodium` | `float` | `na >= 0` | Electrolyte concentration must be non-negative |
| `sex` | `int` | `0 <= sex <= 1` | Strictly binary (0 or 1) |
| `smoking` | `int` | `0 <= smoking <= 1` | Strictly binary flag (0 or 1) |

Any payload violating these rules is immediately halted by FastAPI with `HTTP 422 Unprocessable Entity` containing an explicit error location and description before touching the ML model or database.

---

## 5. Automated Test Suite (`pytest`)

Automated tests are implemented in `question_b/tests/test_api.py` using FastAPI's `TestClient`:

1. **`test_health_endpoint`**:
   - Asserts that `GET /health` returns `HTTP 200` with `status == "healthy"` and `model_loaded == True`.
2. **`test_predict_valid_input`**:
   - Sends a physiologically valid patient dictionary.
   - Asserts `HTTP 200`, verifies response schema contains `prediction`, `risk_label`, `predicted_risk`, `threshold`, and ensures predicted risk is bounded within `[0.0, 1.0]`.
3. **`test_predict_invalid_input`**:
   - Sends invalid patient data (`age: -5`).
   - Asserts that the API returns `HTTP 422 Unprocessable Entity`, confirming that invalid patient records are rejected.

---

## 6. How to Run the Tests

Execute from the project root:
```bash
python -m pytest question_b/tests -v
```
All 3 automated tests execute successfully; runtime depends on the local environment.
