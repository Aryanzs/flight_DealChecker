import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
import pandas as pd
from tabulate import tabulate

def send_email(receiver_email, subject, body, attachment_path=None):
    # Set up the SMTP server
    smtp_server = "smtp.gmail.com"
    smtp_port = 587
    smtp_username = "your_gmail_id"  # Replace with your Gmail email address
    smtp_password = "your_smtp_password"  # Replace with your Gmail app password

    # Set up the message
    message = MIMEMultipart()
    message["From"] = smtp_username
    message["To"] = receiver_email
    message["Subject"] = subject

    # Attach the body of the email
    message.attach(MIMEText(body, "plain"))

    # Attach the CSV file if specified
    if attachment_path:
        with open(attachment_path, "rb") as file:
            attachment = MIMEApplication(file.read(), _subtype="csv")
            attachment.add_header("Content-Disposition", f"attachment; filename=flight_data_sorted.csv")
            message.attach(attachment)

    # Connect to the SMTP server and send the email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(smtp_username, receiver_email, message.as_string())
        server.quit()
        print("Email sent successfully.")
    except Exception as e:
        print(f"Error: Unable to send email. {e}")

# Example usage:
#receiver_email = "supersaiyanaryan@gmail.com"  # Replace with the recipient's email address
user_data = pd.read_csv('user_data.csv')
receiver_email = user_data.loc[0, 'Email'] 
subject = "Flight Data Information"

# Replace 'your_file_path/filename.csv' with the actual path to your CSV file
csv_file_path = 'flight_data_sorted.csv'

# Read the CSV file into a DataFrame
try:
    df = pd.read_csv(csv_file_path)
    print("CSV file successfully loaded into DataFrame.")
    
    # Tabulate the DataFrame
    tabulated_data = tabulate(df, headers='keys', tablefmt='pretty')
    
    # Customize the body of the email with the tabulated data
    body = f"Hello,\n\nHere is the flight data:\n\n{tabulated_data}\n\nBest regards,\nYour Name"
    
    # Send the email with the CSV file attached
    send_email(receiver_email, subject, body, csv_file_path)

except FileNotFoundError:
    print(f"Error: The file {csv_file_path} was not found.")
except pd.errors.EmptyDataError:
    print(f"Error: The file {csv_file_path} is empty.")
except pd.errors.ParserError as e:
    print(f"Error: Unable to parse the CSV file. {e}")
