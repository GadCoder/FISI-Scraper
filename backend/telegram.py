import requests
import random


TOKEN = "5907691902:AAEzElCtv5ooMEugKofP7k_JIUDvkv4OIe4"
CHAT_ID = "1446179367"
GROUP_CHAT_ID = "-1001800110316"


def get_animal_emoji():
    emojis = [
        "🐰",
        "🐭",
        "🐱",
        "🐶",
        "🦊",
        "🐹",
        "🐻",
        "🐼",
        "🐸",
        "🐵",
        "🐷",
        "🐧",
        "🐨",
    ]
    return random.choice(emojis)


def telegram_bot_send_message(bot_message, isPersonal=False):
    bot_token = TOKEN
    bot_chatID = CHAT_ID if isPersonal else GROUP_CHAT_ID
    send_text = (
        "https://api.telegram.org/bot"
        + bot_token
        + "/sendMessage?chat_id="
        + bot_chatID
        + "&parse_mode=Markdown&text="
        + bot_message
    )
    response = requests.get(send_text)
    return response.json()
