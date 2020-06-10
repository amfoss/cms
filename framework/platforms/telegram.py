import telegram
from framework.platforms.userPlatform import UserPlatform
from datetime import date
from utilities.models import Token


class Telegram(UserPlatform):

    def __init__(self, telegram_id):
        self.telegram_id = telegram_id

    def removeUser(self):
        TELEGRAM_BOT_TOKEN = Token.objects.values().get(key='TELEGRAM_BOT_TOKEN')['value']
        TELEGRAM_CHAT_ID = Token.objects.values().get(key='TELEGRAM_CHAT_ID')['value']
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        try:
            bot.kick_chat_member(chat_id=TELEGRAM_CHAT_ID, user_id=self.telegram_id)
            bot.unban_chat_member(
                chat_id=TELEGRAM_CHAT_ID,
                user_id=self.telegram_id
            )
        except:
            pass

    def addUser(self):
        TELEGRAM_BOT_TOKEN = Token.objects.values().get(key='TELEGRAM_BOT_TOKEN')['value']
        TELEGRAM_CHAT_ID = Token.objects.values().get(key='TELEGRAM_CHAT_ID')['value']
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        user = bot.get_chat(chat_id=self.telegram_id)
        message = 'Hi Admin, \n\n'
        message += 'Please add @' + user['username'] + ' to amFOSS-2019 Telegram Group, \n\n'
        message += '<i>This is an automatically generated request powered by the CMS on </i>' \
                   + '<i>' + date.today().strftime('%d %B %Y') + '.</i>'
        admins = bot.get_chat_administrators(chat_id=TELEGRAM_CHAT_ID)
        for admin in admins:
            if admin['status'] == "creator":
                bot.send_message(
                    chat_id=admin['user']['id'],
                    text=message,
                    parse_mode=telegram.ParseMode.HTML
                )

    def checkIfUserExists(self):
        TELEGRAM_BOT_TOKEN = Token.objects.values().get(key='TELEGRAM_BOT_TOKEN')['value']
        TELEGRAM_CHAT_ID = Token.objects.values().get(key='TELEGRAM_CHAT_ID')['value']
        bot = telegram.Bot(token=TELEGRAM_BOT_TOKEN)
        try:
            status = bot.get_chat_member(chat_id=TELEGRAM_CHAT_ID, user_id=self.telegram_id).status
            if status == "left" or status == "kicked":
                return False
            else:
                return True
        except:
            return False
