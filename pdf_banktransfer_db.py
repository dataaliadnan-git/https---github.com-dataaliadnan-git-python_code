# program to retreive table from pdf and store the contents in database table.

import pdfplumber
import pandas as pd
import pyodbc
import datetime

# 1️⃣ Path to your PDF
pdf_path = r"C:\Users\Dell\Desktop\Python Practice\source_datafiles\pdfs\BankTransfer.pdf"

# 2️⃣ Extract all tables from PDF
all_tables = []

with pdfplumber.open(pdf_path) as pdf:
    for page_number, page in enumerate(pdf.pages, start=1):
        tables = page.extract_tables()
        for table_number, table in enumerate(tables, start=1):
            if len(table) > 1:  # Skip empty tables
                df = pd.DataFrame(table[1:], columns=table[0])
                df['Page'] = page_number
                df['Table_Number'] = table_number
                all_tables.append(df)

# Combine all tables
if all_tables:
    final_df = pd.concat(all_tables, ignore_index=True)
else:
    final_df = pd.DataFrame()


# Add create_date and last_update columns
final_df["create_date"] = datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S")
final_df["last_update"] = None

# Optional: Preview
print(final_df.head())
print(final_df)
print("✅ Data Fram Printed")
