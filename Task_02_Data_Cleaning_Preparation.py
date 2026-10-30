"""Task 02 – Data Cleaning and Preparation | SkillCraft Technology
Extract train.csv from the supplied ZIP and place it beside this script.
Run: python Task_02_Data_Cleaning_Preparation.py
"""
from pathlib import Path
import pandas as pd
import numpy as np

sales = pd.read_csv(Path("train.csv"))
print("Original shape:", sales.shape)
print("Missing values before:\n", sales.isna().sum()[sales.isna().sum() > 0])
print("Exact duplicates:", sales.duplicated().sum())

cleaned = sales.drop_duplicates().copy()
for col in cleaned.select_dtypes(include=["object"]).columns:
    cleaned[col] = cleaned[col].astype("string").str.strip()

# Source dates use DD/MM/YYYY
for col in ["Order Date", "Ship Date"]:
    cleaned[col] = pd.to_datetime(cleaned[col], format="%d/%m/%Y", errors="coerce")

cleaned["Sales"] = pd.to_numeric(cleaned["Sales"], errors="coerce")
cleaned["Postal Code"] = pd.to_numeric(cleaned["Postal Code"], errors="coerce").astype("Int64")
cleaned["Order Year"] = cleaned["Order Date"].dt.year.astype("Int64")
cleaned["Order Month"] = cleaned["Order Date"].dt.month.astype("Int64")
cleaned["Order Month Name"] = cleaned["Order Date"].dt.strftime("%B").astype("string")
cleaned["Year-Month"] = cleaned["Order Date"].dt.to_period("M").astype("string")

cleaned.to_csv("Task_02_Cleaned_Superstore_Sales.csv", index=False)
print("Cleaned shape:", cleaned.shape)
print("Remaining duplicates:", cleaned.duplicated().sum())
print("Missing values after:\n", cleaned.isna().sum()[cleaned.isna().sum() > 0])
print("Export complete.")
