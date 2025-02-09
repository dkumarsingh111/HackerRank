import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import configparser

config = configparser.ConfigParser()
config.read("config.ini")

# Access values
# smtp_server = config.get("EMAIL", "smtp_server")
# smtp_port = config.getint("EMAIL", "smtp_port")
# sender_email = config.get("EMAIL", "sender_email")
# receiver_email = config.get("EMAIL", "receiver_email")

smtp_server = "casarray1.bdx.com"
smtp_port = 587
sender_email = "SAGE50ACCOUNT@bd.com"
receiver_email = "deepak.singh@bd.com"


# Create the Email Message
msg = MIMEMultipart()
msg["From"] = sender_email
msg["To"] = receiver_email
msg["Subject"] = "Test Email from Python"
body = "Hello, this is a test email sent from Python!"
msg.attach(MIMEText(body, "plain"))

# Connect to SMTP Server and Send Email
try:
    server = smtplib.SMTP(smtp_server, 25)
    server.sendmail(sender_email, receiver_email, "Subject: Hello\n\nThis is a test email!")
    print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")
# finally:
#     server.close()
