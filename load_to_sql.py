
import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
CSV_PATH = BASE_DIR / "output" / "bank_risk_analysis_data.csv"
DB_PATH = BASE_DIR / "banking_risk.db"

# Load data hasil analisis
df = pd.read_csv(CSV_PATH)

# Simpan ke database SQLite
with sqlite3.connect(DB_PATH) as conn:
    df.to_sql(
        "bank_risk",
        conn,
        if_exists="replace",
        index=False
    )

    # Verifikasi jumlah baris
    result = pd.read_sql_query(
        "SELECT COUNT(*) AS total_rows FROM bank_risk",
        conn
    )

    print("=== DATABASE BERHASIL DIBUAT ===")
    print(f"Lokasi database: {DB_PATH}")
    print(result.to_string(index=False))

    # Contoh query: lima observasi dengan NPL tertinggi
    query = """
        SELECT
            TICKER,
            YEAR,
            "NPL (%)",
            "CAR (%)",
            "BOPO (%)",
            "ROA (%)"
        FROM bank_risk
        ORDER BY "NPL (%)" DESC
        LIMIT 5;
    """

    top_npl = pd.read_sql_query(query, conn)

    print("\n=== TOP 5 OBSERVASI NPL TERTINGGI ===")
    print(top_npl.to_string(index=False))