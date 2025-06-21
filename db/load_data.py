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
category.columns = category.columns.str.strip().str.lower()

required = ["category", "start_date", "end_date", "revenue"]
missing = [col for col in required if col not in category.columns]
if missing:
    raise ValueError(f"Expected columns in category CSV: {missing}")

category["category"] = category["category"].apply(standardize_category)
category["start_date"] = pd.to_datetime(category["start_date"])
category["end_date"] = pd.to_datetime(category["end_date"])
category["revenue"] = pd.to_numeric(
    category["revenue"].replace(r"(US)?\$|,", "", regex=True),
    errors="coerce"
)

# Log dropped rows
before = len(category)
category = category.dropna(subset=required)
after = len(category)
if before != after:
    print(f"⚠️ Dropped {before - after} rows from category_sales due to missing or malformed data.")
    print(category.head(3))

# === Load & Clean Sales Summary ===
summary = pd.read_csv(summary_path)
summary.columns = summary.columns.str.strip()
summary.rename(columns={summary.columns[0]: "Sales"}, inplace=True)

# Filter out irrelevant rows
summary = summary[summary["Sales"].notna()]
summary = summary[~summary["Sales"].str.lower().isin([
    "total", "payments", "fees", "net total", "total collected",
    "card", "cash", "other", "gift card", ""
])]

# Melt to long format
date_cols = [col for col in summary.columns if "/" in col]
summary = summary.melt(id_vars="Sales", value_vars=date_cols,
                       var_name="date_range", value_name="amount")
summary.rename(columns={"Sales": "sales_type"}, inplace=True)

# Extract date ranges
summary["start_date"] = pd.to_datetime(
    summary["date_range"].str.extract(r"(\d{2}/\d{2}/\d{4})")[0], format="%m/%d/%Y"
)
summary["end_date"] = pd.to_datetime(
    summary["date_range"].str.extract(r"-(\d{2}/\d{2}/\d{4})")[0], format="%m/%d/%Y"
)

# Clean amounts
summary["amount"] = summary["amount"].astype(str).replace(r"[^\d\.-]", "", regex=True)
summary["amount"] = pd.to_numeric(summary["amount"], errors="coerce")

# Map verbose labels to enum
def map_sales_type(label):
    label = label.lower()
    if "gross" in label or "net sales" in label:
        return "Sale"
    elif "tip" in label:
        return "Tip"
    elif "discount" in label or "comp" in label:
        return "Discount"
    elif "tax" in label:
        return "Tax"
    elif "refund" in label or "return" in label:
        return "Refund"
    else:
        return "Other"

summary["sales_type"] = summary["sales_type"].apply(map_sales_type)

# Enforce constraint: no negative amounts for Refunds/Discounts
summary.loc[summary["sales_type"].isin(["Refund", "Discount"]), "amount"] = (
    summary.loc[summary["sales_type"].isin(["Refund", "Discount"]), "amount"].abs()
)

summary = summary[["sales_type", "start_date", "end_date", "amount"]].dropna()

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

# Clean numeric columns
for col in ["gross_sales", "discounts", "refunds"]:
    if col in details.columns:
        details[col] = pd.to_numeric(
            details[col].replace(r"[\$,]", "", regex=True), errors="coerce"
        )

details.dropna(subset=required, inplace=True)
details = details[details["gross_sales"] >= 0]
if "discounts" in details.columns:
    details = details[details["discounts"] >= 0]
if "refunds" in details.columns:
    details = details[details["refunds"] >= 0]

# Standardize categories
if "category" in details.columns:
    details["category"] = details["category"].apply(standardize_category)

# Final keep columns
keep_cols = [
    "transaction_id", "item", "category", "date", "time",
    "gross_sales", "discounts", "refunds",
    "modifiers_applied", "channel", "card_brand",
    "employee_id", "employee_name", "customer_id", "customer_name"
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
