import schedule
import time
from datetime import datetime
import pandas as pd
import json
import smtplib
import os
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

# Function to load player data from JSON file
def load_data():
    try:
        with open("registrations.json", "r", encoding="utf-8") as file:
            return pd.DataFrame(json.load(file))
    except FileNotFoundError:
        return pd.DataFrame(columns=["Name", "Alliance", "Time Zone", "Fight Time", "Approved"])

# Function to save player data to JSON file
def save_data(data):
    temp_file = "registrations_temp.json"
    data.to_json(temp_file, orient="records", force_ascii=False, indent=4)
    os.replace(temp_file, "registrations.json")

# Function to archive and reset the registrations
def archive_and_reset():
    data = load_data()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archive_file = f"registrations_archive_{timestamp}.json"
    data.to_json(archive_file, orient="records", force_ascii=False, indent=4)
    save_data(pd.DataFrame(columns=["Name", "Alliance", "Time Zone", "Fight Time", "Approved"]))
    print("Registrations have been archived and reset.")

# Function to convert JSON to Excel
def convert_json_to_excel(json_file, excel_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    df = pd.DataFrame(data)
    df.to_excel(excel_file, index=False, engine='openpyxl')
    print(f"Converted {json_file} to {excel_file}")

# Function to send email
def send_email(sender_email, receiver_emails, subject, body, excel_file, smtp_server, smtp_port, smtp_username, smtp_password):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = ', '.join(receiver_emails)
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    attachment = MIMEBase('application', 'octet-stream')
    with open(excel_file, 'rb') as f:
        attachment.set_payload(f.read())
    encoders.encode_base64(attachment)
    attachment.add_header('Content-Disposition', f'attachment; filename={excel_file}')
    msg.attach(attachment)

    server = smtplib.SMTP(smtp_server, smtp_port)
    server.starttls()
    server.login(smtp_username, smtp_password)
    text = msg.as_string()
    server.sendmail(sender_email, receiver_emails, text)
    server.quit()
    print(f"Email sent to {', '.join(receiver_emails)} with attachment {excel_file}")

# New task to convert JSON to Excel and send via email
def json_to_excel_and_send_email():
    json_file = 'registrations.json'
    excel_file = 'registrations.xlsx'
    
    # Convert JSON to Excel
    convert_json_to_excel(json_file, excel_file)
    
    # Send Email
    sender_email = 'KD3270@outlook.com'
    receiver_emails = ['jackicapatain44@outlook.com', 'KD3270@outlook.com']
    subject = 'Registration Data'
    body = 'Please find the attached registration data.'
    smtp_server = 'smtp.office365.com'
    smtp_port = 587
    smtp_username = os.getenv('SMTP_USERNAME', 'KD3270@outlook.com')
    smtp_password = os.getenv('SMTP_PASSWORD', '3270Kingdom')

    send_email(sender_email, receiver_emails, subject, body, excel_file, smtp_server, smtp_port, smtp_username, smtp_password)

# Schedule archiving and resetting
schedule.every().tuesday.at("11:00").do(archive_and_reset)
schedule.every().tuesday.at("12:00").do(lambda: save_data(pd.DataFrame(columns=["Name", "Alliance", "Time Zone", "Fight Time", "Approved"])))

# Schedule the task to convert JSON to Excel and send via email
schedule.every().tuesday.at("13:00").do(json_to_excel_and_send_email)

# Run the scheduled tasks
while True:
    schedule.run_pending()
    time.sleep(1)
