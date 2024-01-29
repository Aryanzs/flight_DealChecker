from twilio.rest import Client
import pandas as pd
from dotenv import load_dotenv
import os

load_dotenv()


# Your Twilio Account SID and Auth Token
account_sid = os.getenv("TWILIO_ACCOUNT_SID")

auth_token = auth_token = os.getenv("TWILIO_AUTH_TOKEN")


# Create a Twilio client
client = Client(account_sid, auth_token)

def send_sms(to_phone_number, message):
    try:
        # Replace 'your_twilio_phone_number' with your Twilio phone number
        from_phone_number = os.getenv("TWILIO_PHONE_NUMBER")


        # Send the SMS
        message = client.messages.create(
            body=message,
            from_=from_phone_number,
            to=to_phone_number
        )

        print(f"SMS sent successfully. SID: {message.sid}")

    except Exception as e:
        print(f"Error: Unable to send SMS. {e}")

# Example usage:
to_phone_number = os.getenv("RECIPIENT_PHONE_NUMBER") # Replace with the recipient's phone number
fly_data = pd.read_csv('flight_data_sorted.csv')
first_row_data = fly_data.iloc[0].to_dict()
message = ', '.join([f"{key}: {value}" for key, value in first_row_data.items()])

send_sms(to_phone_number, message)
