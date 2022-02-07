from parse_try import parse
from celery import Celery
from email.message import EmailMessage
from celery.utils.log import get_task_logger
import smtplib
import os
from dotenv import load_dotenv, find_dotenv
load_dotenv(dotenv_path=find_dotenv())

import time

BACKEND_URL = 'redis://localhost:6379/3'
celery = Celery('tasks', broker = 'redis://localhost:6379/1', backend = BACKEND_URL)
default_config = 'configs.celeryconfig'
celery.config_from_object(default_config)
# Create logger - enable to display messages on task logger
celery_log = get_task_logger(__name__)


@celery.task
def checking():
    for i in range(0, 20):
        time.sleep(1)
        print(f"Sleep number = {i}") 
    return "Finish sleeping"

@celery.task
def parsing_celery(mail, number_adds, city, price1, price2):
    value = parse(number_adds, city, price1, price2)
    mail1 = mail
    if value == 1:
        return "Message : <ERROR ON PARSING>"
    else:
        email.delay(mail1) 
        celery_log.info("Your parser has finished!")
        return value

@celery.task
def email(mail):
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
