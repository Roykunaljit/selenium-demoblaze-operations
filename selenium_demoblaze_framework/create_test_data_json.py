# create_test_data_json.py

import os
import json

os.makedirs("data", exist_ok=True)

test_data = {
    "users": [
        {
            "username": "testuser1",
            "password": "Test@123",
            "email": "test1@example.com"
        },
        {
            "username": "testuser2",
            "password": "Test@456",
            "email": "test2@example.com"
        }
    ],
    "products": [
        {
            "name": "Samsung galaxy s6",
            "category": "Phones",
            "price": "360"
        },
        {
            "name": "Nokia lumia 1520",
            "category": "Phones",
            "price": "820"
        }
    ]
}

with open("data/test_data.json", "w", encoding="utf-8") as f:
    json.dump(test_data, f, indent=4)

print("✅ JSON file 'data/test_data.json' created successfully.")