import nltk 
nltk.download('punkt')
nltk.download('wordnet')

from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

from nltk.chat.util import Chat, reflections
from lextoplus import LexToPlus
tokenizer = LexToPlus()
# Define pairs of patterns and responses
pairs = [
    [
        r"ฉัน ชื่อ (.*)",
        ["สวัสดี %1, สบายดีมั้ย",]
    ],
    [
        r"hi|hey|hello|สวัสดี|สบาย ดี",
        ["สวัสดีเจ้า", "ยินดีที่ได้รู้จัก",]
    ],
    [
        r"คุณ ชื่อ (.*)",
        ["ฉันชื่อปอน",]
    ]
    ,
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
# Create chatbot
chatbot = Chat(pairs, reflections)

# Start conversation
def chat():
    print("สวัสดีครับ/ค่ะ! ฉันคือแชทบอทที่คุณสร้างขึ้นนะครับ/ค่ะ พิมพ์ 'quit' เมื่อต้องการจบการสนทนาครับ/ค่ะ")
#     chatbot.converse()
    while True:
        user_input = input("You: ")
        if user_input.lower() == "quit":
            break

        user_input = tokenizer.tokenize(user_input)
        user_input = ' '.join(user_input)
        response = chatbot.respond(user_input)

        if response is None:
            response = "Don't understand!"
        print("Bot:", response)

# Run chatbot
if __name__ == "__main__":
    chat()
