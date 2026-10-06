# Question B — Level 3: Robustness and Concurrency

## Seed

50

## Objective

The Level 3 task is to deliberately break the application in two ways,
observe the failure, fix each problem, and reason about how the application
could safely support approximately 100 users at once.

The experiments are based on the predictions committed before testing.

---

## Break/Fix Experiment 1 — Missing Model File

### Prediction

I predicted that making the trained model file unavailable would prevent
the FastAPI application from starting because the model is loaded when
`main.py` is imported.

### Failure Introduced

The trained model file was temporarily renamed:

```text
question_b/api/model/heart_failure_rf.joblib

---

## Break/Fix Experiment 2 — Invalid Input

### Prediction

I predicted that sending text instead of a numeric value for a patient input
such as `age` would be rejected by FastAPI/Pydantic before the request
reached the model or database.

I expected the API to return HTTP 422.

### Failure Introduced

A prediction request was deliberately sent with:

```json
{
  "age": "not-a-number"
}

## Experiment 3 — Approximately 100 Concurrent Users

### Test Setup

The FastAPI application was running locally at:

`http://127.0.0.1:8000`

I sent 100 concurrent POST requests to `/predict` using
`question_b/level3/concurrency_test.py`.

The requests used valid patient inputs and were sent using a
ThreadPoolExecutor with 100 workers.

### Prediction

Before running the experiment, I predicted that the application would
handle the concurrent requests without producing incorrect prediction
responses. I also predicted that PostgreSQL would store the successful
requests and that database connections could become the main bottleneck
under higher concurrency.

### Actual Result

| Metric | Result |
|---|---:|
| Requests sent | 100 |
| Successful requests | 100 |
| Failed requests | 0 |
| Total time | 3.924 seconds |
| Fastest request | 1.515 seconds |
| Slowest request | 3.789 seconds |
| Average response time | 2.715 seconds |

All 100 requests returned successfully.

### Database Verification

Before the concurrency experiment, the `predictions` table contained
5 records.

After the experiment, the `/stats` endpoint reported:

- Total requests: 105
- Average predicted risk: 0.084
- High-risk share: 0.0286

Therefore, the database count increased by exactly 100 records:

`105 - 5 = 100`

This confirms that all 100 successful prediction requests were also
persisted in PostgreSQL.

### Prediction vs Actual Result

My prediction was correct.

I expected all approximately 100 concurrent requests to be handled
successfully and expected the successful requests to be stored in the
database. The experiment produced 100 successful responses, 0 failed
responses, and 100 additional database records.

### How I Would Make the Application Safer for 100 Users at Once

The test shows that the current local implementation successfully
handled 100 concurrent requests. However, the database layer currently
opens a database connection for each database operation.

For a production deployment, I would use a bounded PostgreSQL connection
pool so that a large number of simultaneous requests do not create an
uncontrolled number of database connections. I would also add connection
timeouts, request logging, monitoring, and run the API behind a
production ASGI server with multiple workers.

The concurrency result should therefore be interpreted as a successful
local robustness test rather than a guarantee of production-scale
performance.