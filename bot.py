import telegram
import requests
import logging
import os
from time import sleep

from dotenv import load_dotenv


def main():
    url = 'https://dvmn.org/api/long_polling/'
    headers = {'Authorization': f'Token {os.environ["DVMN_TOKEN"]}'}
    timestamp = ''
    params = dict()
    tg_token = os.environ['TG_TOKEN']
    chat_id = os.environ['TG_CHAT_ID']
    bot = telegram.Bot(token=tg_token)
    while True:
        try:
            if timestamp:
                params = {'timestamp': timestamp}
            response = requests.get(url, headers=headers, params=params)
            dvmn_answer = response.json()
            if dvmn_answer['status'] == 'timeout':
                timestamp = dvmn_answer['timestamp_to_request']
            else:
                checking_result = dvmn_answer['new_attempts'][0]
                if checking_result['is_negative']:
                    result = 'К сожалению, в работе нашлись ошибки:('
                else:
                    result = 'Преподавателю всё понравилось!'
                text = f'У вас проверили работу "{checking_result["lesson_title"]}"!\n{result}\nСсылка: {checking_result["lesson_url"]}'
                bot.send_message(text=text, chat_id=chat_id)            
        except requests.exceptions.ReadTimeout:
            logging.warning('Превышено время ожидания! Делаю повторный запрос')
        except requests.exceptions.ConnectionError:
            logging.error('Нет подключения к сети!')
            sleep(6)


if __name__ == '__main__':
    load_dotenv()
    main()
