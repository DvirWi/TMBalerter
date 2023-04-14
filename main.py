from TMBAvalabilityChecker import TMBAvalabilityChecker
from TelegramSender import TelegramSender
from Refugee import Refugee
from datetime import datetime
import argparse
import logging

DAYS_RANGE = 0
NUM_OF_GUESTS = 2

REFUGEES_TO_CHECK = [   
                        Refugee(name='Cabane du Combal', refugee_id=36471, date=datetime(2023,8,31)),
                        Refugee(name='Refuge Le Peuty', refugee_id=32405, date=datetime(2023,9,5))
                    ]

#token that can be generated talking with @BotFather on telegram
API_TOKEN = '6100544234:AAFQR983PK7BwFrfAEWmJ6YxsiZXd1PPQx0'
# GET_CHAT_ID_URL = f'https://api.telegram.org/bot{API_TOKEN}/getUpdates'
# Look for the chat.id object
CHAT_ID = -1001970603229
DATETIME_FORMAT = '%d/%m/%y'
DEFAULT_LOG_FILE = r'C:\Users\Dvir\Documents\TMB\TMB.log'


def format_logger(log_file: str):
    logging.basicConfig(filename=log_file, filemode='a', format='%(asctime)s | %(levelname)s | %(message)s', level=logging.INFO)
    return logging.getLogger('TMB')


def init_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l','--log-file', type=str, default=DEFAULT_LOG_FILE, help='log file path')
    return parser.parse_args()


def main():
    args = init_args()
    logger = format_logger(args.log_file)
    telegram_sender = TelegramSender(API_TOKEN, CHAT_ID)
    for refugee in REFUGEES_TO_CHECK:
        try:
            avaliable_dates = TMBAvalabilityChecker(refugee.id, refugee.date, NUM_OF_GUESTS, DAYS_RANGE).check()
            if not avaliable_dates:
                logger.info(f'{refugee.name} is fully booked on {refugee.date.strftime(DATETIME_FORMAT)}{f" (+-{DAYS_RANGE} days)" if DAYS_RANGE else ""}')
            else:
                for date in avaliable_dates:
                    logger.warning(f'{refugee.name} is avaliable on {refugee.date.strftime(DATETIME_FORMAT)}')
                    try:
                        telegram_sender.send_message(f'{refugee.name} is avaliable on {refugee.date.strftime(DATETIME_FORMAT)}')
                    except Exception as e:
                        logger.error(f'Failed to send telegram message, Traceback: {e}')
        except Exception as e:
            logger.error(f'Failed to check avalibility for {refugee.name} on {refugee.date.strftime(DATETIME_FORMAT)}, Traceback: {e}')

if __name__ == '__main__':
    main()
