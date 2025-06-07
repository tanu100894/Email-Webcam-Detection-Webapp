import smtplib, os
import mimetypes
from email.message import EmailMessage
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def send_email(image_path):
    email_message = EmailMessage()
    email_message["Subject"] = "New Customer showed up!"
    email_message.set_content("Hey, we just saw a new customer!")

    with open(image_path, "rb") as file:
        content = file.read()

    # Guess the mime type (e.g. image/png, image/jpeg)
    mime_type, _ = mimetypes.guess_type(image_path)
    print(mime_type)
    maintype, subtype = mime_type.split("/")
    print(maintype, subtype)

    email_message.add_attachment(content, maintype=maintype, subtype=subtype, filename=os.path.basename(image_path))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()

    SENDER = os.getenv("sender_email")
    PASSWORD = os.getenv("password")
    RECEIVER = os.getenv("receiver_email")
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, RECEIVER, email_message.as_string())
    gmail.quit()

if __name__ == "__main__":
    send_email(image_path="images/19.png")

