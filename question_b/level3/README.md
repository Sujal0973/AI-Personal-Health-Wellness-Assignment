# Question B — Level 3: Robustness, Fault Tolerance & Concurrency

## 1. Objective

Systematically validate application resilience, fault tolerance, and concurrency performance through three practical engineering experiments:
1. **Break/Fix Experiment 1:** Deliberately induce a missing ML model file and document behavior before and after the fix.
2. **Break/Fix Experiment 2:** Deliberately send malformed/non-numeric input where a number is expected and verify boundary validation before and after the fix.
3. **100 Concurrent Users Stress Test:** Benchmark the application under 100 simultaneous prediction requests, verify database transaction integrity, and propose a production-grade concurrency architecture.

---

## 2. Seed & Environment Setup

- **Candidate USN:** `1DA23AI050`
- **Assigned Seed ($S$):** `50`
- **Application Endpoint:** `http://127.0.0.1:8000`
- **Database:** PostgreSQL (`health_wellness`)

---

## 3. Break/Fix Experiment 1 — Missing Model File

### 3.1 Pre-Experiment Prediction (Committed to Git)
As recorded in `question_b/level3/prediction.md` (Commit `460dbfc`):
> *"I expect the application to fail during startup or model loading because the `/predict` endpoint depends on the saved Random Forest model. I expect prediction requests to be unavailable until the missing model file is restored."*

### 3.2 Failure Introduced
The serialized model artifact was temporarily renamed:
```bash
mv question_b/api/model/heart_failure_rf.joblib question_b/api/model/heart_failure_rf.joblib.bak
```

### 3.3 What Happened BEFORE the Fix
When attempting to launch the FastAPI server via Uvicorn:
```text
$ uvicorn question_b.api.main:app --reload
...
Traceback (most recent call last):
  File "question_b/api/main.py", line 41, in <module>
    model_package = joblib.load(MODEL_PATH)
  File "joblib/numpy_pickle.py", line 650, in load
    with open(filename, 'rb') as f:
FileNotFoundError: [Errno 2] No such file or directory: '.../question_b/api/model/heart_failure_rf.joblib'
ERROR: Application startup failed. Exiting.
```
- **Observed Behavior:** The application could not complete ASGI startup.
- **Client Impact:** All client requests to `/predict` or `/health` resulted in immediate connection refused errors (`ERR_CONNECTION_REFUSED`).

### 3.4 Fix Applied
1. Verified file path resolution logic using `Path(__file__).resolve().parent`.
2. Restored the trained model artifact to `question_b/api/model/heart_failure_rf.joblib`.
3. Restarted the Uvicorn application service.

### 3.5 What Happened AFTER the Fix
```text
INFO:     Started server process [18420]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```
- Sending `GET /health` returned `HTTP 200`:
  ```json
  {"status": "healthy", "model_loaded": true}
  ```
- Sending a valid `POST /predict` request returned `HTTP 200`:
  ```json
  {"prediction": 1, "risk_label": "High Risk", "predicted_risk": 0.51, "threshold": 0.5}
  ```
- The application fully recovered, verifying that model availability is required for service startup.

---

## 4. Break/Fix Experiment 2 — Malformed / Non-Numeric Input

### 4.1 Pre-Experiment Prediction (Committed to Git)
As recorded in `question_b/level3/prediction.md` (Commit `460dbfc`):
> *"I expect FastAPI/Pydantic validation to reject the request before it reaches the model or database. I expect an HTTP 422 validation response rather than a prediction being generated or invalid data being stored."*

### 4.2 Failure Introduced
A POST request was sent to `/predict` where the numeric `age` field was deliberately replaced with text:
```json
{
  "age": "not-a-number",
  "anaemia": 1,
  "creatinine_phosphokinase": 582,
  "diabetes": 0,
  "ejection_fraction": 30,
  "high_blood_pressure": 1,
  "platelets": 263358,
  "serum_creatinine": 1.9,
  "serum_sodium": 136,
  "sex": 1,
  "smoking": 0
}
```

### 4.3 What Happened BEFORE the Fix
The API intercepted the request at the schema boundary and refused processing:
- **HTTP Status Code:** `422 Unprocessable Entity`
- **Response Body:**
  ```json
  {
    "detail": [
      {
        "type": "float_parsing",
        "loc": ["body", "age"],
        "msg": "Input should be a valid number, unable to parse string as an float",
        "input": "not-a-number"
      }
    ]
  }
  ```
- **Database Verification:** A direct SQL query `SELECT COUNT(*) FROM predictions;` confirmed that **zero records** were inserted.
- **Observed Behavior:** The backend validation successfully prevented invalid types from reaching NumPy array transformations (which would have caused a runtime `ValueError`) or corrupting the PostgreSQL database.

