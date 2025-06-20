# app/utils.py

from sqlalchemy import create_engine, text
from dotenv import load_dotenv
import pandas as pd
import os

# === Load environment variables from .env ===
load_dotenv()

# === Build Supabase-compatible DB URL with SSL ===
DB_URL = (
    f"postgresql+psycopg2://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}?sslmode=require"
)

engine = create_engine(DB_URL)

def fetch_query(sql_path: str) -> pd.DataFrame:
    """
    Load and run a SQL query from file and return results as a DataFrame.
    Also logs the returned columns to help debug mismatched names.
    """
    try:
        with open(sql_path, "r") as file:
            query = text(file.read())

        with engine.begin() as conn:
            df = pd.read_sql_query(query, conn)

        # === Debugging Aid ===
        print(f"[DEBUG] ✅ Query: {sql_path}")
        print(f"[DEBUG] Columns: {df.columns.tolist()}")

        return df

    except Exception as e:
        print(f"[ERROR] ❌ Failed to run query: {sql_path}")
        print(f"[ERROR] {str(e)}")
        return pd.DataFrame()  # Fail gracefully


def rename_columns(df: pd.DataFrame, rename_map: dict) -> pd.DataFrame:
    """
    Rename columns in a DataFrame using a provided mapping dictionary.
    Only renames columns that exist.

    Args:
        df: The DataFrame to rename.
        rename_map: A dictionary like {'old_col': 'new_col'}

    Returns:
        The same DataFrame with columns renamed where applicable.
    """
    for old, new in rename_map.items():
        if old in df.columns:
            df.rename(columns={old: new}, inplace=True)
    return df
