import requests
import csv
from tqdm import tqdm
from bs4 import BeautifulSoup

BASE_URL = "https://freelansim.ru/"


def get_html(url):
    response = requests.get(url)
    return response.text


def get_pages(html):
    soup = BeautifulSoup(html, "lxml")
    page = soup.find("div", class_="pagination").find_all("a")[-2].get("href")
    total_page = page.split("=")[1]
    return int(total_page)


def write_csv(dictOfData):
    with open("weblancer.csv", "w") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(('Название', 'Цена', 'Ссылка'))
        for data in dictOfData:
            if data["price"] != []:
                price = data["price"][0]
            else:
                price = "Не указано!"
            writer.writerow((data["title"],
                            price,
                            data["url"]))


def get_data(html):
    soup = BeautifulSoup(html, "lxml")
    article = soup.find_all('article', class_='task task_list')
    dictOfData = []
    for i in article:
        dictOfData.append({"title": i.div.a.text,
                          "price": [price.text.strip() for price in i.aside.find_all('span', class_='count')],
                          "url": BASE_URL + i.div.a["href"]})
    return dictOfData


def main():
    links = []
    total_page = get_pages(get_html(BASE_URL))
    for i in tqdm(range(1, total_page + 1)):
        links.extend(get_data(get_html(BASE_URL + "tasks?page=1")))
    write_csv(links)


if __name__ == "__main__":
    main()
