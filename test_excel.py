import pandas as pd

# Define the path to the CSV file (instead of Excel)
csv_file = 'attendance.csv'

try:
    # Try reading the CSV file
    df = pd.read_csv(csv_file)  # Use read_csv for CSV files
    print(f"CSV file loaded successfully:\n{df}")
except Exception as e:
    print(f"Error reading the CSV file: {e}")

# Create a new DataFrame with a sample BI number
new_entry = pd.DataFrame({'BI Number': ['123456']})

try:
    # Try writing to the CSV file
    new_entry.to_csv(csv_file, index=False)  # Save to the same CSV file
    print(f"New entry has been written to {csv_file}")
except Exception as e:
    print(f"Error saving the CSV file: {e}")
