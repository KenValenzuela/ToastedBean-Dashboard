# db/load_data.py

import os
from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# === Setup ===
project_root = Path(__file__).resolve().parent.parent
os.chdir(project_root)

import sys
sys.path.append(str(project_root / "db"))
from category_map import standardize_category

# === Load Env ===
load_dotenv(dotenv_path=project_root / ".env")
DB_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?sslmode=require"
)
engine = create_engine(DB_URL)

# === File Paths ===
category_path = Path("data/cleaned/cleaned_category_sales.csv")
summary_path = Path("data/cleaned/cleaned_sales_summary.csv")
details_path = Path("data/cleaned/cleaned_detail_items.csv")
schema_path = Path("db/schema.sql")

for path in [category_path, summary_path, details_path, schema_path]:
    if not path.exists():
        raise FileNotFoundError(f"Missing required file: {path}")

# === Load & Clean Category Sales ===
category = pd.read_csv(category_path)
category.columns = category.columns.str.strip()
category = category.melt(id_vars="Category", var_name="date_range", value_name="revenue")
category["revenue"] = category["revenue"].replace(r"[\$,US]", "", regex=True).replace(",", "", regex=True).astype(float)
category["category"] = category["Category"].apply(standardize_category)
category.drop(columns=["Category"], inplace=True)
category.columns = category.columns.str.lower()

# === Load & Clean Summary ===
summary = pd.read_csv(summary_path)
summary.columns = summary.columns.str.strip()
summary = summary.melt(id_vars="Sales", var_name="date_range", value_name="amount")
summary.rename(columns={"Sales": "sales_type"}, inplace=True)
summary["amount"] = summary["amount"].replace(r"[\$,US]", "", regex=True).replace(",", "", regex=True)
summary["amount"] = pd.to_numeric(summary["amount"], errors="coerce")
summary.dropna(subset=["sales_type", "date_range", "amount"], inplace=True)
summary.columns = summary.columns.str.lower()

# === Load & Clean Detail Items ===
details = pd.read_csv(details_path)
details.columns = (
    details.columns.str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace("-", "_")
)

required = ["item", "date", "time", "gross_sales"]
missing = [col for col in required if col not in details.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")

for col in ["gross_sales", "discounts", "refunds"]:
    if col in details.columns:
        details[col] = details[col].replace(r"[\$,US]", "", regex=True).replace(",", "", regex=True)
        details[col] = pd.to_numeric(details[col], errors="coerce")

details.dropna(subset=required, inplace=True)
details = details[details["gross_sales"] >= 0]
if "discounts" in details.columns:
    details = details[details["discounts"] >= 0]
if "refunds" in details.columns:
    details = details[details["refunds"] >= 0]

if "category" in details.columns:
    details["category"] = details["category"].apply(standardize_category)

keep_cols = [
    "item", "category", "date", "time", "gross_sales", "discounts", "refunds",
    "modifiers_applied", "channel", "card_brand", "transaction_id",
    "customer_id", "customer_name"
]
details = details[[c for c in keep_cols if c in details.columns]]

# === Execute Schema (DROP + CREATE) ===
with engine.begin() as conn:
    conn.execute(text(schema_path.read_text()))

# === Load Tables ===
category.to_sql("category_sales", engine, if_exists="append", index=False)
summary.to_sql("sales_summary", engine, if_exists="append", index=False)
details.to_sql("detail_items", engine, if_exists="append", index=False)

# === Load Customers ===
if "customer_id" in details.columns and "customer_name" in details.columns:
    customers = (
        details[["customer_id", "customer_name"]]
        .dropna()
        .drop_duplicates()
        .query("customer_name.str.strip() != '' and customer_name.str.strip() != ','", engine="python")
    )
    customers.to_sql("customers", engine, if_exists="replace", index=False)
    print(f"✅ Loaded: {len(customers)} cleaned customers.")
else:
    print("⚠️ Skipped customer table — missing required columns.")

# === Final Log ===
print(f"✅ Loaded: {len(category)} category rows | {len(summary)} summary rows | {len(details)} detail rows.")
