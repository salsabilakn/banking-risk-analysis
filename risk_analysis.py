
import pandas as pd
from pathlib import Path

# ==================================================
# 1. SETUP
# ==================================================

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "data" / "bank_risk_cleaned.csv"
OUTPUT_DIR = BASE_DIR / "output"

OUTPUT_DIR.mkdir(exist_ok=True)

if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Dataset tidak ditemukan: {DATA_PATH}\n"
        "Pastikan file bank_risk_cleaned.csv ada di folder data."
    )

df = pd.read_csv(DATA_PATH)

# Rapikan nama kolom dan ticker
df.columns = df.columns.str.strip()
df["TICKER"] = df["TICKER"].astype("string").str.strip().str.upper()

numeric_cols = [
    "YEAR",
    "NPL (%)",
    "NIM (%)",
    "BOPO (%)",
    "CAR (%)",
    "ROA (%)",
    "Stock Return (%)",
]

for col in numeric_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

# Hapus baris yang tidak memiliki identitas bank atau tahun
df = df.dropna(subset=["TICKER", "YEAR"]).copy()
df["YEAR"] = df["YEAR"].astype(int)

risk_cols = [
    "NPL (%)",
    "NIM (%)",
    "BOPO (%)",
    "CAR (%)",
    "ROA (%)",
    "Stock Return (%)",
]

# ==================================================
# 2. DATA QUALITY CHECK
# ==================================================

print("=" * 65)
print("BANKING RISK MANAGEMENT ANALYSIS")
print("=" * 65)

print("\n=== DATASET OVERVIEW ===")
print(f"Total observasi : {len(df)}")
print(f"Jumlah bank     : {df['TICKER'].nunique()}")
print(f"Periode         : {df['YEAR'].min()} - {df['YEAR'].max()}")
print(f"Jumlah kolom    : {len(df.columns)}")

print("\n=== DATA QUALITY ===")
print("\nMissing values:")
print(df.isna().sum().to_string())

duplicate_count = df.duplicated(
    subset=["TICKER", "YEAR"]
).sum()

print(f"\nDuplikasi bank-tahun: {duplicate_count}")

if duplicate_count > 0:
    print("PERINGATAN: Ada duplikasi bank-tahun yang perlu diperiksa.")
else:
    print("Tidak ditemukan duplikasi bank-tahun.")

# Simpan laporan kualitas data
quality_report = pd.DataFrame({
    "column": df.columns,
    "missing_values": [df[col].isna().sum() for col in df.columns],
    "data_type": [str(df[col].dtype) for col in df.columns],
})

quality_report.to_csv(
    OUTPUT_DIR / "data_quality_report.csv",
    index=False
)

# ==================================================
# 3. DESCRIPTIVE STATISTICS
# ==================================================

print("\n" + "=" * 65)
print("DESCRIPTIVE STATISTICS")
print("=" * 65)

descriptive_stats = df[risk_cols].describe().T.round(2)

print(descriptive_stats.to_string())

descriptive_stats.to_csv(
    OUTPUT_DIR / "descriptive_statistics.csv"
)

# ==================================================
# 4. AVERAGE INDICATORS BY BANK
# ==================================================

print("\n" + "=" * 65)
print("AVERAGE RISK INDICATORS BY BANK")
print("=" * 65)

bank_summary = (
    df.groupby("TICKER")[risk_cols]
    .mean()
    .round(2)
)

# Urutkan berdasarkan NPL tertinggi
bank_summary = bank_summary.sort_values(
    "NPL (%)",
    ascending=False
)

print(bank_summary.to_string())

bank_summary.to_csv(
    OUTPUT_DIR / "bank_risk_summary.csv"
)

# ==================================================
# 5. TOP 5 BANKS BY AVERAGE NPL
# ==================================================

print("\n=== TOP 5 BANKS WITH HIGHEST AVERAGE NPL ===")

top_npl_banks = bank_summary.nlargest(5, "NPL (%)")

print(top_npl_banks[["NPL (%)"]].to_string())

top_npl_banks.to_csv(
    OUTPUT_DIR / "top_5_average_npl_banks.csv"
)

# ==================================================
# 6. YEARLY NPL TREND
# ==================================================

print("\n" + "=" * 65)
print("AVERAGE NPL BY YEAR")
print("=" * 65)

