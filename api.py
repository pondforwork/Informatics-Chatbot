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
    [
        r"การติด โปร คือ อะไร   \( Probation \)   ?| ติด โปร คือ อะไร|ติด โปร คือ ไร|ติด โปร",
        [
            "Probation แปลเป็นภาษาไทยง่าย ๆ คือ 'สถานะรอพินิจ' และแบ่งเป็น 2 ประเภท:"
            "- โปรสูง: เกรดเฉลี่ยสะสมต่ำกว่า 2.00 แต่มากกว่าหรือเท่ากับ 1.80 นิสิตที่ติดโปรสูงเกิน 4 เทอม ถ้าเทอมที่ 5 เกรดเฉลี่ยสะสมยังไม่พ้น 1.80 - 2.00 จะถูกรีไทร์"
            "- โปรต่ำ: เกรดเฉลี่ยสะสมน้อยกว่า 1.80 แต่มากกว่า 1.75 นิสิตที่ติดโปรต่ำเกิน 2 เทอม ถ้าเทอมที่ 3 เกรดเฉลี่ยสะสมยังไม่พ้น 1.75 - 1.79 จะถูกรีไทร์"
        ],
    ],
    [
        r"การย้าย คณะ มี หลัก เกณฑ์ อะไร บ้าง|หลัก เกณฑ์ การย้าย คณะ|ย้าย คณะ",
        [
            "นิสิต ซึ่งศึกษาตามหลักสูตร 4 ปี อาจขอย้ายคณะได้ โดยต้องเรียนในคณะเดิมอย่างน้อย 2ภาคเรียนทั้งนี้ ไม่นับภาคเรียนที่ลาพักการศึกษาหรือถูกสั่งให้พักการเรียน และ ไม่เคยได้รับอนุมัติให้ย้ายคณะมาก่อน"
        ],
    ],
    [
        r"การ เปลี่ยน สาขา วิชา ภายใน คณะ   มี หลัก เกณฑ์   อะไร บ้าง|เปลี่ยน สาขา วิชา ใน คณะ|เปลี่ยน สาขา วิชา|เปลี่ยน สาขา",
        [
            "นิสิต ซึ่งศึกษาตามหลักสูตร 4ปี อาจขอเปลี่ยนสาขาวิชาภายในคณะได้เพียงครั้งเดียว ทั้งนี้โดยความเห็นชอบของหัวหน้าภาควิชาหรือประธานสาขาวิชาที่เกี่ยวข้องและได้รับอนุมัติจากคณบดี แล้วให้คณบดีแจ้งให้นายทะเบียนทราบ"
        ],
    ],
    [
        r"การ เทียบ โอน หน่วยกิต   มี เกณฑ์ อะไร บ้าง|เทียบ โอน หน่วยกิต|เกณฑ์ การ เทียบ โอน หน่วยกิต|โอน   หน่วยกิต",
        [
            "มหาวิทยาลัยอาจพิจารณาเทียบโอนหน่วยกิตได้ตามประกาศของมหาวิทยาลัย (โดยนิสิต สามารถอ่านเพิ่มเติมได้จากระเบียบมหาวิทยาลัยบูรพา ว่าด้วยการเทียบโอนผลการเรียนระดับปริญญาตรีพ.ศ. 2552)"
        ],
    ],
    [
        r"การลงทะเบียน เพิ่ม ลด ราย วิชา ทำ ได้ อย่างไร|ลงทะเบียน เพิ่ม ลด",
        [
            "– เมื่อถึงช่วงเวลาเพิ่มลดรายวิชาเรียน ตามปฏิทินการศึกษาของมหาวิทยาลัย ให้นิสิตดำเนินการเพิ่มลดออนไลน์ ได้ที่ "
            "http://reg.buu.ac.th/โดยนิสิตต้องรออนุมัติจากอาจารย์ผู้สอน อาจารย์ที่ปรึกษา และคณบดี นิสิตสามารถตรวจสอบ"
            "ได้ในระบบว่าได้รับอนุมัติเพิ่มลดเรียบร้อยหรือไม่"
            "– กรณีที่ไม่ได้รับอนุมัติ นิสิตต้องเขียนใบคำร้องทั่วไป RE-01 เรื่องขอเพิ่มรายวิชาล่าช้า โดยระบุเหตุผล ขอเรียนรายวิชา "
            "xxxxxx และให้อาจารย์ผู้สอนเซนกำกับ และให้อาจารย์ที่ปรึกษาและคณบดีลงนาม จากนั้น นิสิตนำใบคำร้อง ส่งได้ที่งานทะเบียนและสถิตินิสิต ชั้น 1  อาคาร ภปร."
        ],
    ],
    [
        r"การถอน ราย วิชา   \( Drop \)   ทำ อย่างไร   ?",
        [
            "ในการถอนรายวิชา นิสิตสามารถขอใบคำร้องถอนรายวิชาได้ที่งานทะเบียนและสถิตินิสิต ชั้น 1  อาคาร ภปร. โดยไม่ต้อง"
            "ให้อาจารย์ประจำวิชาลงนาม แต่ต้องให้อาจารย์ที่ปรึกษาและคณบดีลงนาม และนำส่งที่งานทะเบียนและสถิตินิสิต ชั้น 1  "
            "อาคาร ภปร. ตามวันเวลาที่กำหนด โดยเก็บสำเนาใบถอนรายวิชาไว้ด้วย"
        ],
    ],
    [
        r"เรียน แล้ว ติด   F   ทำ อย่างไร   ?|ติด   F|ติด   f",
        [
            "ถ้าวิชาใดที่นิสิตเรียนแล้วติด F นิสิตต้องเรียนซ้ำเพื่อแก้ผลการเรียนครับ มีเงื่อนไขคือ ถ้านิสิตได้รับF ในรายวิชาบังคับ "
            "นิสิตจะต้องลงทะเบียนเรียนรายวิชานั้นซ้ำอีก จนกว่าจะได้รับ A, B+, B, C+, C, D+, D หรือ  S  แต่ถ้าได้รับ F ในรายวิชา"
            "เลือกนิสิตจะสามารถลงทะเบียนเรียนวิชาอื่นแทนได้ แต่ต้องอยู่ในกลุ่มวิชาเดียวกัน"
        ],
    ],
    [
        r"คณะ วิทยา การ สารสนเทศ จัดตั้ง เมื่อ ใด|คณะ วิทยา การ สารสนเทศ จัดตั้ง เมื่อ ไห ร่|คณะ นี้ จัดตั้ง เมื่อ ไห ร่",
        [
            " คณะวิทยาการสารสนเทศ จัดตั้งขึ้นอย่างเป็นทางการเมื่อวันที่ 9 ธันวาคม พ.ศ. 2552 โดยยกฐานะจากภาควิชาวิทยาการคอมพิวเตอร์ ซึ่งเป็นหน่วยงานภายใต้คณะวิทยาศาสตร์ ที่ถูกจัดตั้งขึ้นเมื่อวันที่ 4 ตุลาคม พ.ศ. 2536"
        ],
    ],
    [
        r"สาขา ใด เปิด หลักสูตร มานาน แล้ว ที่สุด|สาขา ใด เปิด มานานที่ สุด",
        ["สาขาวิชาวิทยาการคอมพิวเตอร์ เปิดหลักสูตรปี พ.ศ. 2536 ซึ่งเปิดมานานที่สุดภายในคณะ"],
    ],
    [
        r"ที่ คณะ มี สโมสร นิสิต ไหม |สโมสร นิสิต",
        [
            "ทางคณะมีสโมสรนิสิต ปกป้องรักษาผลประโยชน์และสิทธิอันชอบธรรมของนิสิตคณะวิทยาการสารสนเทศในเรื่องที่เกี่ยว"
            "กับกิจกรรมนิสิต ไม่ว่าจะเป็นกิจกรรมภายในคณะวิทยาการสารสนเทศ หรือกิจกรรมภายนอกคณะวิทยาการสารสนเทศ"
        ],
    ],
    [
        r"มี การเตรียมพร้อม ให้ นิสิต ใหม่ หรือ ไม่|มี การเตรียมพร้อม ให้ เด็กใหม่ หรือ ไม่|การเตรียมพร้อม|การเตรียมพร้อม ให้ นิสิต",
        ["มีการเตรียมความพร้อมให้น้องปีหนึ่งก่อนเริ่มเรียนภาคเรียนแรกในรั้วมหาวิทยาลัย"],
    ],
    [
        r"ทาง คณะ มี ทุนการศึกษา ให้ หรือ ไม่|ทุนการศึกษา",
        ["ทางคณะมีทุนให้กับนักศึกษา โดยสามารถติดตามข่าวสารได้ที่ประกาศประชาสัมพันธ์"],
    ],
    [
        r"สามารถ จอง ห้อง เพื่อ ใช้งาน ได้ หรือ ไม่|ถ้า นิสิต ไม่มี คอม|จอง ห้อง เพื่อ ใช้ คอม|จอง ห้อง",
        [
            "ทางคณะมีระบบจองห้องคณะวิทยาการสารสนเทศ ตามลิงก์นี้ https://docs.google.com/forms/d/e/1FAIpQLSedKs0QhG_aD6x-Vxp9zDfq41WeVyDf_dDnpeA6pjoYfjxMTA/viewform"
        ],
    ],
    [
        r"Where is your faculty|where is this faculty",
        [
            "169 Long Had Bangsaen Road, Saensuk Subdistrict,Muang District, Chonburi Province 20131"
        ],
    ],
    [
        r"How many courses that you have|how many course this faculty have",
        [
            "4 courses for Bachelor Degree: Computer Science, Information Technology, Software Engineering,  Applied Artificial Intelligence and Smart Technology. all of this are Bachelor of Science Program Department. 1 course for Master Degree: Master of Science Program Department of Data Science 1 course for Doctoral Degree: Doctor of Philosophy Program Department of Data Science"
        ],
    ],
    [
        r"if i need more information about the course what should i do|more information|about the course|more info about the course",
        [
            "Website: https://www.informatics.buu.ac.th/2020/?page_id=35&lang=en Facebook Page: https://www.facebook.com/InformaticsBuu Email: pr@informatics.buu.ac.th  Dean Office Tel. +66 (0)38-103061, Academic Office Tel.+66 (0)38-103096"
        ],
    ],
    [
        r"do you join the tcas|tcas",
        [
            "yes. we join tcas can you can see more information about timeline and requirements on our website: https://www.informatics.buu.ac.th/2020/?page_id=35&lang=en"
        ],
    ],
    [
        r"how i go|how to travel|how to travel to faculty|how to travel to this faculty",
        [
            "you have 3 ways to go to our faculty: 1.with trains and buses 2.with trains and mini-vans 3.with taxi and this are guide if you want more detail: https://www.informatics.buu.ac.th/2020/wp-content/uploads/2018/11/travel_direction_to_buu.pdf"
        ],
    ],
    [
        r"about visa for international students",
        [
            "ED visa request you can go to: https://www.informatics.buu.ac.th/2020/wp-content/uploads/2018/11/infomation.pdf this is guide of information about visa extentionand this is all guides in visa for international students : https://www.informatics.buu.ac.th/2020/?page_id=8184&lang=en"
        ],
    ],
    [
        r"คนต่างชาติ สามารถ เรียน ได้ ไหม|คนต่างชาติ|ต่างชาติ|ต่างชาติ เรียน ได้ ไหม",
        [
            "สามารถเรียนได้ โดยรายวิชาแผนการสอนที่เปิดเป็นภาษาอังกฤษมีด้วยกัน 4 สาขา"
            "1.สาขาวิชาวิทยาการคอมพิวเตอร์"
            "2.สาขาวิชาเทคโนโลยีสารสนเทศเพื่ออุตสาหกรรมดิจิทัล"
            "3.สาขาวิชาวิศวกรรมซอฟต์แวร์"
            "4.สาขาวิชาปัญญาประดิษฐ์ประยุกต์และเทคโนโลยีอัจฉริยะ"
        ],
    ],
    [
        r"ถ้า อยาก ไป เรียน ต่อ ที่ ต่างประเทศ ต้อง ทำ ยัง ไง|อยาก ไป เรียน ต่อ ต่างประเทศ|อยาก เรียน ต่อ ต่างประเทศ",
        [
            "ในกรณีที่นิสิตมีความประสงค์จะไปแลกเปลี่ยนกับมหาวิทยาลัยหรือหน่วยการเพื่อการศึกษาในต่างประเทศ นิสิตควรปฏิบัติดังนี้"
            "1.ถ้ามีการประกาศให้ทุน ให้นิสิตอ่านรายละเอียดและเงื่อนไขของทุนให้ละเอียด แล้วปฏิบัติตามที่ทุนดังกล่าวได้ระบุไว้"
            "2.ถ้านิสิตมีข้อสงสัยเกี่ยวกับทุน ให้ติดต่อสำนักงานจัดการศึกษา คณะวิทยาการสารสนเทศ"
            "3.ถ้านิสิตมีความประสงค์จะไปศึกษาแลกเปลี่ยนด้วยทุนส่วนตัว ให้แจ้งความจำนงที่สำนักงานจัดการศึกษา เพื่อจะได้ประสานงานกับมหาวิทยาลัยหรือหน่วยงานในต่างประเทศต่อไป"
            "4.นิสิตต้องเตรียมความพร้อมด้านเอกสารที่จำเป็นทั้งหมด เช่น หนังสือเดินทาง การขอตรวจลงตรา (วีซ่า) เอกสารตอบรับจากมหาวิทยาลัยต่างประเทศ เป็นต้น"
            "5.นิสิตต้องเตรียมการด้านภาษาเพื่อการสื่อสาร ถ้าเป็นการแลกเปลี่ยนระยะสั้น อาจจะไม่จำเป็นต้องใช้ผลการทดสอบความสามารถด้านภาษาอังกฤษ แต่ถ้าเป็นการศึกษาต่อ นิสิตจำเป็นจะต้องมีผลการทดสอบภาษาอังกฤษด้วย"
            "6.สำนักงานจัดการศึกษา คณะวิทยาการสารสนเทศ เป็นผู้ประสานงานให้นิสิตโดยตรง สามารถติดต่อสอบถาม ขอความช่วยเหลือ ได้ในวันและเวลาราชการ"
        ],
    ],
    [
        r"จะ ทำ วี ซ่า เพื่อ ไป ศึกษา ต่อ ที่ ต่างประเทศ ได้ อย่างไร|ทำ วี ซ่า|วี ซ่า เพื่อ ไป ศึกษา ต่อ ที่ ต่างประเทศ|ศึกษา   ต่อ   ที่   ต่างประเทศ",
        [
            "ข้อมูลสำหรับนิสิตไทย การขอวีซ่าเพื่อการศึกษานั้น ขึ้นอยู่กับประเทศปลายทางที่จะไป นิสิตที่สนใจจำเป็นจะต้องศึกษารายละเอียดด้วยตนเอง หากต้องการคำปรึกษา กรุณาติดต่อสำนักงานจัดการศึกษา คณะวิทยาการสารสนเทศ"
        ],
    ],
    [
        r"ค่าใช้จ่าย ที่จะ ไป ศึกษา ต่อ ต่างประเทศ เท่าไหร่|ค่าใช้จ่าย ศึกษา ต่อ ต่างประเทศ",
        ["ขั้นอยู่กับประเทศที่ต้องการจะไปศึกษาต่อ และวีซ่าในแต่ละประเภทของประเทศนั้น ๆ"],
    ],
    [
        r"ใน แต่ หลักสูตร ของ แต่ละ สาขา มี การฝึกงาน หรือ ไม่|การฝึกงาน|ฝึกงาน|สาขา มี การฝึกงาน หรือ ไม่",
        [
            "ทางคณะมีวิชาที่ให้นิสิตเลือกได้คล้ายกับการฝึกงานคือสหกิจศึกษาโดยจะมีเกณฑ์ในการรับสหกิจศึกษาสามารถศึกษาเพิ่มเติมได้ที่เล่มหลักสูตร"
        ],
    ],
    [
        r"อยาก เป็น   BA|ชอบ ออกแบบ",
        [
            "แนะนำสาขา IT สาขานี้เราจะมุ่งไปทางด้าน Business ด้านการออกแบบหน้าจอ UI และการทำเอกสารต่างๆ"
        ],
    ],
    [
        r"อยาก สร้าง   AI|อยาก ทำ ChatGPT|อยาก ทำ บอ ท|อยาก ทำ AI|อยาก ทำ ai",
        [
            "แนะนำให้เรียนสาขา AI สาขานี้กำลังมาแรงในยุคนี้ สาขานี้จะเน้นไปในทางการสร้าง AI "
        ],
    ],[
        r"อยาก เป็น โปรแกรมเมอร์|อยาก เขียนโปรแกรม|เขียนโปรแกรม|อยาก สร้าง แอ ป|อยาก สร้าง แอ พ",
        [
            "แนะนำให้เรียนที่สาขา CS(Computer Science) เพราะว่าสายนี้เหมาะกับผู้ที่มีความสนใจในการเขียนโปรแกรม ทางสาขานี้จะมีการเรียนการสอนที่มุ่งเน้นไปในด้านการเขียนโปรแกรม"
        ],
    ],[
        r"example",
        [
            "ตัวอย่างคำถาม : มีสาขาอะไรบ้าง , ติดโปรคือไร , เรียนแล้วติด F ทำอย่างไร ?, อยากเป็นโปรแกรมเมอร์ต้องเรียนสาขาไหน สำหรับตัวอย่างเพิ่มเติม พิมพ์ example2"
        ],
    ],[
        r"example2",
        [
            "ตัวอย่างคำถาม : ถ้าอยากไปเรียนต่อที่ต่างประเทศต้องทำยังไง , คนต่างชาติสามารถเรียนได้ไหม , where is this faculty , about visa for international students"
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


# @app.post("/chat")
# def chat_post_endpoint(request: QuestionRequest):
#     try:
#         user_input = tokenizer.tokenize(request.question)
#         user_input = " ".join(user_input)
#     except Exception as e:
#         return {"error": f"Tokenization failed: {str(e)}"}

#     response = chatbot.respond(user_input)
#     if response is None:
#         response = "ถามใหม่สิ"

#     return {"question": request.question, "response": response}


# @app.post("/ask")
# def ask_question(item: Item):
#     user_input = item.question
#     user_input = tokenizer.tokenize(user_input)
#     user_input = " ".join(user_input)

#     response = chatbot.respond(user_input)

#     if response is None:
#         response = "Don't understand!"

#     return {"response": response}


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
                response = (
                    "ไม่เข้าใจ กรุณาถามใหม : หรือพิมพ์ example เพื่อดูตัวอย่างคำถาม"
                )
            messages = [TextSendMessage(text=response)]
            line_bot_api.reply_message(event["replyToken"], messages)

    return JSONResponse(content={"success": True})
