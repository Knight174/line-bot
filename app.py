from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('6yap6XSlJj162ccjFDG2HwdZET4rAqG18yJyyJbh7nuJc4y8PMP39ZzmRqCc6hVYe6uBpk5yzah4dUgIqZDwZLq+yT0L0auRoYOXctw+L19ehcVSdiqt1+BUNluGoC1ubMvWKNJLZ8L+w3eXBZqOcwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('705eac1cd70377db3f0d035c1250ac88')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()
