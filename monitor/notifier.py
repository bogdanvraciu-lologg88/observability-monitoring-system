import requests


def send_telegram_alert(message, config):
    token = config["alerting"]["telegram_bot_token"]
    chat_id = config["alerting"]["telegram_chat_id"]

    url = f"https://api.telegram.org/bot8687331385:AAGFznGcYxBE8k8Z3r1T0FeI4aj-u4xncUU/sendMessage"

    payload = {
        "chat_id": str(chat_id),
        "text": str(message)
    }

    try:
        response = requests.post(url, json=payload)

    except Exception as e:
        print(f"Telegram error: {e}")