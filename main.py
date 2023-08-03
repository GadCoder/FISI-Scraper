import os
import shutil
import random
from datetime import datetime
from backend.scrape import check_main_posts, check_under_posts, get_main_news, get_under_news
from backend.telegram import telegram_bot_send_message


FILES_PATH = "/fisi-scrapper/"


def get_current_time():
    now = datetime.now()
    current_time = now.strftime("%H:%M")
    return current_time


def get_animal_emoji():
    emojis = ["🐰", "🐭", "🐱", "🐶", "🦊", "🐹", "🐻", "🐼", "🐸", "🐵", "🐷", "🐧", "🐨", "🦦", "🦔"]
    return random.choice(emojis)

def is_daytime():
    now = datetime.now()
    current_time = int(now.strftime("%H"))
    if current_time >= 0 and current_time < 6:
        return False    
    return True


def check_if_jsons_exits():
    jsons = ["main_posts.json", "under_posts.json"]
    for json_file in jsons:
        if not os.path.exists(FILES_PATH + json_file):
            shutil.copyfile(f"backend/{json_file}", FILES_PATH + json_file)
        print(f"Creando {json_file}")


def check_if_txt_time_exists():
    txt_path = FILES_PATH + "last_update.txt"
    if os.path.exists(txt_path):
        return
    current_time = datetime.now().strftime("%H")
    with open(txt_path, "w") as f:
        print("Creating txt update time")
        f.write(current_time)
        f.close()


def check_if_files_exists():
    check_if_txt_time_exists()
    check_if_jsons_exits()
    

def read_last_hour(txt_path):
    with open(txt_path, "r") as f:
        last_update_time = int(f.readline())
        f.close()
        return last_update_time


def write_last_update_hour(txt_path, current_time):
    txt_path = FILES_PATH + "last_update.txt"
    with open(txt_path, "w") as f:
            f.write(current_time)
            f.close()


def check_last_update(is_under_news):
    txt_path = FILES_PATH + "last_update.txt"
    current_time = datetime.now().strftime("%H")
    last_update_hour = read_last_hour(txt_path)

    if abs(int(current_time) - last_update_hour) > 1:
        if is_under_news:
            write_last_update_hour(txt_path, current_time)
        return True
    return False


def update_news():
    # Noticias principales
    if check_main_posts():
        new_main_post = get_main_news()
        telegram_bot_send_message(f"{get_current_time()}: Nueva noticia principal")
        telegram_bot_send_message(
            f"*{new_main_post['newest_post']['title']}* {get_animal_emoji()}\n🔗*Enlace*: {new_main_post['newest_post']['url']}"
            )
    elif check_last_update(False):
        telegram_bot_send_message(f"{get_current_time()}: No hay noticias principales nuevas ☹️", isPersonal=True)

    # Noticias secundarias
    if check_under_posts():
        new_under_post = get_under_news()
        telegram_bot_send_message(f"{get_current_time()}: Nueva noticia secundaria")
        telegram_bot_send_message(
            f"*{new_under_post['newest_post']['title']}* {get_animal_emoji()}\n🔗*Enlace*: {new_under_post['newest_post']['url']}"
            )
    elif check_last_update(True):
        telegram_bot_send_message(f"{get_current_time()}: No hay noticias principales secundarias ☹️", isPersonal=True)


def main():
    check_if_jsons_exits()
    if is_daytime():
        update_news()


if __name__ == "__main__":
    main()
