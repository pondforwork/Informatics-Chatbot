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
        if event["type"] == "message" and event["message"]["type"] == "text":
            user_input = tokenizer.tokenize(event["message"]["text"])
            user_input = " ".join(user_input)
            response = chatbot.respond(user_input)
            if response is None:
                response = "ไม่เข้าใจ กรุณาถามใหม : หรือพิมพ์ example เพื่อดูตัวอย่างคำถาม"
            messages = [TextSendMessage(text=response)]
            line_bot_api.reply_message(event["replyToken"], messages)
            image_url = "free-nature-images.jpg"  # URL of the image you want to send
            preview_url = image_url  # URL of the preview image (usually the same as the main image)
            # Create ImageSendMessage object
            image_message = ImageSendMessage(
                original_content_url=image_url, preview_image_url=preview_url
            )
            line_bot_api.reply_message(event["replyToken"], [image_message])
        # else:
        #     # Assuming `response` contains a decision on whether to send an image or text.
        #     #if "image_url" in response:
        #     if "image_url" in response:
        #         # Reply with an image
        #         #https://letsenhance.io/static/8f5e523ee6b2479e26ecc91b9c25261e/1015f/MainAfter.jpg
        #         image_url = response["image_url"]  # URL of the image you want to send
        #         preview_url = image_url  # URL of the preview image (usually the same as the main image)
        #         # Create ImageSendMessage object
        #         image_message = ImageSendMessage(
        #             original_content_url=image_url, preview_image_url=preview_url
        #         )

        #         # Send image message as a response
        #         line_bot_api.reply_message(event["replyToken"], [image_message])
        #     else:
        #         # Reply with text message
        #         messages = [TextSendMessage(text=response)]
        #         line_bot_api.reply_message(event["replyToken"], messages)

    #             {
    #   "type": "image",
    #   "originalContentUrl": "https://example.com/original.jpg",
    #   "previewImageUrl": "https://example.com/preview.jpg"
    # }

    return JSONResponse(content={"success": True})
