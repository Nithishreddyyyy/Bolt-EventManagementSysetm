import smtplib
from email.message import EmailMessage
import ssl # Import the ssl module

# --- Your Email Details ---
sender_email = "nithishreddydps@gmail.com"
receiver_email = "nithishreddyb2@gmail.com"
password = 0 #Use 16 char

# --- Create the Email Message ---
msg = EmailMessage()
msg['Subject'] = "Hello from Python! 🐍"
msg['From'] = sender_email
msg['To'] = receiver_email
msg.set_content("This is a test email.")

# --- CREATE AN INSECURE SSL CONTEXT ---
# This part is the change. It tells Python not to verify the certificate.
context = ssl.create_default_context()
context.check_hostname = False
context.verify_mode = ssl.CERT_NONE

# --- Send the Email using the insecure context ---
try:
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(sender_email, password)
        smtp.send_message(msg)
        print("Email sent successfully!")
except Exception as e:
    print(f"Error: {e}")