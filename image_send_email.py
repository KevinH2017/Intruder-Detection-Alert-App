import smtplib, os, imghdr
from email.message import EmailMessage

SENDER = "khui3850@gmail.com"
TARGET = "khui3850@gmail.com"
PASSWORD = os.getenv("PASSWORD")  

def send_email(image):
    """Sends message with image attachment to the target email address"""
    print("send_email function started!")
    message = EmailMessage()
    message["Subject"] = "INTRUDER ALERT!"
    message.set_content("INTRUDER DETECTED! ALERT! INTRUDER DETECTED! ALERT!")

    with open(image, "rb") as file:
        content = file.read()

    # Adds image as attachment to target email server
    message.add_attachment(content, maintype="image", subtype=imghdr.what(None, content))

    gmail = smtplib.SMTP("smtp.gmail.com", 587)
    gmail.ehlo()
    gmail.starttls()
    gmail.login(SENDER, PASSWORD)
    gmail.sendmail(SENDER, TARGET, message.as_string())
    gmail.quit()
    print("send_email function ended!")

if __name__ == "__main__":
    send_email(image="./images/19.png")