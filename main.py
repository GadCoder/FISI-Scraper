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


def check_last_update(is_under_news):
    txt_path = "backend/last_update.txt"
    current_time = datetime.now().strftime("%H")
    if not os.path.exists(txt_path):
        with open(txt_path, "w") as f:
            print("Creating txt update time")
            f.write(current_time)
            return True
    with open(txt_path, "r") as f:
        last_update_time = int(f.readline())
        f.close()
    if abs(int(current_time) - last_update_time) > 1:
        if is_under_news:
            with open(txt_path, "w") as f:
                f.write(current_time)
                f.close()
        return True
    else:
        return False


def update_news():
    # Noticias principales
    if check_main_posts():
        new_main_post = get_main_news()
        telegram_bot_send_message(
            f"{get_current_time()}: Nueva noticia principal")
        telegram_bot_send_message(
            f"Título: {new_main_post['newest_post']['title']}")
        telegram_bot_send_message(
            f"Enlace: {new_main_post['newest_post']['url']}")
    elif check_last_update(False):
        telegram_bot_send_message(
            f"{get_current_time()}: No hay noticias principales nuevas",
            isPersonal=True)

    # Noticias secundarias
    if check_under_posts():
        new_under_post = get_under_news()
        telegram_bot_send_message(
            f'{get_current_time()}: Nueva noticia secundaria')
        telegram_bot_send_message(
            f"Título: {new_under_post['newest_post']['title']}")
        telegram_bot_send_message(
            f"Enlace: {new_under_post['newest_post']['url']}")
    elif check_last_update(True):
        telegram_bot_send_message(
            f"{get_current_time()}: No hay noticias principales secundaria",
            isPersonal=True)


def main():
    check_if_jsons_exits()
    update_news()


if __name__ == "__main__":
    main()
