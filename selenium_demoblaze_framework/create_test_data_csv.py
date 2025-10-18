# create_test_data_csv.py

import os
import csv

# Ensure the 'data' directory exists
os.makedirs("data", exist_ok=True)

# Define CSV file path
csv_file = "data/test_data.csv"

# Test data rows
test_data = [
    ["username", "password", "product", "category"],
    ["testuser1", "Test@123", "Samsung galaxy s6", "Phones"],
    ["testuser2", "Test@456", "MacBook air", "Laptops"],
    ["testuser3", "Test@789", "ASUS Full HD", "Monitors"]
]

# Write to CSV
with open(csv_file, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerows(test_data)

print("✅ CSV file 'data/test_data.csv' created successfully.")