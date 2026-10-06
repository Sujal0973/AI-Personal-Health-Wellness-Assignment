import os

import psycopg


# PostgreSQL connection settings
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "health_wellness")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD")


def get_connection():
    """Create a connection to the PostgreSQL database."""
    if not DB_PASSWORD:
        raise RuntimeError(
            "DB_PASSWORD environment variable is not set."
        )

    return psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
    )


def initialize_database():
    """Create the predictions table if it does not already exist."""

    create_table_sql = """
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
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(create_table_sql)

        connection.commit()


def save_prediction(data, predicted_risk, prediction, risk_label, threshold):
    """Save a prediction request and its result."""

    insert_sql = """
    INSERT INTO predictions (
        age,
        anaemia,
        creatinine_phosphokinase,
        diabetes,
        ejection_fraction,
        high_blood_pressure,
        platelets,
        serum_creatinine,
        serum_sodium,
        sex,
        smoking,
        predicted_risk,
        prediction,
        risk_label,
        threshold
    )
    VALUES (
        %s, %s, %s, %s, %s, %s, %s, %s, %s,
        %s, %s, %s, %s, %s, %s
    );
    """

    values = (
        data.age,
        data.anaemia,
        data.creatinine_phosphokinase,
        data.diabetes,
        data.ejection_fraction,
        data.high_blood_pressure,
        data.platelets,
        data.serum_creatinine,
        data.serum_sodium,
        data.sex,
        data.smoking,
        predicted_risk,
        prediction,
        risk_label,
        threshold,
    )

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(insert_sql, values)

        connection.commit()

def get_stats():
    """Return aggregate statistics using hand-written SQL."""

    stats_sql = """
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
    """

    with get_connection() as connection:
        with connection.cursor() as cursor:
            cursor.execute(stats_sql)
            row = cursor.fetchone()

    return {
        "total_requests": row[0],
        "average_predicted_risk": round(float(row[1]), 4),
        "high_risk_share": round(float(row[2]), 4),
    }