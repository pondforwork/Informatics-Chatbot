import nltk
import json
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from linebot import LineBotApi, WebhookHandler
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
from lextoplus import LexToPlus
from nltk.chat.util import Chat, reflections
from linebot import LineBotApi, WebhookParser

nltk.download("punkt")
nltk.download("wordnet")
tokenizer = LexToPlus()

CHANNEL_ACCESS_TOKEN = "sFKbmIxkJiVOr+thCyLwFpYffmtUJP0aDbvqVp7hRM4T8qkG4VuTKkfRQzZk5OE9AcYAc2w2y0qPQJZ2Qy9qnQjvk7WAM6b8lJr0S66s71WMszwn6FtRLMMURSo6OU3Js1X1hZee/CZr8mR3HSOuuAdB04t89/1O/w1cDnyilFU="
line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)

pairs = [
    [r"hi|hey|hello|สวัสดี|สบายดี", ["สวัสดีครับ มีอะไรให้ช่วยไหมครับ"]],
    [
        r"มี สาขา อะไร บ้าง|แต่ละ สาขา มีอะไร บ้าง|แต่ละ หลักสูตร มีอะไร บ้าง|สาขา",
        [
            "ปริญญาตรี 1.หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์ 2.หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาเทคโนโลยีสารสนเทศเพื่ออุตสาหกรรมดิจิทัล 3.หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิศวกรรมซอฟต์แวร์ 4.หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาปัญญาประดิษฐ์ประยุกต์และเทคโนโลยีอัจฉริยะปริญญาโท1.หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาวิทยาการข้อมูลปริญญาเอก1.หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาวิชาวิทยาการข้อมูล"
        ],
    ],
    [
        r"คณะ มี กี่ สาขา|คณะ",
        ["ทางคณะมีทั้งหมด 6 สาขา รวมทั้งหลักสูตร ปริญญาตรี ปริญญาโท และ ปริญญาเอก"],
    ],
    [
        r"มี สาขา อะไร บ้าง|แต่ละ สาขา มีอะไร บ้าง|แต่ละ หลักสูตร มีอะไร บ้าง",
        [
            "ปริญญาตรี 1.หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิทยาการคอมพิวเตอร์ 2.หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาเทคโนโลยีสารสนเทศเพื่ออุตสาหกรรมดิจิทัล 3.หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาวิศวกรรมซอฟต์แวร์ 4.หลักสูตรวิทยาศาสตรบัณฑิต สาขาวิชาปัญญาประดิษฐ์ประยุกต์และเทคโนโลยีอัจฉริยะปริญญาโท1.หลักสูตรวิทยาศาสตรมหาบัณฑิต สาขาวิชาวิทยาการข้อมูลปริญญาเอก1.หลักสูตรปรัชญาดุษฎีบัณฑิต สาขาวิชาวิทยาการข้อมูล"
        ],
    ],
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


class LineRequest(BaseModel):
    events: list


@app.post("/line/webhook")
async def line_webhook(data: LineRequest):
    for event in data.events:
        # Check if the event type is a message and the message type is text
        if event["type"] == "message" and event["message"]["type"] == "text":
            reply_token = event.get("replyToken", None)
            if reply_token is None:
                # If reply token is missing, log an error and continue to the next event
                print("Missing reply token in event:", event)
                continue

            # Get the user's input message
            user_input = event["message"]["text"].strip().lower()

            # Check if the user typed "image"
            if "image" in user_input:
                # Define the URLs for the image you want to send
                image_url = "https://images.ctfassets.net/hrltx12pl8hq/28ECAQiPJZ78hxatLTa7Ts/2f695d869736ae3b0de3e56ceaca3958/free-nature-images.jpg?fit=fill&w=1200&h=630"  # Replace with your image URL
                preview_url = (
                    image_url  # The preview URL can be the same as the image URL
                )

                # Create an ImageSendMessage object
                image_message = ImageSendMessage(
                    original_content_url=image_url, preview_image_url=preview_url
                )

                # Send the image message as a response using the reply token
                line_bot_api.reply_message(reply_token, [image_message])

            else:
                # If the user did not type "image", handle the request as usual
                tokenized_input = tokenizer.tokenize(user_input)
                processed_input = " ".join(tokenized_input)
                response = chatbot.respond(processed_input)

                # Check if the response is None or empty and handle appropriately
                if response is None or response == "":
                    response = "ไม่เข้าใจ กรุณาถามใหม : หรือพิมพ์ example เพื่อดูตัวอย่างคำถาม"

                # Create a TextSendMessage object
                text_message = TextSendMessage(text=response)

                # Send the text message as a response using the reply token
                line_bot_api.reply_message(reply_token, [text_message])
