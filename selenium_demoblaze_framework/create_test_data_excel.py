# create_test_data_excel.py

import os
import pandas as pd

# Ensure data directory exists
os.makedirs("data", exist_ok=True)

# Users data
users_data = [
    {"username": "testuser1", "password": "Test@123", "email": "test1@example.com", "phone": "+1234567890"},
    {"username": "testuser2", "password": "Test@456", "email": "test2@example.com", "phone": "+0987654321"},
]

# Products data
products_data = [
    {"product_name": "Samsung galaxy s6", "category": "Phones", "expected_price": "360"},
    {"product_name": "Nokia lumia 1520", "category": "Phones", "expected_price": "820"},
    {"product_name": "Sony vaio i5", "category": "Laptops", "expected_price": "790"},
]

# Orders data
orders_data = [
    {"name": "John Doe", "country": "USA", "city": "New York", "card": "1234567890123456", "month": "12", "year": "2025"},
    {"name": "Jane Smith", "country": "Canada", "city": "Toronto", "card": "9876543210987654", "month": "11", "year": "2026"},
]

# Write to Excel with multiple sheets
with pd.ExcelWriter("data/test_data.xlsx", engine="openpyxl") as writer:
    pd.DataFrame(users_data).to_excel(writer, sheet_name="Users", index=False)
    pd.DataFrame(products_data).to_excel(writer, sheet_name="Products", index=False)
    pd.DataFrame(orders_data).to_excel(writer, sheet_name="Orders", index=False)

print("✅ Excel file 'data/test_data.xlsx' created successfully.")