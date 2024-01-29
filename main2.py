
from tkinter import messagebox
import requests
import pandas as pd
import subprocess
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

api_key = os.getenv("API_KEY")
url = os.getenv("TEQUILA_API_URL")

# fly_from = input("Enter the departure airport code: ")
# fly_to = input("Enter the destination airport code: ")
user_data = pd.read_csv('user_data.csv')

fly_from = user_data.loc[0, 'Departure City']
fly_to = user_data.loc[0, 'Destination City']
min_price=user_data.loc[0,'Minimum Price']
params = {
    "fly_from":fly_from,
    "fly_to": fly_to,
    "date_from": "2024-01-20",
    "date_to": "2024-01-24",
    "partner": api_key,
    "limit": 5  # You can adjust this limit based on the API's constraints
}

headers = {
    "apikey": api_key,
}

# Initialize an empty list to store the results and a set to store unique identifiers
results = []
unique_identifiers = set()

# Continue making requests until you have at least 6 unique results
while len(unique_identifiers) < 6:
    # Send an HTTP GET request to the API endpoint
    response = requests.get(url, params=params, headers=headers)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        data = response.json()

        # Extract unique identifiers from the new data
        new_identifiers = {item['id'] for item in data['data']}

        # Filter out duplicates and extend the results list
        new_results = [item for item in data['data'] if item['id'] not in unique_identifiers]
        results.extend(new_results)
        unique_identifiers.update(new_identifiers)
    else:
        print("Failed to retrieve data. Status code:", response.status_code)
        print(response.text)  # Print the response content for debugging purposes

# Extract only the desired columns and add a 'date' and 'time' column
selected_columns = ['flyFrom', 'flyTo', 'cityFrom', 'cityCodeFrom', 'cityTo', 'cityCodeTo','local_departure', 'price', 'route']
filtered_results = [{key: item[key] for key in selected_columns} for item in results]

# Convert the filtered list of dictionaries to a DataFrame
df = pd.DataFrame(filtered_results)

# Extract the date and time from 'local_departure' and add new 'date' and 'time' columns
df['date'] = pd.to_datetime(df['local_departure']).dt.strftime('%Y-%m-%d')
df['time'] = pd.to_datetime(df['local_departure']).dt.strftime('%H:%M:%S')

# Extract 'flight_no' from the 'route' column
df['flight_no'] = df['route'].apply(lambda x: x[0]['flight_no'] if isinstance(x, list) and len(x) > 0 else None)

# Reorder columns if needed and drop 'local_departure' and 'route'
df = df[['date', 'time', 'flyFrom', 'flyTo', 'cityFrom', 'cityCodeFrom', 'cityTo', 'cityCodeTo','local_departure', 'price', 'flight_no']]

# Sort the DataFrame by the 'price' column
df = df.sort_values(by='price')

# Save DataFrame to CSV
csv_file_path = 'flight_data_sorted.csv'
df.to_csv(csv_file_path, index=False, encoding='utf-8')

print(f"Data extraction successful. Check '{csv_file_path}' for sorted results.")

# Run readcsv.py
subprocess.run(['python', 'readcsv.py'])

# Run mail.py
subprocess.run(['python', 'mail.py'])

if min_price >= df['price'].min(): 
    # Run sms.py if the condition is met
    print("Okay We Found A Deal For U Sending msg ASAP")
    subprocess.run(['python', 'sms.py'])
else:
    # Handle the case when the deal is not found
    print("Sorry, No Deal Found Within Your Budget.")
    messagebox.showinfo("No Flights", "No flights available at your minimum price.")