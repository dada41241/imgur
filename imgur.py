import requests
import re
import random
import configparser
from bs4 import BeautifulSoup
from flask import Flask, request, abort
from imgurpython import ImgurClient

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)
config = configparser.ConfigParser()
config.read("config.ini")

line_bot_api = LineBotApi(config['line_bot']['P7V+AiwPyztvIPr8EK+AlVWacCTa5FQWPNJs/0giVGt+0o985Srw35KwIYnIEPjqKgCVZomwbrcFt63vCUeUH9EPi2UwxqQ9XWraylX3/YHd/BPa/8W0wwZm36+XQ4LVuWAKhOopLbSrhHeprh9N7gdB04t89/1O/w1cDnyilFU='])
handler = WebhookHandler(config['line_bot']['59e352af8b15a1efddee622ce3c31d81'])
client_id = config['imgur_api']['18f064544f219ac']
client_secret = config['imgur_api']['c33fdd2c822d20be16ea2eb691242616f4759733']
album_id = config['imgur_api']['X0QL4']


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    # print("body:",body)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'ok'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)

    if event.message.text == "早安":
        client = ImgurClient(client_id, client_secret)
        images = client.get_album_images(album_id)
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, image_message)
        return 0


if __name__ == "__main__":
    app.run()