from bs4 import BeautifulSoup
import requests
import time
import redis



def get_content(html, number):
    soup = BeautifulSoup(html, "html.parser")
    #INFO of all cars
    items = soup.find_all("div", class_="a-info-side col-right-list")
    r = redis.Redis(charset="utf-8", decode_responses=True)
    cars = []
    b = 0
    for item in items:
    #     "number" is number less than 20 
    #     which we find after operation
    #     in func "parse"
        b += 1
        if b <= number:

            link = "https://kolesa.kz" + item.find("a", class_="list-link ddl_product_link").get("href")
            link_id = link.split("/")[-1]
            # print(link)
            if link not in r.keys():
                
                s = requests.Session()
                s.get(link, headers=HEADERS)
                time.sleep(1)
                phones = s.get(PHONE_LINK, headers=HEADERS, params={"id": link_id},)
                phone = " ".join(phones.json()['phones'])
                data = {
                    "title" : item.find("a", class_="list-link ddl_product_link").get_text(strip=True),
                    "price" : " ".join(item.find("span", class_="price").get_text(strip=True).split("\xa0")),
                    "city" : item.find("div", class_="list-region").get_text(strip=True),
                    "date" : item.find("span", class_="date").get_text(strip=True),
                    "phones": phone,
                    "link" : link,
                }
                r.hmset(link, data)
            else:
                link_str = str(link)
                data = r.hgetall(link_str)
            cars.append(data)
            # print(r.keys())
    return cars
