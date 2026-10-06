# Question B — Level 2

## Objective

Persist prediction requests in a relational database, expose aggregate statistics through an API endpoint, validate inputs, and test the application.

## Database

PostgreSQL was selected as the database.

Database:

`health_wellness`

Table:

`predictions`

The table stores:

- Patient feature values
- Predicted risk
- Prediction
- Risk label
- Classification threshold
- Creation timestamp

## Persistence

Every successful `/predict` request is stored in PostgreSQL.

The database password is supplied through the `DB_PASSWORD` environment variable and is not hardcoded in the application.

## SQL

Database operations use hand-written SQL rather than an ORM.

Prediction records are inserted using parameterized SQL values rather than constructing SQL statements from user input.

This reduces the risk of SQL injection.

## `/stats`

A `GET /stats` endpoint calculates:

- Total prediction requests
- Average predicted risk
- Share of high-risk predictions

The statistics are calculated directly from the PostgreSQL `predictions` table.

## Verified Result

After two prediction requests, `/stats` returned:

```json
{
  "total_requests": 2,
  "average_predicted_risk": 0.29,
  "high_risk_share": 0.5
}