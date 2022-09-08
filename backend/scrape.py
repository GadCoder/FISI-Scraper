
import json
import requests
from bs4 import BeautifulSoup

fisi_url = "https://sistemas.unmsm.edu.pe/site/"


def remove_spaces_from_tittle(title):
    trash_characters = ['\n', '\r', '\t', ]
    letters = [letter for letter in title if (letter not in trash_characters)]
    while letters[0] == " ":
        letters.pop(0)
    return ''.join(letters)


def read_json(path):
    return json.load(open(path))


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


def check_under_posts():
    page = requests.get(fisi_url, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")
    news_items = soup.find_all("div", class_="mfp_carousel_item")
    news_list = [item.find("h4", class_="mfp_carousel_title").find("a") for item in news_items]
    first_post = news_list[0]
    title = remove_spaces_from_tittle(first_post.text)
    url = fisi_url + first_post['href']
    first_post_json = transform_post_to_json(title, url)
    print(f"First post on under: {first_post_json}")
    check_last_post("backend/under_posts.json", first_post_json)


def check_main_posts():
    page = requests.get(fisi_url, verify=False)
    soup = BeautifulSoup(page.content, "html.parser")
    carousel = soup.find("div", id="Youdeveloperslider").find("div", class_="elements")
    slides = carousel.find_all("div", class_="slide")
    first_slide = slides[0].find("div", class_="title")
    title = remove_spaces_from_tittle(first_slide.text)
    url = fisi_url + first_slide.find("a")['href']
    first_slide_json = transform_post_to_json(title, url)
    print(f"First slide on main: {first_slide_json}")
    check_last_post("backend/main_posts.json", first_slide_json)


def get_main_news(type):
    main_posts = read_json("backend/main_posts.json")
    return main_posts[type],

def get_under_news(type):
    under_posts = read_json("backend/under_posts.json")
    return under_posts[type],


def get_news(type):
    main_posts = read_json("backend/main_posts.json")
    under_posts = read_json("backend/under_posts.json")

    return {
        "main_posts": main_posts[type],
        "under_posts": under_posts[type]
    }
