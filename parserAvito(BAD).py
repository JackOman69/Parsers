import requests
from bs4 import BeautifulSoup
import csv


def get_html(url):
    res = requests.get(url)
    return res.text


def get_total_pages(html):
    soup = BeautifulSoup(html, "lxml")
    pages = soup.find("div", class_="pagination-pages").find_all("a", class_="pagination-page")[-1].get("href")
    total_pages = pages.split("=")[1].split("&")[0]
    return int(total_pages)


def write_csv(data):
    with open("avito.csv", "a", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows((str(data["title"]),
                          str(data["price"]),
                          str(data["metro"]),
                          str(data["url"])))

def get_page_data(html):
    soup = BeautifulSoup(html, "lxml")
    ads = soup.find("div", class_="catalog-list").find_all("div", class_="item_table")
    for ad in ads:
        try:
            title = ad.find("div", class_="description").find("h3").text.strip()
        except AttributeError:
            title = ""
        try:
            url = "https://www.avito.ru" + ad.find("div", class_="description").find("h3").find("a").get("href")
        except AttributeError:
            url = ""
        try:
            price = ad.find("div", class_="about").find("span", class_="price").text.strip()
            # total_price = price.split(" ", maxsplit=2)[0] + price.split(" ", maxsplit=2)[1] + " руб"
        except AttributeError:
            price = ""
        try:
            metro = ad.find("div", class_="data").find_all("p")[-1].text.strip()
            # total_metro = ad.find("div", class_="data").find_all("p")[-1].text.split(
            #   "\xa0")[0] + ad.find("div", class_="data").find_all("p")[-1].text.split("\xa0")[1]
        except AttributeError:
            metro = ""
        data = {"title": title,
                "price": price,
                "metro": metro,
                "url": url}
        write_csv(data)


def main():
    url = "https://www.avito.ru/moskva/noutbuki?p=1&q=lenovo"
    BASE_URL = "https://www.avito.ru/moskva/noutbuki?"
    page_part = "p="
    query_part = "&q=lenovo"
    # total_pages = get_total_pages(get_html(url))

    for i in range(1, 3):
        url_gen = BASE_URL + page_part + str(i) + query_part
        # print(url_gen)
        html = get_html(url_gen)
        get_page_data(html)


if __name__ == "__main__":
    main()
