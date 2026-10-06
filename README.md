# AI for Personal Health and Wellness

Technical Assignment for B.E. AI & ML

## Candidate Information

- USN: 1DA23AI050
- Seed: 50
- Questions: A and B

## Question A

Predict a health risk using the Heart Failure Clinical Records dataset.

### Question A Structure

- Level 1: Logistic Regression and Random Forest baseline models.
- Level 2: NumPy Logistic Regression implemented from scratch and comparison with the sklearn model.
- Level 3: Prediction and testing of the effect of lowering the classification threshold on recall and precision.

## Question B

Turn the trained health-risk model into a usable application through an API and frontend.

### Question B Structure

- Level 1: FastAPI prediction endpoint and simple frontend.
- Level 2: PostgreSQL persistence, `/stats` endpoint using hand-written SQL, input validation, and pytest tests.
- Level 3: Break/fix experiments and approximately 100 concurrent prediction requests.

## Dataset

UCI Heart Failure Clinical Records Dataset.

The `time` column is excluded from the prediction features because it represents follow-up duration rather than a baseline patient input.

## Important

All train/test splits and model randomness use seed 50.

## Question B — PostgreSQL Setup

Question B uses PostgreSQL to store prediction requests and results.

### 1. Create the database

Create a PostgreSQL database named:

```text
health_wellness