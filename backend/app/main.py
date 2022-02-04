from fastapi import FastAPI
from configs.config import settings
from dotenv import load_dotenv, find_dotenv
from routers import parsers_back, parsers_front


load_dotenv(dotenv_path=find_dotenv())

app = FastAPI(
    title=settings.TITLE,
    description=settings.DESCRIPTION,
    contact=settings.CONTACT,
    openapi_tags=settings.TAGS
)

app.include_router(parsers_back.router)
app.include_router(parsers_front.router)

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


# @app.get("/celery/", tags=["Parse kolesa.kz's adds"])
# def celery_parse(mail, number_adds: int, city: Optional[str] = None, price1: Optional[int] = None, price2: Optional[int] = None):
#     if price1 is not None and price2 is not None:
#         if price1 > price2:
#             return {"Message": "<Price1> can't be more than <price2>"}
#     else:
#         asyncresult = parsing_celery.delay(mail, number_adds, city, price1, price2)
#         # if a == False:
#         #     return "some error"
#         return {"Message": f"Hi, {mail}. Parsing started! XLSX file will send to your email after parser finish"}


