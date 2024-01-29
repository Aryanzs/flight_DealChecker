import pandas as pd
from tabulate import tabulate

# Replace 'your_file_path' with the actual path to your CSV file
csv_file_path = 'flight_data_sorted.csv'

# Read the CSV file into a DataFrame
try:
    df = pd.read_csv(csv_file_path)
    print("CSV file successfully loaded into DataFrame.")
    
    # Print the DataFrame in a well-formatted table
    print(tabulate(df, headers='keys', tablefmt='pretty'))
    
except FileNotFoundError:
    print(f"Error: The file {csv_file_path} was not found.")
except pd.errors.EmptyDataError:
    print(f"Error: The file {csv_file_path} is empty.")
except pd.errors.ParserError as e:
    print(f"Error: Unable to parse the CSV file. {e}")
