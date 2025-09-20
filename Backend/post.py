import pandas as pd
from sqlalchemy import create_engine

def upload_csv_to_postgres():
    DB_USER = "ghanagokulgabburi"
    DB_PASSWORD = "Saibaba3123"
    DB_HOST = "127.0.0.1"
    DB_PORT = "5432"
    DB_NAME = "housing_db"
    TABLE_NAME = "lease_data"
    CSV_FILE = "final_housing_dataset_with_links.csv"

    try:
        connection_string = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
        engine = create_engine(connection_string)

        df = pd.read_csv(CSV_FILE)

        # Optional: convert date columns to appropriate formats
        df["available_from"] = pd.to_datetime(df["available_from"], errors='coerce')
        df["created_at"] = pd.to_datetime(df["created_at"], errors='coerce')

        print(f"📄 Loaded {len(df)} rows from {CSV_FILE}")
        df.to_sql(TABLE_NAME, engine, index=False, if_exists="append")  # Use "append" not "replace"
        print(f"✅ Successfully uploaded data to '{TABLE_NAME}' in '{DB_NAME}'")

    except Exception as e:
        print(f"❌ Error uploading data: {e}")

if __name__ == "__main__":
    upload_csv_to_postgres()
