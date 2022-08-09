#載入LineBot所需要的模組
from flask import Flask, request, abort
 
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

line_bot_api = LineBotApi('sjEayc82L0K5ev7FYdxxs7AV4jNAx1nqKQmrVlc+PeJOHaRB+meKQg0wpVFIlbbIF791AbvJDZ6LFiVsCQmddIH4OLMVRRyP4iugpwocMSREw/9T9hM5KQ16QsddyQUo93zVlIGBmk5Wkcnq745HKAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('e213dad35df328c5db99a16199c7ecef')
line_bot_api.push_message('Uc1256d73be33afcc36970d5f722b6114', TextSendMessage(text='你可以開始了'))

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
    message = TextSendMessage(text=event.message.text)
    #line_bot_api.reply_message(event.reply_token,message)
    if "股票 " in message:
        buttons_template_message = TemplateSendMessage(
        alt_text = "股票資訊",
        template=CarouselTemplate( 
            columns=[ 
                CarouselColumn( 
                            thumbnail_image_url ="https://www.moneyweekly.com.tw/Photo/%E8%AA%AA%E8%A7%A3%E8%B2%A1%E7%B6%93%E5%A4%A7%E5%B0%8F%E4%BA%8B/202109281943_510054.jpg",
                            title = message[3:] + " 股票資訊", 
                            text ="請點選想查詢的股票資訊", 
                            actions =[
                                MessageAction( 
                                    label= message[3:] + " 個股資訊",
                                    text= "個股資訊 " + message[3:]),
                                MessageAction( 
                                    label= message[3:] + " 個股新聞",
                                    text= "個股新聞 " + message[3:]),
                            ]
                        ),
                        CarouselColumn( 
                            thumbnail_image_url ="https://www.moneyweekly.com.tw/Photo/%E8%AA%AA%E8%A7%A3%E8%B2%A1%E7%B6%93%E5%A4%A7%E5%B0%8F%E4%BA%8B/202109281943_510054.jpg",
                            title = message[3:] + " 股票資訊", 
                            text ="請點選想查詢的股票資訊", 
                            actions =[
                                MessageAction( 
                                    label= message[3:] + " 最新分鐘圖",
                                    text= "最新分鐘圖 " + message[3:]), 
                                MessageAction( 
                                    label= message[3:] + " 日線圖",
                                    text= "日線圖 " + message[3:]),  
                            ]
                        ),
                        CarouselColumn( 
                            thumbnail_image_url ="https://www.moneyweekly.com.tw/Photo/%E8%AA%AA%E8%A7%A3%E8%B2%A1%E7%B6%93%E5%A4%A7%E5%B0%8F%E4%BA%8B/202109281943_510054.jpg",
                            title = message[3:] + " 股利資訊", 
                            text ="請點選想查詢的股票資訊", 
                            actions =[
                                MessageAction( 
                                    label= message[3:] + " 平均股利",
                                    text= "平均股利 " + message[3:]),
                                MessageAction( 
                                    label= message[3:] + " 歷年股利",
                                    text= "歷年股利 " + message[3:])
                            ]
                        ),                               
                    ]
                ) 
            )
        line_bot_api.reply_message(event.reply_token, buttons_template_message)
    else:
         line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

    if '大戶籌碼 ' in message:
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
    else:
         line_bot_api.reply_message(event.reply_token, TextSendMessage(message))

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)