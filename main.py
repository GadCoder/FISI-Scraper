import os
from datetime import datetime
from backend.scrape import check_main_posts, check_under_posts, get_main_news, get_under_news
from backend.telegram import telegram_bot_send_message


def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time


def check_if_jsons_exits():
    if not os.path.exists("backend/main_posts.json"):
        with open("backend/main_posts.json", 'w') as f:
            print("Creando main_posts.json")
    if not os.path.exists("backend/under_posts.json"):
        with open("backend/under_posts.json", 'w') as f:
            print("Creando under_posts.json")


def update_news():
    if check_under_posts():
        new_under_post = get_under_news()
        telegram_bot_send_message(f'{get_current_time()}: Nueva noticia principal')
        telegram_bot_send_message(f"Título: {new_under_post['newest_post']['title']}")
        telegram_bot_send_message(f"Enlace: {new_under_post['newest_post']['url']}")
    else:
        telegram_bot_send_message(f"{get_current_time()}: No hay noticias principales nuevas")

    if check_main_posts():
        new_main_post = get_main_news()
        telegram_bot_send_message(f"{get_current_time()}: Nueva noticia secundaria")
        telegram_bot_send_message(f"Título: {new_main_post['newest_post']['title']}")
        telegram_bot_send_message(f"Enlace: {new_main_post['newest_post']['url']}")
    else:
        telegram_bot_send_message(f"{get_current_time()}: No hay noticias secundarias nuevas")


def main():
    check_if_jsons_exits()
    update_news()


if __name__ == "__main__":
    main()
