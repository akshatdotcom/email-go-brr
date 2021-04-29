import csv
import smtplib
from email.message import EmailMessage
from decouple import config

headings = []
data = []
with open('data.csv', 'r') as f:
    reader = csv.DictReader(f, delimiter=',')
    headings = reader.fieldnames
    for row in reader:
        data.append(row)

templateRawText = open("template.txt", "r").read()
for entry in data:
    filledTemplate = templateRawText
    for heading in entry:
        filledTemplate = filledTemplate.replace('{{ ' + heading + ' }}', entry[heading])
    entry["email_content"] = filledTemplate

server = smtplib.SMTP('smtp.gmail.com', 587)
try:
    server.ehlo()
    server.starttls()
    gmail_user = config("GMAIL_USER")
    gmail_password = config("GMAIL_PASSWORD")
    server.login(gmail_user, gmail_password)
except:
    print('Something went wrong in connecting to the SMTP server...')

emailsSent = 0
for entry in data:
    msg = EmailMessage()
    msg.set_content(entry["email_content"])
    msg['Subject'] = 'Testing'
    msg['From'] = config("GMAIL_USER")
    msg['To'] = entry["email"]
    msg['Cc'] = ''
    msg['Bcc'] = ''
    server.send_message(msg)
    emailsSent += 1
    print(str(emailsSent) + " out of " + str(len(data)) + " emails sent!")
server.close()