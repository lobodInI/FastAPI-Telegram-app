import requests


def send_message(
        bot_token: str,
        chat_id: str,
        message: str
) -> requests.Response:
    api_url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": message,
    }
    response = requests.post(api_url, data=data)

    return response
