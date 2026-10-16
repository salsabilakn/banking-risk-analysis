
import pandas as pd
from pathlib import Path

# 1. Baca sheet REKAP
file_path = Path("data/Indri Gunawan File Jurnal.xlsx")
df = pd.read_excel(file_path, sheet_name="REKAP")

# 2. Rapikan nama kolom
df.columns = df.columns.str.strip()

# 3. Isi ticker kosong berdasarkan ticker sebelumnya
df["TICKER"] = df["TICKER"].ffill()

# 4. Pastikan kolom numerik terbaca dengan benar
numeric_cols = [
    "YEAR", "NPL (%)", "NIM (%)",
    "BOPO (%)", "CAR (%)", "ROA (%)",
    "Stock Return (%)"
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# 5. Periksa kualitas data
print("=== UKURAN DATA ===")
print(f"Baris: {df.shape[0]}")
print(f"Kolom: {df.shape[1]}")

print("\n=== JUMLAH BANK ===")
print(df["TICKER"].nunique())
print(sorted(df["TICKER"].dropna().unique()))

print("\n=== RENTANG TAHUN ===")
print(df["YEAR"].min(), "-", df["YEAR"].max())

print("\n=== NILAI KOSONG ===")
print(df.isna().sum())

print("\n=== DUPLIKASI BANK-TAHUN ===")
print(df.duplicated(subset=["TICKER", "YEAR"]).sum())

# 6. Simpan dataset hasil cleaning
output_path = Path("data/bank_risk_cleaned.csv")
df.to_csv(output_path, index=False)

print("\nDataset bersih disimpan di:")
print(output_path.resolve())