import pandas as pd
import csv

# Path to your Excel file
xlsx_path = "test.xlsx"

# Load Excel file
excel = pd.ExcelFile(xlsx_path)

# Convert each sheet to a CSV file
for sheet_name in excel.sheet_names:
    df = excel.parse(sheet_name)
    csv_filename = f"{sheet_name}.csv"
    df.to_csv(csv_filename, index=False)
    print(f"Saved {csv_filename}")