yearly_npl = (
    df.groupby("YEAR")
    .agg(
        average_npl=("NPL (%)", "mean"),
        median_npl=("NPL (%)", "median"),
        average_car=("CAR (%)", "mean"),
        average_roa=("ROA (%)", "mean"),
        average_bopo=("BOPO (%)", "mean"),
    )
    .round(2)
)

print(yearly_npl.to_string())

yearly_npl.to_csv(
    OUTPUT_DIR / "yearly_risk_trend.csv"
)

# ==================================================
# 7. HIGHEST NPL OBSERVATIONS
# ==================================================

print("\n" + "=" * 65)
print("TOP 10 HIGHEST NPL OBSERVATIONS")
print("=" * 65)

top_npl_observations = df.nlargest(10, "NPL (%)")[
    ["TICKER", "YEAR", "NPL (%)", "CAR (%)", "BOPO (%)", "ROA (%)"]
]

print(top_npl_observations.to_string(index=False))

top_npl_observations.to_csv(
    OUTPUT_DIR / "top_10_npl_observations.csv",
    index=False
)

# ==================================================
# 8. EXTREME STOCK RETURNS
# ==================================================

return_cols = ["TICKER", "YEAR", "Stock Return (%)"]

print("\n" + "=" * 65)
print("TOP 10 HIGHEST STOCK RETURNS")
print("=" * 65)

top_returns = df.nlargest(10, "Stock Return (%)")[return_cols]

print(top_returns.to_string(index=False))

top_returns.to_csv(
    OUTPUT_DIR / "top_10_stock_returns.csv",
    index=False
)

print("\n=== TOP 10 LOWEST STOCK RETURNS ===")

lowest_returns = df.nsmallest(10, "Stock Return (%)")[return_cols]

print(lowest_returns.to_string(index=False))

lowest_returns.to_csv(
    OUTPUT_DIR / "bottom_10_stock_returns.csv",
    index=False
)

# ==================================================
# 9. BEKS NPL TREND
# ==================================================

print("\n" + "=" * 65)
print("BEKS NPL TREND")
print("=" * 65)

beks_data = (
    df.loc[
        df["TICKER"] == "BEKS",
        ["TICKER", "YEAR", "NPL (%)", "CAR (%)", "BOPO (%)", "ROA (%)"]
    ]
    .sort_values("YEAR")
)

if beks_data.empty:
    print("Data BEKS tidak ditemukan.")
else:
    print(beks_data.to_string(index=False))

beks_data.to_csv(
    OUTPUT_DIR / "beks_risk_trend.csv",
    index=False
)

# ==================================================
# 10. CORRELATION ANALYSIS
# ==================================================

print("\n" + "=" * 65)
print("CORRELATION BETWEEN INDICATORS")
print("=" * 65)

correlation = df[risk_cols].corr().round(3)

print(correlation.to_string())

correlation.to_csv(
    OUTPUT_DIR / "risk_correlation_matrix.csv"
)

# ==================================================
# 11. CHECK EXTREME VALUES
# ==================================================

print("\n" + "=" * 65)
print("EXTREME VALUE CHECK")
print("=" * 65)

for col in risk_cols:
    series = df[col].dropna()

    if series.empty:
        continue

    q1 = series.quantile(0.25)
    q3 = series.quantile(0.75)
    iqr = q3 - q1

    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr

    outliers = df.loc[
        df[col].notna()
        & (
            (df[col] < lower_bound)
            | (df[col] > upper_bound)
        ),
        ["TICKER", "YEAR", col]
    ]

    print(f"\n{col}")
    print(f"Lower bound: {lower_bound:.2f}")
    print(f"Upper bound: {upper_bound:.2f}")
    print(f"Jumlah observasi ekstrem: {len(outliers)}")

    if not outliers.empty:
        print(outliers.to_string(index=False))

# ==================================================
# 12. EXPORT ANALYTICAL DATA
# ==================================================

# Ekspor data yang sudah dibaca dan divalidasi
df.to_csv(
    OUTPUT_DIR / "bank_risk_analysis_data.csv",
    index=False
)

print("\n" + "=" * 65)
print("ANALYSIS COMPLETED")
print("=" * 65)

print(f"Hasil analisis tersimpan di: {OUTPUT_DIR.resolve()}")
print("\nFile output:")
for output_file in sorted(OUTPUT_DIR.glob("*.csv")):
    print(f"- {output_file.name}")
