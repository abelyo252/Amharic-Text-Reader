import os
import telebot
import uuid
from dotenv import load_dotenv
import cv2
import urllib.request
import numpy as np
import io
from PIL import Image
load_dotenv()

API_KEY = os.getenv("API_KEY")
tb = telebot.TeleBot(API_KEY)
print("Ethio Language Bot Started")


def listener(messages):
    """
    When new messages arrive TeleBot will call this function.
    """
    for m in messages:
        chatid = m.chat.id

        if m.content_type == 'text':
            text = m.text
            tb.send_message(chatid, f"Hello @{m.chat.username}")

def sendPicture(image , chat_id):
    # sendPhoto
    photo = open('img/paper3.jpg', 'rb')
    tb.send_photo(chat_id, photo)
    file_id = str(uuid.uuid4())
    tb.send_photo(chat_id, file_id)

def sendMessage(text , chatid):
    tb.send_message(chatid, text)

def forwardMessage(to_chat_id, from_chat_id, message_id):
    # forwardMessage
    # tb.forward_message(10894,926,3)
    tb.forward_message(to_chat_id, from_chat_id, message_id)















########################################################
############## MESSAGE HANDLER #########################
########################################################

# Handles all text messages that contains the commands '/start' or '/help'.
@tb.message_handler(commands=['start', 'help'])
def handle_start_help(message):
	pass

@tb.message_handler(content_types=['photo'])
def photo(message):
    chatid = message.chat.id
    fileID = message.photo[-1].file_id
    file = tb.get_file(fileID)
    filepath = file.file_path
    downloaded_file = tb.download_file(filepath)
    print(type(downloaded_file))
    img = io.BytesIO(downloaded_file)






    #img = open(downloaded_file, 'rb')
    image = io.BytesIO(img.read())
    frame = Image.open(image)
    img_arr = np.array(frame,dtype="uint8")
    img_arr = cv2.cvtColor(img_arr , cv2.COLOR_RGB2BGR)


    cv2.imshow('lalala', img_arr)
    if cv2.waitKey() & 0xff == 27: quit()






    print('Image Translated Successfully')













########################################################
############## ADD LISTENER HL #########################
########################################################
tb.set_update_listener(listener)
tb.polling(interval=3)

while True: # Don't let the main Thread end.
    pass