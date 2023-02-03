import smtplib
import configparser
from email.mime.text import MIMEText

config = configparser.ConfigParser()
config.read('config.ini')

sender_email = config['email']['sender']
bcc_emails = config['email']['bcc'].split(",")
password = config['email']['password']

message = MIMEText("""Hello World""")
message['Subject'] = "Hi there"
message['From'] = sender_email

try:
    server = smtplib.SMTP('smtp.qq.com', 25)
    server.ehlo()
    server.starttls()
    server.login(sender_email.split("<")[1][:-1], password)
    server.sendmail(sender_email, bcc_emails, message.as_string())
    print('Email sent!')
except Exception as e:
    print('Something went wrong...', e)
finally:
    server.quit()
