
import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "banking_risk.db"

with sqlite3.connect(DB_PATH) as conn:

    # 1. Rata-rata NPL setiap bank
    query_npl = """
        SELECT
            TICKER,
            ROUND(AVG("NPL (%)"), 2) AS avg_npl,
            ROUND(AVG("ROA (%)"), 2) AS avg_roa,
            ROUND(AVG("BOPO (%)"), 2) AS avg_bopo
        FROM bank_risk
        GROUP BY TICKER
        ORDER BY avg_npl DESC;
    """

    print("=== RATA-RATA RISIKO SETIAP BANK ===")
    for row in conn.execute(query_npl):
        print(row)

    # 2. Tren NPL setiap tahun
    query_yearly = """
        SELECT
            YEAR,
            ROUND(AVG("NPL (%)"), 2) AS avg_npl
        FROM bank_risk
        GROUP BY YEAR
        ORDER BY YEAR;
    """

    print("\n=== TREN NPL TAHUNAN ===")
    for row in conn.execute(query_yearly):
        print(row)

    # 3. Observasi dengan NPL di atas 5%
    query_high_npl = """
        SELECT
            TICKER,
            YEAR,
            "NPL (%)",
            "ROA (%)"
        FROM bank_risk
        WHERE "NPL (%)" > 5
        ORDER BY "NPL (%)" DESC;
    """

    print("\n=== OBSERVASI DENGAN NPL DI ATAS 5% ===")
    for row in conn.execute(query_high_npl):
        print(row)