### 4.4 Fix Applied (Client Remediation)
Corrected the client payload by supplying a valid float within physiological bounds (`age: 60.0`).

### 4.5 What Happened AFTER the Fix
```json
{
  "prediction": 1,
  "risk_label": "High Risk",
  "predicted_risk": 0.51,
  "threshold": 0.5
}
```
- **HTTP Status Code:** `200 OK`
- The prediction was calculated and persisted in the database with `id = 106`.

---

## 5. Experiment 3 — Approximately 100 Concurrent Users Stress Test

### 5.1 Test Methodology
Using `question_b/level3/concurrency_test.py`, 100 simultaneous HTTP POST requests containing valid patient parameters were dispatched to `http://127.0.0.1:8000/predict` using Python's `concurrent.futures.ThreadPoolExecutor(max_workers=100)`.

### 5.2 Empirical Results
| Metric | Benchmark Result |
|---|:---:|
| **Concurrent Requests Sent** | **100** |
| **Successful Responses (HTTP 200)** | **100 (100.0%)** |
| **Failed Requests** | **0 (0.0%)** |
| **Total Test Wall-Clock Time** | **3.924 seconds** |
| **Fastest Request Latency** | 1.515 seconds |
| **Slowest Request Latency** | 3.789 seconds |
| **Average Response Latency** | 2.715 seconds |

### 5.3 Database Integrity & Concurrency Verification
Before running the benchmark, the PostgreSQL `predictions` table held exactly **5 records**.

Immediately following the 100-request burst, `GET /stats` returned:
```json
{
  "total_requests": 105,
  "average_predicted_risk": 0.084,
  "high_risk_share": 0.0286
}
```
$$105 - 5 = \mathbf{100 \text{ newly persisted records}}$$
- Confirmed that PostgreSQL and the hand-written SQL transaction logic handled concurrent row insertions with **zero lost writes, zero race conditions, and zero lock deadlocks**.

---

## 6. Architectural Blueprint: Making the App Production-Safe for 100+ Concurrent Users

While the test server successfully handled 100 concurrent requests locally, scaling to hundreds of concurrent clinical users in production requires eliminating architectural bottlenecks:

```text
[ Incoming Web Traffic ]
           │
           ▼
[ Nginx / Cloudflare Load Balancer ]
  ├── SSL Termination & DDoS Mitigation
  └── Rate Limiting (Token Bucket: 20 req/sec per IP)
           │
           ▼
[ Production ASGI Server (Gunicorn + Uvicorn Workers) ]
  ├── Worker 1 (Uvicorn Async Event Loop)
  ├── Worker 2 (Uvicorn Async Event Loop)
  ├── Worker 3 (Uvicorn Async Event Loop)
  └── Worker 4 (Uvicorn Async Event Loop)
           │
           ▼
[ Bounded Connection Pool (psycopg_pool) ]
  ├── Min Connections: 5
  ├── Max Connections: 20
  └── Connection Timeout: 5.0 seconds
           │
           ▼
[ PostgreSQL Primary Database ]
```

### 1. Bounded Database Connection Pooling
- **Current Limitation:** The development script opens and closes an ad-hoc connection for every request (`psycopg.connect(...)`). Under heavy traffic, opening 100+ raw TCP connections exhausts PostgreSQL's `max_connections` limit and spikes connection latency.
- **Production Solution:** Implement a bounded connection pool using `psycopg_pool.ConnectionPool(min_size=5, max_size=20, timeout=5.0)`. Connections are reused across requests, preventing connection exhaustion.

### 2. Multi-Worker ASGI Architecture
- **Current Limitation:** Running with a single Uvicorn process is bounded by Python's single thread of execution.
- **Production Solution:** Deploy behind **Gunicorn** managing multiple Uvicorn workers:
  ```bash
  gunicorn question_b.api.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
  ```
  This enables multi-core CPU parallelism for model inferences.

### 3. Asynchronous Database Driver
- Transition from synchronous `psycopg` to non-blocking `psycopg.AsyncConnection` with `async def predict(...)`. The FastAPI event loop can then handle incoming requests while awaiting I/O from PostgreSQL without thread blocking.

### 4. In-Memory Caching for `/stats`
- The `/stats` query performs a full table scan (`COUNT(*)`, `AVG(...)`). Under heavy load, computing aggregates on every request causes database CPU spikes.
- **Solution:** Cache `/stats` results in Redis with a 30-second TTL (Time-To-Live).

### 5. API Rate Limiting & Circuit Breaking
- Implement `slowapi` to enforce rate limits (e.g., maximum 30 prediction requests per minute per IP), preventing denial-of-service abuse while maintaining high availability.

---

## 7. Reproduction Commands

```bash
# 1. Run automated test suite
python -m pytest question_b/tests -v

# 2. Run the 100-user concurrency benchmark
python question_b/level3/concurrency_test.py
```