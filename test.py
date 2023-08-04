import json
import requests
from bs4 import BeautifulSoup


FISI_URL = "https://sistemas.unmsm.edu.pe"


def create_soup():
    page = requests.get(FISI_URL, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup




soup = create_soup()


news_items = soup.find_all("div", class_="mfp_carousel_item")
news_list = [item.find("h4", class_="mfp_carousel_title").find("a") for item in news_items]
first_post = news_list[0]
print(first_post)