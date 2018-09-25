import requests
from bs4 import BeautifulSoup
import csv
import sys
from time import sleep

BASE_URL = "https://www.avito.ru/moskva/noutbuki"

def get_html(url):
    res = requests.get(url)
    return res.text


def get_total_pages(html):
    soup = BeautifulSoup(html, "lxml")
    pages = soup.find("div", class_="pagination-pages").find_all("a", class_="pagination-page")[-1].get("href")
    total_pages = pages.split("=")[1].split("&")[0]
    return int(total_pages)


def write_csv(datadata):
    with open("avito.csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.write(('Название', 'Описание', 'Ссылка'))
        for data in datadata:
            writer.writerows((str(data["title"]),
                              str(data["price"]),
                              str(data["url"])))

def get_page_data(html):
    soup = BeautifulSoup(html, "lxml")
    ads = soup.find("div", class_="catalog-list").find_all("div", class_="item_table")
    data = []
    for ad in ads:
        title = ad.find("div", class_="description").find("h3").text.strip()
        url = "https://www.avito.ru" + ad.find("div", class_="description").find("h3").find("a").get("href")
        price = ad.find("div", class_="about").find("span", class_="price").text.strip()

        data.append({"title": title,
                "price": price,
                "url": url})

    return data


def main():
    ad = []

    page_num = 15
    page = 1
    for i in range(page, page_num):
        sys.stdout.write("\rПарсинг {} ".format(str((page / page_num) * 100)))
        sleep(0.15)
        ad.extend(get_page_data(get_html(BASE_URL + "?p={}&q=lenovo".format(str(i)))))

    write_csv(ad)

if __name__ == "__main__":
    main()
