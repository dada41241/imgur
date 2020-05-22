
import requests
import re
import random
import configparser
from bs4 import BeautifulSoup
from imgurpython import ImgurClient

from flask import Flask, request, abort



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

# Channel Access Token

line_bot_api = LineBotApi('P7V+AiwPyztvIPr8EK+AlVWacCTa5FQWPNJs/0giVGt+0o985Srw35KwIYnIEPjqKgCVZomwbrcFt63vCUeUH9EPi2UwxqQ9XWraylX3/YHd/BPa/8W0wwZm36+XQ4LVuWAKhOopLbSrhHeprh9N7gdB04t89/1O/w1cDnyilFU=')

# Channel Secret

handler = WebhookHandler('59e352af8b15a1efddee622ce3c31d81')

client = ImgurClient('18f064544f219ac', 'b17f2b3ef24f98c4e3cce9424ef0b1b7173ef642')
album_id = 'mKFXEqB'



# 監聽所有來自 /callback 的 Post Request

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

        abort(400)

    return 'OK'



# 處理訊息

@handler.add(MessageEvent, message=TextMessage)
    
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)
    
    if event.message.text == "imgur":
        client = ImgurClient('18f064544f219ac', 'b17f2b3ef24f98c4e3cce9424ef0b1b7173ef642')
        images = client.get_album_images('mKFXEqB')
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, [
                image_message,
                TextSendMessage(text="早安你好!!")
            ])                               
        return 0
    
    if event.message.text == "嘿嘿":
        target_url = 'https://www.youtube.com/playlist?list=FLc2pCs0Dog_Nw7oQYFlSxpg'
        rs = requests.session()
        res = rs.get(target_url, verify=False)
        soup = BeautifulSoup(res.text, 'html.parser')
        seqs = ['https://www.youtube.com{}'.format(data.find('a')['href']) for data in soup.select('.yt-lockup-title')]
        line_bot_api.reply_message(
            event.reply_token, [
                TextSendMessage(text=seqs[random.randint(0, len(seqs) - 1)]),
                TextSendMessage(text=seqs[random.randint(0, len(seqs) - 1)])
            ])
        return 0

@app.route('/')

def index():

    return 'Hello World'



import os

if __name__ == "__main__":

    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port)
