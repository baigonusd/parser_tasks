import time
import requests
from bs4 import BeautifulSoup
import csv

HEADERS = {"user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36", "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9"}
HOST = "https://kolesa.kz"
SITE = "https://kolesa.kz/cars/vaz"
FILE = "cars.csv"
CITY = ["almaty", "nur-sultan"]

def get_inform():
    city = input("('almaty' or 'nur-sultan')\nCity: ")
    price1 = input("From <price> tenge: ")
    price2 = input("To <price> tenge: ")

    if price2 > price1:
        if city in CITY:
        # if city in CITY or None:
            url = SITE + f"/{city}/?price[from]={price1}&price[to]={price2}"
            return url
    else:
        return 1


def get_html(url, params=None):
    r = requests.get(url, headers=HEADERS, params=params)
    return r

number_adds = int(input("Number of adds: "))


def check_pages_number(html):
    soup = BeautifulSoup(html, "html.parser")
    number_of_adds = number_adds
    pagination = soup.find("div", class_="finded")
    word_list = pagination.get_text(strip=True).split()
    for word in word_list:
        if word.isnumeric():
            how_much_all_adds = int(word)
    if number_of_adds < how_much_all_adds:
        pages = number_of_adds/20
        return int(pages)+1
    

def get_content(html, number):
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all("div", class_="a-info-side col-right-list")
    cars = []
    b = 0
    for item in items:
        b += 1
        if b <= number:
            cars.append({
                "title" : item.find("a", class_="list-link ddl_product_link").get_text(strip=True),
                "price" : " ".join(item.find("span", class_="price").get_text(strip=True).split("\xa0")),
                "city" : item.find("div", class_="list-region").get_text(strip=True),
                "date" : item.find("span", class_="date").get_text(strip=True),
                "link" : HOST + item.find("a", class_="list-link ddl_product_link").get("href"),
            })
    return cars

def save_file(items, path):
    with open(path, "w", newline="") as file:
        writer = csv.writer(file, delimiter=";")
        writer.writerow(["Марка", "Цена", "Город", "Дата", "Ссылка"])
        for item in items:
            writer.writerow([item["title"], item["price"], item["city"], item["date"], item["link"]])

def parse():
    url = get_inform()
    html = get_html(url)

    if html.status_code == 200:
        cars = []
        pages = check_pages_number(html.text)
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
        print(f"Number of adds {len(cars)}")
    else:
        print("Error - status_code is nor equal to 200")

parse()


# def get_pages_count(html):
#     soup = BeautifulSoup(html, "html.parser")
#     pagination = soup.find_all("div", class_="pager")
#     word_list = pagination[-1].get_text().split()
#     num_list = []
#     for word in word_list:
#         if word.isnumeric():
#             num_list.append(int(word))
#     return num_list[-1]