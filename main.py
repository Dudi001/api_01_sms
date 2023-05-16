import os
import time

import requests
from dotenv import load_dotenv
from twilio.rest import Client

load_dotenv()

BASE_URL = 'https://api.vk.com/method/users.get'


def get_status(user_id):
    params = {
        'user_ids': user_id,
        'V': os.getenv('API_V'),
        'access_token': os.getenv('ACCESS_TOKEN'),
        'fields': 'online'
    }
    friends_status = requests.post(BASE_URL, params=params)

    return friends_status.json()['response'][0]['online']


def send_sms(sms_text):
    account_sid = os.getenv('TWILIO_ACCOUNT_SID')
    auth_token = os.getenv('TWILIO_AUTH_TOKEN')
    client = Client(account_sid, auth_token)

    message = client.messages.create(
        body='Joing the dark side',
        from_=os.getenv('NUMBER_FROM'),
        media_url=['https://demo.twilio.com/owl.png'],
        to=os.getenv('NUMBER_TO')
    )
    return message.sid


if __name__ == '__main__':
    vk_id = input('Введите id ')
    while True:
        if get_status(vk_id) == 1:
            send_sms(f'{vk_id} сейчас онлайн!')
            break
        time.sleep(5)
