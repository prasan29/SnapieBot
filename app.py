import re
from flask import Flask, request
import telegram
from telebot.credentials import bot_token, bot_user_name, URL

global bot
global TOKEN

TOKEN = bot_token
bot = telegram.Bot(token=TOKEN)

app = Flask("bot_server")


@app.route('/{}'.format(TOKEN), methods=['POST'])
def respond():

    # retrieve the message in JSON and then transform it to Telegram object
    update = telegram.Update.de_json(request.get_json(force=True), bot)

    chat_id = update.message.chat.id
    msg_id = update.message.message_id

    # Telegram understands UTF-8, so encode text for unicode compatibility
    text = update.message.text.encode('utf-8').decode()

    print('Message: ', text)

    if text == "/start":
        bot_welcome = """
        - I am SnapieBot!
        - I am Prasanna's virtual manager. 
        - I am handling all queries and business requirements about Prasanna.
        """

        bot.sendMessage(chat_id=chat_id, text=bot_welcome,
                        reply_to_message_id=msg_id)
    else:
        try:
            # clear the message we got from any non alphabets
            text = re.sub(r"\W", "_", text)
            url = "https://api.adorable.io/avatars/285/{}.png".format(
                text.strip())
            bot.sendPhoto(chat_id=chat_id, photo=url,
                          reply_to_message_id=msg_id)
        except Exception:
            bot.sendMessage(
                chat_id=chat_id,
                text="There is some prblem in finding what you are looking for.",
                reply_to_message_id=msg_id)

    return 'Okay'


@app.route('/setwebhook', methods=['GET', 'POST'])
def set_webhoot():
    # we use the bot object to link the bot to our app which live
    # in the link provided by URL
    s = bot.setWebhook('{URL}{HOOK}'.format(URL=URL, HOOK=TOKEN))

    if s:
        return 'Success: WebHook setup successful.'
    else:
        return 'Failure: WebHook setup failed!'


@app.route('/')
def index():
    return '.'


if __name__ == '__main__':
    # note the threaded arg which allow
    # your app to have more than one thread
    app.run(threaded=True)
