
import requests
import re
import random
from random import choice
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
    
    if event.message.text == "早安":
        image_message = ImageSendMessage(
            original_content_url='https://i.imgur.com/kZD28Qo.gif',
            preview_image_url='https://i.imgur.com/kZD28Qo.gif'
        )
        
        line_bot_api.reply_message(
            event.reply_token, image_message)
                                                        
        return 0
    
    if event.message.text == "午安":
        client = ImgurClient('18f064544f219ac', 'b17f2b3ef24f98c4e3cce9424ef0b1b7173ef642')
        images = client.get_album_images('k7Z38KG')
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message1 = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message2 = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        line_bot_api.reply_message(
            event.reply_token, [image_message1, image_message2])
        
        
                                                        
        return 0
    
    if event.message.text == "晚安":
        client = ImgurClient('18f064544f219ac', 'b17f2b3ef24f98c4e3cce9424ef0b1b7173ef642')
        images = client.get_album_images('k7Z38KG')
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url='https://example.com/item1.jpg',
                        title='this is menu1',
                        text='description1',
                        actions=[
                            PostbackTemplateAction(
                                label='postback1',
                                text='postback text1',
                                data='action=buy&itemid=1'
                            ),
                            MessageTemplateAction(
                                label='message1',
                                text='message text1'
                            ),
                            URITemplateAction(
                                label='uri1',
                                uri='http://example.com/1'
                            )
                        ]
                    ),
                    CarouselColumn(
                        thumbnail_image_url='https://example.com/item2.jpg',
                        title='this is menu2',
                        text='description2',
                        actions=[
                            PostbackTemplateAction(
                                label='postback2',
                                text='postback text2',
                                data='action=buy&itemid=2'
                            ),
                            MessageTemplateAction(
                                label='message2',
                                text='message text2'
                            ),
                            URITemplateAction(
                                label='uri2',
                                uri='http://example.com/2'
                            )
                        ]
                    )
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, message)
    
    
    
    
    
    
    
    
    
    if event.message.text == "Mariona":
        from random import choice
        mottos2 = [1, 2, 3, 4, 5]
        line_bot_api.reply_message(
            event.reply_token, 
                TextSendMessage(text=random.choice(mottos2))
        )
        return 0
    
    
        
 

@app.route('/')

def index():

    return 'Hello World'



import os

if __name__ == "__main__":

    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port)
