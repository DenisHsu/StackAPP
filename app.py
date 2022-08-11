#載入LineBot所需要的模組
from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import re
import requests
from bs4 import BeautifulSoup
import jieba
import pandas as pd


app = Flask(__name__)

line_bot_api = LineBotApi('sjEayc82L0K5ev7FYdxxs7AV4jNAx1nqKQmrVlc+PeJOHaRB+meKQg0wpVFIlbbIF791AbvJDZ6LFiVsCQmddIH4OLMVRRyP4iugpwocMSREw/9T9hM5KQ16QsddyQUo93zVlIGBmk5Wkcnq745HKAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e213dad35df328c5db99a16199c7ecef')
line_bot_api.push_message('Uc1256d73be33afcc36970d5f722b6114', TextSendMessage(text='Program Update Success!!'))

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

#訊息傳遞區塊
##### 基本上程式編輯都在這個function #####
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = event.message.text
    #line_bot_api.reply_message(event.reply_token,message)
    try:
        # if re.match("股票 ",message):
        #     buttons_template_message = TemplateSendMessage(
        #     alt_text = "股票資訊",
        #     template=CarouselTemplate( 
        #         columns=[ 
        #                 CarouselColumn( 
        #                     thumbnail_image_url ="https://www.moneyweekly.com.tw/Photo/%E8%AA%AA%E8%A7%A3%E8%B2%A1%E7%B6%93%E5%A4%A7%E5%B0%8F%E4%BA%8B/202109281943_510054.jpg",
        #                     title = message + " 股票資訊", 
        #                     text ="請點選想查詢的股票資訊", 
        #                     actions =[
        #                         MessageAction( 
        #                             label= message[3:] + " 個股資訊",
        #                             text= "個股資訊 " + message[3:]),
        #                         MessageAction( 
        #                             label= message[3:] + " 個股新聞",
        #                             text= "個股新聞 " + message[3:])
        #                     ]
        #                 )
        #             ]
        #         )
        #     )
        #     line_bot_api.reply_message(event.reply_token, buttons_template_message)
        # else:
        #     line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

        if re.match("大戶籌碼 ",message):
            flex_message = TextSendMessage(text="請選擇要顯示的買賣超資訊",
            quick_reply=QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="最新法人", text="最新法人買賣超 " + message[5:])),
            QuickReplyButton(action=MessageAction(label="歷年法人", text="歷年法人買賣超 " + message[5:])),
            QuickReplyButton(action=MessageAction(label="外資", text="外資買賣超 " + message[5:])),
            QuickReplyButton(action=MessageAction(label="投信", text="投信買賣超 " + message[5:])),
            QuickReplyButton(action=MessageAction(label="自營商", text="自營商買賣超 " + message[5:])),
            QuickReplyButton(action=MessageAction(label="三大法人", text="三大法人買賣超 " + message[5:]))
            ]))
            line_bot_api.reply_message(event.reply_token, flex_message)
        elif re.match("個股資訊 ",message):
            stock_n = stock_id(message[5:])
            #cont = continue_after(message[5:])
            line_bot_api.reply_message(event.reply_token,TextSendMessage(stock_n))
        else:
            line_bot_api.reply_message(event.reply_token, TextSendMessage(message))
    except Exception as e:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(e))
    

#個股資訊
def stock_id(message):
    try:
        url = "https://goodinfo.tw/StockInfo/StockDetail.asp?STOCK_ID=" + str(message)
        headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36"
        }
        res = requests.get(url,headers = headers)
        res.encoding = "utf-8"
        soup = BeautifulSoup(res.text,"html.parser")
        soup1 = soup.find("table",{"class":"b1 p4_2 r10"})
        soup2 = soup1.find("tr",{"align":"center"}).text.split(" ")[1:-1]
        soup3 = soup.find("td",{"style":"padding:0 2px 5px 20px;width:10px;"})
        soup4 = soup3.find("a").text.split("\xa0")
        soup_1 = soup.find("table",{"class":"b1 p4_4 r10"})
        soup_2 = soup_1.find_all("td",{"bgcolor":"white"})
        mes = "股票代號 :{} \n股票名稱 : {} \n產業別 : {} \n市場 : {}\n成交價 : {} \n昨收 : {} \n漲跌價 : {} \n漲跌幅 : {} \n振幅 : {} \n開盤價 : {} \n最高價 : {} \n最低價 : {} \n資本額 : {} \n市值 : {}".format(soup4[0],soup4[1],soup_2[1].text,soup_2[2].text,soup2[0],soup2[1],soup2[2],soup2[3],soup2[4],soup2[5],soup2[6],soup2[7],soup_2[4].text,soup_2[5].text)
        return mes
    except:
        return("請輸入正確的股票代號")


#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)