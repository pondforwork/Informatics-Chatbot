import nltk
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from lextoplus import LexToPlus
from nltk.chat.util import Chat, reflections
from linebot import LineBotApi, WebhookParser
nltk.download('punkt')
nltk.download('wordnet')
tokenizer = LexToPlus()

CHANNEL_ACCESS_TOKEN = "sFKbmIxkJiVOr+thCyLwFpYffmtUJP0aDbvqVp7hRM4T8qkG4VuTKkfRQzZk5OE9AcYAc2w2y0qPQJZ2Qy9qnQjvk7WAM6b8lJr0S66s71WMszwn6FtRLMMURSo6OU3Js1X1hZee/CZr8mR3HSOuuAdB04t89/1O/w1cDnyilFU="
CHANNEL_SECRET = "10c92ee5f26b16203603692bfdce9b1a"
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(CHANNEL_SECRET)

pairs = [
    [
        r"ฉัน ชื่อ (.*)",
        ["สวัสดี %1 สบายดีมั้ย",]
    ],
    [
        r"hi|hey|hello|สวัสดี|สบาย ดี",
        ["สวัสดีเจ้า", "ยินดีที่ได้รู้จัก",]
    ],
    [
        r"คุณ ชื่อ (.*)",
        ["ฉันชื่อปอน",]
    ],
    [
        r"สถานที่ ท่องเที่ยว บาง แสน",
        ["หาดบางแสน",]
    ],[
        r"ร้าน ที่ อร่อย ที่สุด ใน ม   บูรพา",
        ["กะเพราบัง",]
    ],[
        r"คุณ เรียน คณะ อะไร",
        ["วิทยาการคอมพิวเตอร์",]
    ]
]

chatbot = Chat(pairs, reflections)
app = FastAPI()

class QuestionRequest(BaseModel):
    question: str

class Item(BaseModel):
    question: str

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/chat")
def chat_post_endpoint(request: QuestionRequest):
    try:
        user_input = tokenizer.tokenize(request.question)
        user_input = ' '.join(user_input)
    except Exception as e:
        return {"error": f"Tokenization failed: {str(e)}"}

    response = chatbot.respond(user_input)
    if response is None:
        response = "ไม่เข้าใจ กรุณาถามใหม่"

    return {"question": request.question, "response": response}

@app.post("/ask")
def ask_question(item: Item):
    user_input = item.question
    user_input = tokenizer.tokenize(user_input)
    user_input = ' '.join(user_input)
    
    response = chatbot.respond(user_input)

    if response is None:
        response = "Don't understand!"

    return {"response": response}


class LineRequest(BaseModel):
    events: list

class LineResponse(BaseModel):
    replyToken: str
    messages: list

@app.post("/line/webhook")
async def line_webhook(data: LineRequest):
    for event in data.events:
        if event["type"] == "message" and event["message"]["type"] == "text":
            user_input = tokenizer.tokenize(event["message"]["text"])
            user_input = ' '.join(user_input)
            response = chatbot.respond(user_input)
            if response is None:
                response = "ไม่เข้าใจ กรุณาถามใหม่"
            messages = [TextSendMessage(text=response)]
            line_bot_api.reply_message(event["replyToken"], messages)

    return JSONResponse(content={"success": True})
