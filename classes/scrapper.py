import requests
from bs4 import BeautifulSoup
from classes.news import News


class Scrapper:
    def __init__(self) -> None:
        self.soup: BeautifulSoup = None
        self.main_url: str = "https://sistemas.unmsm.edu.pe"

    def create_soup(self):
        page = requests.get(self.main_url, verify=False)
        self.soup = BeautifulSoup(page.content, "html.parser")

    def remove_spaces_from_tittle(self, title: str) -> str:
        trash_characters = [
            "\n",
            "\r",
            "\t",
        ]
        letters = [letter for letter in title if (letter not in trash_characters)]
        return "".join(letters).strip()

    def get_last_main_news(self) -> News:
        carousel = self.soup.find("div", id="Youdeveloperslider").find(
            "div", class_="elements"
        )
        slides = carousel.find_all("div", class_="slide")
        first_slide = slides[0].find("div", class_="title")
        news_title = self.remove_spaces_from_tittle(first_slide.text)
        news_url = first_slide.find("a")["href"]
        full_url = f"{self.main_url}/{news_url}"
        news = News(news_title, full_url)
        return news

    def check_under_posts(self) -> News:
        news_items = self.soup.find_all("div", class_="mfp_carousel_item")
        news_list = [
            item.find("h4", class_="mfp_carousel_title").find("a")
            for item in news_items
        ]
        first_post = news_list[0]
        news_title = self.remove_spaces_from_tittle(first_post.text)
        news_url = first_post["href"]
        full_url = f"{self.main_url}/{news_url}"
        news = News(news_title, full_url)
        return news
