import time
import requests
from bs4 import BeautifulSoup
import csv
import smtplib
from dotenv import load_dotenv, find_dotenv
import os
from email.message import EmailMessage
import xlsxwriter
import pandas as pd
import xlrd
load_dotenv(dotenv_path=find_dotenv())





HEADERS = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9", "x-requested-with": "XMLHttpRequest"}
HOST = "https://kolesa.kz"
SITE = "https://kolesa.kz/cars"
FILE = "cars.csv"
CITY = ["almaty", "nur-sultan"]
PHONE_LINK = "https://kolesa.kz/a/ajaxPhones"


# INPUT DETAILS > CREATING URL
# def get_inform():
#     city = input("('almaty' or 'nur-sultan')\nCity: ")
#     price1 = input("From <price> tenge: ")
#     price2 = input("To <price> tenge: ")

#     if price2 > price1:
#         if city in CITY:
#         # if city in CITY or None:
#             url = SITE + f"/{city}/?price[from]={price1}&price[to]={price2}"
#             return url
#         else: 
#             return "city"
#     else:
#         return "price"


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

# number_adds = int(input("Number of adds: "))


#How many pages we need to open
def check_pages_number(html, number_adds):
    soup = BeautifulSoup(html, "html.parser")
    number_of_adds = number_adds
    pagination = soup.find("div", class_="finded")
    word_list = pagination.get_text(strip=True).split()
    sum = ""
    for word in word_list:
        if word.isnumeric():
            sum = sum + word
    how_much_all_adds = int(sum)
    if number_of_adds < how_much_all_adds:
        #20 adds on 1 page
        pages = number_of_adds/20
        if number_of_adds%20 == 0:
            return int(pages)
        else:
            return int(pages)+1
    else: 
        return "number"


def get_content(html, number):
    soup = BeautifulSoup(html, "html.parser")
    #INFO of all cars
    items = soup.find_all("div", class_="a-info-side col-right-list")


    cars = []
    b = 0
    for item in items:
        # "number" is number less than 20 
        # which we find after operation
        # in func "parse"
        b += 1
        if b <= number:
            link = HOST + item.find("a", class_="list-link ddl_product_link").get("href")
            link_id = link.split("/")[-1]
            s = requests.Session()
            s.get(link, headers=HEADERS)
            phones = s.get(PHONE_LINK, headers=HEADERS, params={"id": link_id},)
            phone = " ".join(phones.json()['phones'])
            cars.append({
                "title" : item.find("a", class_="list-link ddl_product_link").get_text(strip=True),
                "price" : " ".join(item.find("span", class_="price").get_text(strip=True).split("\xa0")),
                "city" : item.find("div", class_="list-region").get_text(strip=True),
                "date" : item.find("span", class_="date").get_text(strip=True),
                "phones": phone,
                "link" : link,
            })
    return cars


def save_file(items, path):
    df = pd.DataFrame()
    titles = []
    prices = []
    cities = []
    dates = []
    telephones = []
    links = []
    for i in range(0, len(items)):
        titles.append(items[i]["title"])
        prices.append(items[i]["price"])
        cities.append(items[i]["city"])
        dates.append(items[i]["date"])
        telephones.append(items[i]["phones"])
        links.append(items[i]["link"])


    df["Марка"] = titles
    df["Цена"] = prices
    df["Город"] = cities
    df["Дата"] = dates
    df["Телефон"] = telephones
    df["Ссылка"] = links

    writer = pd.ExcelWriter("./kolesa.xlsx", engine="xlsxwriter")
    df.to_excel(writer, sheet_name="List1", index=False)

    writer.sheets["List1"].set_column("A:A", 30)
    writer.sheets["List1"].set_column("B:B", 15)
    writer.sheets["List1"].set_column("C:C", 20)
    writer.sheets["List1"].set_column("D:D", 10)
    writer.sheets["List1"].set_column("E:E", 35)
    writer.sheets["List1"].set_column("F:F", 35)

    writer.save()

def parse(number_adds, city, price1, price2):
    url = SITE + f"/{city}/?price[from]={price1}&price[to]={price2}"
    html = get_html(url)
    if html.status_code == 200:
        cars = []
        pages = check_pages_number(html.text, number_adds)
        if pages == "number":
            print("\n<ERROR>\nNumber of adds is more than all adds on the site")
            return 1
        # finding "number"
        a = number_adds
        for i in range(1, pages+1):
            if a > 20: 
                a -= 20


        for page in range (1, pages+1):
            print(f"Parsing of page {page} from {pages} started...")
            html = get_html(url, params={"page": page})
            time.sleep(1)
            if page < pages:
                cars.extend(get_content(html.text, 20))
            elif page == pages:
                cars.extend(get_content(html.text, a))
        save_file(cars, FILE)
        return f"{len(cars)} adds were created"
    else:
        print("Error - status_code is nor equal to 200")
        return 1

# if parse()==1:
#     print("<ERROR>")
# else:
#     msg = EmailMessage()
#     msg['Subject'] = 'PARSER OF KOLESA'
#     msg['From'] = os.getenv("EMAIL")
#     msg['To'] = os.getenv("RECEIVER")
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

