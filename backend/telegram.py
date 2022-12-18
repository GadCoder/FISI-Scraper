import requests


TOKEN = ""
CHAT_ID = ""
GROUP_CHAT_ID = ""


def telegram_bot_send_message(bot_message, isPersonal=False):
    bot_token = TOKEN
    bot_chatID = CHAT_ID if isPersonal else GROUP_CHAT_ID
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message
    response = requests.get(send_text)
    return response.json()
