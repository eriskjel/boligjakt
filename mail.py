import smtplib
from email.message import EmailMessage
import os


def send_email(subject, body, to_emails):
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = os.environ['EMAIL_FROM']
    msg['To'] = to_emails

    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(os.environ['EMAIL_USERNAME'], os.environ['EMAIL_PASSWORD'])
    server.send_message(msg)
    server.quit()


if __name__ == '__main__':
    # Call the function with your subject and body
    subject = "Housing Rental Objects Notification"
    body = "Housing rental objects are now available!"
    to_emails = os.environ['RECIPIENT']  # Replace with the recipient's email address
    send_email(subject, body, to_emails)
