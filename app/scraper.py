import requests
import pandas as pd
from datetime import datetime
import psycopg2
import io
import os

# Configuration from environment variables
DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT", 5432)
DB_NAME = os.environ.get("DB_NAME")
DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
ETF = YieldMax

# Intraday file link (redirects to actual CSV)
DOWNLOAD_URL = "https://www.yieldmaxetfs.com/ym/intraday-file"

def download_csv():
    response = requests.get(DOWNLOAD_URL)
    response.raise_for_status()
    return response.content

def load_to_postgresql(csv_bytes):
    df = pd.read_csv(io.BytesIO(csv_bytes))
    df.columns = [col.strip().replace(" ", "_").lower() for col in df.columns]

    # Add a scrape_date column for auditing
    df["scrape_date"] = datetime.utcnow()

    conn = psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    cur = conn.cursor()
    # Create table if it doesn't exist
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {ETF.lower()}_intraday_trades (
        {", ".join([f"{col} TEXT" for col in df.columns if col != "scrape_date"])},
        scrape_date TIMESTAMP
    );
    """
    cur.execute(create_table_query)
    conn.commit()

    # Insert data
    for _, row in df.iterrows():
        placeholders = ','.join(['%s'] * len(row))
        insert_query = f"INSERT INTO {ETF.lower()}_intraday_trades VALUES ({placeholders})"
        cur.execute(insert_query, tuple(row))
    conn.commit()
    cur.close()
    conn.close()

def main():
    csv_bytes = download_csv()
    load_to_postgresql(csv_bytes)

if __name__ == "__main__":
    main()
