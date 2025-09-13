import json
import pyodbc

# 1️⃣ SQL Server connection parameters
server = r'(localdb)\MSSQLLocalDB'   # or 'localhost\SQLEXPRESS'
database = 'Arsipa'
driver = '{ODBC Driver 17 for SQL Server}'

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};Trusted_Connection=yes;'
conn = pyodbc.connect(conn_str)
cursor = conn.cursor()
print("✅ Connected to SQL Server")

# 2️⃣ Load JSON file
json_file = r"C:\Users\Dell\Desktop\Python Practice\source_datafiles\jsonfiles\customer_orders.json"
with open(json_file, "r", encoding="utf-8") as f:
    data = json.load(f)

customer = data["customer"]
orders = data["orders"]
loyalty = data["loyalty"]

# 3️⃣ Drop & Create tables
cursor.execute("""
IF OBJECT_ID('dbo.OrderItems', 'U') IS NOT NULL DROP TABLE dbo.OrderItems;
IF OBJECT_ID('dbo.Orders', 'U') IS NOT NULL DROP TABLE dbo.Orders;
IF OBJECT_ID('dbo.Loyalty', 'U') IS NOT NULL DROP TABLE dbo.Loyalty;
IF OBJECT_ID('dbo.Customers', 'U') IS NOT NULL DROP TABLE dbo.Customers;

CREATE TABLE dbo.Customers (
    CustomerID NVARCHAR(50) PRIMARY KEY,
    FirstName NVARCHAR(100),
    LastName NVARCHAR(100),
    Email NVARCHAR(150),
    Phone NVARCHAR(50),
    BillingStreet NVARCHAR(200),
    BillingCity NVARCHAR(100),
    BillingPostalCode NVARCHAR(20),
    BillingCountry NVARCHAR(50),
    ShippingStreet NVARCHAR(200),
    ShippingCity NVARCHAR(100),
    ShippingPostalCode NVARCHAR(20),
    ShippingCountry NVARCHAR(50),
    CreatedAt DATETIME
);

CREATE TABLE dbo.Orders (
    OrderID NVARCHAR(50) PRIMARY KEY,
    CustomerID NVARCHAR(50),
    OrderDate DATETIME,
    Status NVARCHAR(50),
    ShippingMethod NVARCHAR(50),
    SubTotal DECIMAL(10,2),
    Shipping DECIMAL(10,2),
    Tax DECIMAL(10,2),
    Discount DECIMAL(10,2),
    Total DECIMAL(10,2),
    Currency NVARCHAR(10),
    Notes NVARCHAR(500),
    FOREIGN KEY (CustomerID) REFERENCES dbo.Customers(CustomerID)
);

CREATE TABLE dbo.OrderItems (
    ItemID INT IDENTITY(1,1) PRIMARY KEY,
    OrderID NVARCHAR(50),
    SKU NVARCHAR(50),
    Name NVARCHAR(200),
    Quantity INT,
    UnitPrice DECIMAL(10,2),
    Currency NVARCHAR(10),
    FOREIGN KEY (OrderID) REFERENCES dbo.Orders(OrderID)
);

CREATE TABLE dbo.Loyalty (
    LoyaltyID INT IDENTITY(1,1) PRIMARY KEY,
    CustomerID NVARCHAR(50),
    Program NVARCHAR(50),
    Points INT,
    Joined DATE,
    FOREIGN KEY (CustomerID) REFERENCES dbo.Customers(CustomerID)
);
""")
conn.commit()
print("✅ Tables created successfully")

# 4️⃣ Insert Customer
cursor.execute("""
    INSERT INTO dbo.Customers (
        CustomerID, FirstName, LastName, Email, Phone,
        BillingStreet, BillingCity, BillingPostalCode, BillingCountry,
        ShippingStreet, ShippingCity, ShippingPostalCode, ShippingCountry,
        CreatedAt
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", customer["customer_id"], customer["first_name"], customer["last_name"],
     customer["email"], customer["phone"],
     customer["billing_address"]["street"], customer["billing_address"]["city"],
     customer["billing_address"]["postal_code"], customer["billing_address"]["country"],
     customer["shipping_address"]["street"], customer["shipping_address"]["city"],
     customer["shipping_address"]["postal_code"], customer["shipping_address"]["country"],
     customer["created_at"])
print("✅ Customer inserted")

# 5️⃣ Insert Orders + Items
for order in orders:
    cursor.execute("""
        INSERT INTO dbo.Orders (
            OrderID, CustomerID, OrderDate, Status, ShippingMethod,
            SubTotal, Shipping, Tax, Discount, Total, Currency, Notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, order["order_id"], customer["customer_id"], order["order_date"], order["status"],
         order["shipping_method"], order["summary"]["sub_total"], order["summary"]["shipping"],
         order["summary"]["tax"], order["summary"]["discount"], order["summary"]["total"],
         order["summary"]["currency"], order["notes"])

    # Insert Order Items
    for item in order["items"]:
        cursor.execute("""
            INSERT INTO dbo.OrderItems (OrderID, SKU, Name, Quantity, UnitPrice, Currency)
            VALUES (?, ?, ?, ?, ?, ?)
        """, order["order_id"], item["sku"], item["name"], item["quantity"],
             item["unit_price"], item["currency"])
print("✅ Orders & Items inserted")

# 6️⃣ Insert Loyalty
cursor.execute("""
    INSERT INTO dbo.Loyalty (CustomerID, Program, Points, Joined)
    VALUES (?, ?, ?, ?)
""", customer["customer_id"], loyalty["program"], loyalty["points"], loyalty["joined"])
print("✅ Loyalty inserted")

# ✅ Commit all changes
conn.commit()

cursor.close()
conn.close()
print("🔒 Connection closed")