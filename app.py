from flask import Flask, request, abort
from linebot import (LineBotApi, WebhookHandler)
from linebot import (InvalidSignatureError)
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
    line_bot_api.reply_message(event.reply_token,message)

#主程式
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
