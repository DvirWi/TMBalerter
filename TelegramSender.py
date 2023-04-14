import telebot

class TelegramSender(object):
    def __init__(self, api_token, chat_id):
        self.api_token = api_token
        self.chat_id = chat_id

    def send_message(self, msg):
        """
        Send a message to a telegram user or group specified on chatId
        chat_id must be a number!
        """
        bot = telebot.TeleBot(token=self.api_token)
        bot.send_message(chat_id=self.chat_id, text=msg)