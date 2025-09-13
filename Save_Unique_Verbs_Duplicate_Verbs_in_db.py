import pandas as pd
import pyodbc

# 1️⃣ SQL Server connection parameters
server = r'(localdb)\MSSQLLocalDB'   # or 'localhost\SQLEXPRESS'
database = 'Arsipa'
driver = '{ODBC Driver 17 for SQL Server}'

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
print("✅ Connected to SQL Server")

# 2️⃣ Read Excel file
excel_file = r"C:\Users\Dell\Desktop\Python Practice\outputfiles\cleaned_data\Processed_Verbs.xlsx"
df1 = pd.read_excel(excel_file, sheet_name="Unique_Verbs")
df2 = pd.read_excel(excel_file, sheet_name="Duplicate_Verbs")

# drop null values from excel sheets
df1.dropna(inplace=True)
df2.dropna(inplace=True)


# Ensure column names match DB columns
print("📊 Unique_Verbs columns:", df1.columns.tolist())
print("📊 Duplicate_Verbs columns:", df2.columns.tolist())

# 3️⃣ Create tables
cursor.execute("""
IF OBJECT_ID('dbo.Duplicate_Verbs', 'U') IS NOT NULL DROP TABLE dbo.Duplicate_Verbs;
CREATE TABLE dbo.Duplicate_Verbs (
    VerbID INT IDENTITY(1,1) PRIMARY KEY,
    SrNo int,
    Verb NVARCHAR(500),
    Meaning NVARCHAR(500),
    Sample_Sentence NVARCHAR(500),
    Praesens NVARCHAR(500),    
    Praeteritum NVARCHAR(500),
    Perfekt NVARCHAR(500)
)
""")

cursor.execute("""
IF OBJECT_ID('dbo.Unique_Verbs', 'U') IS NOT NULL DROP TABLE dbo.Unique_Verbs;
CREATE TABLE dbo.Unique_Verbs (
    VerbID INT IDENTITY(1,1) PRIMARY KEY,
    SrNo int,
    Verb NVARCHAR(500),
    Meaning NVARCHAR(500),
    Sample_Sentence NVARCHAR(500),
    Praesens NVARCHAR(500),    
    Praeteritum NVARCHAR(500),
    Perfekt NVARCHAR(500)
)
""")

conn.commit()
print("✅ Tables created successfully")

# 4️⃣ Insert data from df1 into Unique_Verbs
for _, row in df1.iterrows():
    cursor.execute("""
        INSERT INTO dbo.Unique_Verbs (SrNo, Verb, Meaning, Sample_Sentence, Praesens, Praeteritum, Perfekt)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]))

# 5️⃣ Insert data from df2 into Duplicate_Verbs
for _, row in df2.iterrows():
    cursor.execute("""
        INSERT INTO dbo.Duplicate_Verbs (SrNo, Verb, Meaning, Sample_Sentence, Praesens, Praeteritum, Perfekt)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, str(row[0]), str(row[1]), str(row[2]), str(row[3]), str(row[4]), str(row[5]), str(row[6]))


conn.commit()
print("✅ Data inserted successfully into both tables")

cursor.close()
conn.close()
print("🔒 Connection closed")
