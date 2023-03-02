import json
import requests
from bs4 import BeautifulSoup

FISI_URL = "https://sistemas.unmsm.edu.pe"
FILES_PATH = "/fisi-scrapper/"

def remove_spaces_from_tittle(title):
    trash_characters = ['\n', '\r', '\t', ]
    letters = [letter for letter in title if (letter not in trash_characters)]
    while letters[0] == " ":
        letters.pop(0)
    return ''.join(letters)


def read_json(path):
    with open(path) as json_file:
        return json.load(json_file)


def write_json(path, newest_post, last_post):
    new_json = {
        "newest_post": newest_post,
        "last_post": last_post
    }
    with open(path, "w") as file:
        json.dump(new_json, file)


def transform_post_to_json(new_title, new_url):
    return {"title": new_title, "url": new_url}


def check_last_post(json_path, post):
    post_json = read_json(json_path)
    last_post = post_json["newest_post"]
    if not last_post:
        write_json(json_path, post, post)
        return True
    else:
        if last_post['title'] == post['title']:
            print(f"No hay noticias nuevas en {json_path}")
            return False
        else:
            print("Noticia nueva, guardando")
            write_json(json_path, post, last_post)
            return True


def create_soup():
    page = requests.get(FISI_URL, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


def check_under_posts():
    soup = create_soup()
    news_items = soup.find_all("div", class_="mfp_carousel_item")
    news_list = [item.find("h4", class_="mfp_carousel_title").find("a") for item in news_items]
    first_post = news_list[0]
    title = remove_spaces_from_tittle(first_post.text)
    url = FISI_URL + first_post['href']
    first_post_json = transform_post_to_json(title, url)
    return check_last_post(FILES_PATH + "under_posts.json", first_post_json)


def check_main_posts():
    soup = create_soup()
    carousel = soup.find("div", id="Youdeveloperslider").find("div", class_="elements")
    slides = carousel.find_all("div", class_="slide")
    first_slide = slides[0].find("div", class_="title")
    title = remove_spaces_from_tittle(first_slide.text)
    url = FISI_URL + first_slide.find("a")['href']
    first_slide_json = transform_post_to_json(title, url)
    return check_last_post(FILES_PATH + "main_posts.json", first_slide_json)

def get_main_news():
    return read_json(FILES_PATH + "main_posts.json")


def get_under_news():
    return read_json(FILES_PATH + "under_posts.json")


