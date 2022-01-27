from fastapi import FastAPI
from config import settings
from parse_try import parse
from email.message import EmailMessage
import os
import smtplib
from dotenv import load_dotenv, find_dotenv
from celery_worker import parsing_celery, email
load_dotenv(dotenv_path=find_dotenv())

CITY = ["almaty", "nur-sultan"]

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    contact=settings.CONTACT,
    openapi_tags=settings.TAGS
)

@app.post('/kolesa/', tags=["Adds"])
def parsing(number_adds: int, city, price1: int, price2: int):
    value = parse(number_adds, city, price1, price2)
    if value == 1:
        return {"Message": "<ERROR ON PARSING>"}
    else: 
        return value


@app.post('/kolesa/send/', tags=["Sending email"])
def email_send(mail):
    msg = EmailMessage()
    msg['Subject'] = 'PARSER OF KOLESA'
    msg['From'] = os.getenv("EMAIL")
    msg['To'] = mail
    msg.set_content('LIST OF ADDS')
    files = ['kolesa.xlsx']
    for file in files:
        with open(file, 'rb') as f:
            file_data = f.read()
            file_name = f.name

        msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
        print('Message sended')
        smtp.send_message(msg)
    return {"Message": "Email sended"}


@app.post("/celery/")
def celery_parse(number_adds: int, city, price1: int, price2: int, mail):
    if city not in CITY:
        return {"Message": "This city is not available"}
    if price1 > price2:
        return {"Message": "<Price1> can't be more than <price2>"}
    else:
        asyncresult = parsing_celery.delay(number_adds, city, price1, price2, mail)
        # if a == False:
        #     return "some error"
        return {"Message": "Parsing started! XLSX file will send to your email after parser finish"}