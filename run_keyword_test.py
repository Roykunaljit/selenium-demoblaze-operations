import subprocess
import os
import sys

# First, create fresh test data
print("=" * 60)
print("STEP 1: Creating fresh test data with unique username")
print("=" * 60)

# Use UTF-8 encoding to handle emojis properly on Windows
result = subprocess.run(
    [sys.executable, "create_fresh_test_data.py"],
    capture_output=True,
    text=True,
    encoding='utf-8',
    errors='replace'
)
print(result.stdout)
if result.stderr and "UnicodeDecodeError" not in result.stderr:
    print("Errors:", result.stderr)

# Verify the Excel file exists
excel_path = "selenium_demoblaze_framework/data/keyword_test_cases.xlsx"
if not os.path.exists(excel_path):
    print(f"ERROR: Excel file not found at {excel_path}")
    sys.exit(1)
else:
    print(f"SUCCESS: Excel file found at {excel_path}")

print("\n" + "=" * 60)
print("STEP 2: Running the keyword-driven test")
print("=" * 60)

# Run the test
result = subprocess.run(
    [sys.executable, "-m", "pytest",
     "selenium_demoblaze_framework/tests/test_keyword_driven.py",
     "-v", "-s"],
    capture_output=False,
    text=True
)

print("\nTest execution completed!")
if result.returncode == 0:
    print("ALL TESTS PASSED!")
else:
    print("Some tests failed. Check the report for details.")