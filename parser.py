import requests
from bs4 import BeautifulSoup
import csv

BASE_URL = "https://www.weblancer.net/jobs/"    

def get_html(url):
    res = requests.get(url)
    return res.text


def parse(html):
    soup = BeautifulSoup(html, "lxml")
    all_content = soup.find("div", class_="cols_table")
    title_ad = all_content.find_all("h2") 
    print(title_ad)









def main():
    parse(get_html("https://www.weblancer.net/jobs/"))

if __name__ == "__main__":
    main()
