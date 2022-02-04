from fastapi import Depends, APIRouter, HTTPException, status
from typing import Optional
from celery_worker import parsing_celery

router = APIRouter()


@router.get("/celery/", tags=["Parse kolesa.kz's adds"])
def celery_parse(mail, number_adds: int, city: Optional[str] = None, price1: Optional[int] = None, price2: Optional[int] = None):
    if price1 is not None and price2 is not None:
        if price1 > price2:
            return {"Message": "<Price1> can't be more than <price2>"}
        else:
            parsing_celery.delay(mail, number_adds, city, price1, price2)
            return {"Message": f"Hi, {mail}. Parsing started! XLSX file will send to your email after parser finish"}
    parsing_celery.delay(mail, number_adds, city, price1, price2)
    return {"Message": f"Hi, {mail}. Parsing started! XLSX file will send to your email after parser finish"}



# @app.get('/kolesa/', tags=["Adds"])
# def parsing(number_adds: int, city: Optional[str] = None, price1: Optional[int] = None, price2: Optional[int] = None):
#     value = parse(number_adds, city, price1, price2)
#     if value == 1:
#         return {"Message": "<ERROR ON PARSING>"}
#     else: 
#         return value


# @app.get('/kolesa/send/', tags=["Sending email"])
# def email_send(mail):
#     msg = EmailMessage()
#     msg['Subject'] = 'PARSER OF KOLESA'
#     msg['From'] = os.getenv("EMAIL")
#     msg['To'] = mail
#     msg.set_content('LIST OF ADDS')
#     files = ['kolesa.xlsx']
#     for file in files:
#         with open(file, 'rb') as f:
#             file_data = f.read()
#             file_name = f.name

#         msg.add_attachment(file_data, maintype='application', subtype='octet-stream', filename=file_name)

#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#         smtp.login(os.getenv("EMAIL"), os.getenv("PASSWORD"))
#         print('Message sended')
#         smtp.send_message(msg)
#     return {"Message": "Email sended"}