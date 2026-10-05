import pandas as pd

DATA_PATH = "data/heart_failure_clinical_records_dataset.csv"

# Load dataset
df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("DATASET SHAPE")
print("=" * 60)
print(df.shape)

print("\n" + "=" * 60)
print("DATA TYPES")
print("=" * 60)
print(df.dtypes)

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)
print(df.isnull().sum())

print("\nTotal missing values:", df.isnull().sum().sum())

print("\n" + "=" * 60)
print("DUPLICATE ROWS")
print("=" * 60)
print("Duplicate rows:", df.duplicated().sum())

print("\n" + "=" * 60)
print("TARGET VALUES")
print("=" * 60)
print(df["DEATH_EVENT"].value_counts().sort_index())

print("\n" + "=" * 60)
print("UNIQUE VALUES IN BINARY FEATURES")
print("=" * 60)

binary_features = [
    "anaemia",
    "diabetes",
    "high_blood_pressure",
    "sex",
    "smoking",
    "DEATH_EVENT"
]

for column in binary_features:
    print(f"{column}: {sorted(df[column].unique())}")

print("\n" + "=" * 60)
print("SUMMARY STATISTICS")
print("=" * 60)
print(df.describe())