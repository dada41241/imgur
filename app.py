import requests
import re
import random
from random import choice
import csv
import urllib3

urllib3.disable_warnings()

import gspread
import random
from oauth2client.service_account import ServiceAccountCredentials
from pprint import pprint

scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]

creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)

client = gspread.authorize(creds)

sheet = client.open("mottomorning").sheet1
sheet_早安哲學=client.open("mottomorning").sheet2
data = sheet.get_all_records()

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

line_bot_api = LineBotApi(
    'P7V+AiwPyztvIPr8EK+AlVWacCTa5FQWPNJs/0giVGt+0o985Srw35KwIYnIEPjqKgCVZomwbrcFt63vCUeUH9EPi2UwxqQ9XWraylX3/YHd/BPa/8W0wwZm36+XQ4LVuWAKhOopLbSrhHeprh9N7gdB04t89/1O/w1cDnyilFU=')

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


def ettoday():
    target_url = 'https://www.ettoday.net/news/realtime-hot.htm'
    print('Start parsing ptt hot....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = ""
    news_all = soup.select('div.part_pictxt_3 div.piece.clearfix h3 a')
    for news in news_all[0:10]:
        title = news.text
        link = news['href']
        content += '{}\n{}\n\n'.format(title, link)
    return content


def test_news():
    target_url = 'https://www.ettoday.net/news/realtime-hot.htm'
    print('Start parsing ptt hot....')
    rs = requests.session()
    res = rs.get(target_url, verify=False)
    soup = BeautifulSoup(res.text, 'html.parser')
    content = []
    for data in soup.select('div.part_pictxt_3 div.piece.clearfix h3 a'):
        title = data.text
        link = data['href']
        news = '{}\n{}\n\n'.format(title, link)
        content.append(news)
    return content


# 處理訊息

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    print("event.reply_token:", event.reply_token)
    print("event.message.text:", event.message.text)

    if event.message.text == "早安":
        client = ImgurClient('18f064544f219ac', 'b17f2b3ef24f98c4e3cce9424ef0b1b7173ef642')
        images = client.get_album_images('qpPMzY9')
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message2 = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message3 = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )

        早安 = random.choice(sheet.col_values(1))
        標點1 = random.choice(sheet.col_values(2))
        祝福 = random.choice(sheet.col_values(3))
        標點2 = random.choice(sheet.col_values(4))
        分享 = random.choice(sheet.col_values(5))
        標點3 = random.choice(sheet.col_values(6))
        早安祝福 = "{早安}{標點1}{祝福}{標點2}{分享}{標點3}".format(早安=早安, 標點1=標點1, 祝福=祝福, 標點2=標點2, 分享=分享, 標點3=標點3)
        line_bot_api.reply_message(
            event.reply_token, [image_message, image_message2, image_message3, TextSendMessage(text=早安祝福)])

        return 0

    if event.message.text == "午安":
        client = ImgurClient('18f064544f219ac', 'b17f2b3ef24f98c4e3cce9424ef0b1b7173ef642')
        images = client.get_album_images('k7Z38KG')
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )

        午安 = random.choice(sheet.col_values(8))
        標點1 = random.choice(sheet.col_values(2))
        祝福 = random.choice(sheet.col_values(9))
        標點2 = random.choice(sheet.col_values(4))
        分享 = random.choice(sheet.col_values(10))
        標點3 = random.choice(sheet.col_values(6))
        午安祝福 = "{午安}{標點1}{祝福}{標點2}{分享}{標點3}".format(午安=午安, 標點1=標點1, 祝福=祝福, 標點2=標點2, 分享=分享, 標點3=標點3)

        line_bot_api.reply_message(
            event.reply_token, [image_message, TextSendMessage(text=午安祝福)])

        return 0

    if event.message.text == "晚安":
        client = ImgurClient('18f064544f219ac', 'b17f2b3ef24f98c4e3cce9424ef0b1b7173ef642')
        images = client.get_album_images('daOzv5n')
        index = random.randint(0, len(images) - 1)
        url = images[index].link
        image_message = ImageSendMessage(
            original_content_url=url,
            preview_image_url=url
        )

        晚安 = random.choice(sheet.col_values(12))
        標點1 = random.choice(sheet.col_values(2))
        祝福 = random.choice(sheet.col_values(13))
        標點2 = random.choice(sheet.col_values(4))
        分享 = random.choice(sheet.col_values(14))
        標點3 = random.choice(sheet.col_values(6))
        晚安祝福 = "{晚安}{標點1}{祝福}{標點2}{分享}{標點3}".format(晚安=晚安, 標點1=標點1, 祝福=祝福, 標點2=標點2, 分享=分享, 標點3=標點3)

        line_bot_api.reply_message(
            event.reply_token, [image_message, TextSendMessage(text=晚安祝福)])

        return 0

        if event.message.text == "週末愉快":
            client = ImgurClient('18f064544f219ac', 'b17f2b3ef24f98c4e3cce9424ef0b1b7173ef642')
            images = client.get_album_images('hyoRqLE')
            index = random.randint(0, len(images) - 1)
            url = images[index].link
            image_message = ImageSendMessage(
                original_content_url=url,
                preview_image_url=url
            )

            週末 = random.choice(sheet.col_values(16))
            標點1 = random.choice(sheet.col_values(2))
            祝福 = random.choice(sheet.col_values(17))
            標點2 = random.choice(sheet.col_values(4))
            分享 = random.choice(sheet.col_values(5))
            標點3 = random.choice(sheet.col_values(6))
            週末祝福 = "{週末}{標點1}{祝福}{標點2}{分享}{標點3}".format(週末=週末, 標點1=標點1, 祝福=祝福, 標點2=標點2, 分享=分享, 標點3=標點3)
            line_bot_api.reply_message(
                event.reply_token, [image_message, TextSendMessage(text=週末祝福)])

            return 0

    if event.message.text == "我要問安圖!":
        message = ImagemapSendMessage(
            base_url='https://i.imgur.com/SvEVQRQ.png',
            alt_text='this is an imagemap',
            base_size=BaseSize(height=1040, width=1040),
            actions=[
                MessageImagemapAction(
                    text='早安',
                    area=ImagemapArea(
                        x=0, y=0, width=520, height=520
                    )
                ),
                MessageImagemapAction(
                    text='午安',
                    area=ImagemapArea(
                        x=520, y=0, width=520, height=520
                    )
                ),
                MessageImagemapAction(
                    text='晚安',
                    area=ImagemapArea(
                        x=0, y=520, width=520, height=520
                    )
                ),
                MessageImagemapAction(
                    text='週末愉快',
                    area=ImagemapArea(
                        x=520, y=520, width=520, height=520
                    )
                )
            ]
        )
        line_bot_api.reply_message(event.reply_token, message)

        return 0

    if event.message.text == "11111":
        content = ettoday()
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    if event.message.text == "早安哲學":
        article = random.choice(sheet_早安哲學.col_values(1))
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=article))
        return 0

    if event.message.text == "每日新知":
        content = "".join(random.sample(test_news(), k=3))
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0


@app.route('/')
def index():
    return 'Hello World'


import os

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))

    app.run(host='0.0.0.0', port=port)
