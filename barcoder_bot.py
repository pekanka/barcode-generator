import telebot
from io import BytesIO
from PIL import Image
from barcode.writer import ImageWriter
import barcode
from datetime import datetime, date, time
import pytz

BOT_INTERVAL = 3
BOT_TIMEOUT = 30

def cr_bar(bb):
    wdt = 40/(len(str(bb)) + 2)*0.07
    options = {
        "module_width": wdt,
        "module_height": 10,
    }
    rv = BytesIO()
    barc = barcode.get_barcode_class("code128")
    barc = barc(str(bb), writer=ImageWriter())
    barc.write(rv, options = options)
    rv.seek(0)
    return(rv)


def create_pdf(bar_str):
    doc_s = BytesIO()
    doc_s.name = "barcodes.pdf"
    bars = bar_str.split("\n")
    barcds = []
    for i in bars:
        bars = Image.open(cr_bar(i))
        """img = Image.new('RGB', (600, 300), (255, 255, 255))
        bars = bars.resize(img.size)"""
        barcds.append(bars)
    barcds[0].save(doc_s, save_all = True, append_images = barcds[1:])
    doc_s.seek(0)
    return(doc_s)




bot = telebot.TeleBot('5913721854:AAGvFs3iL_rM6i0_9y7lGP3HwEUQKdnQv0Y')

bio = """
    Это мой телеграм бот для создания штрихкодов
    Для использования отправьте ШК с новой строки по типу
    111
    222
    333
    на выходе будет PDF файл
    автор: @pekanka11
"""

@bot.message_handler(commands=['start'])
def starter(message):
    bot.send_message(chat_id=message.chat.id, text = bio)

@bot.message_handler(content_types=["text"])
def start_message(message):
    try:
        bot.send_document(chat_id = message.chat.id, document = create_pdf(message.text))
        tz = pytz.timezone("Europe/Moscow")
        print("usr: " + message.from_user.username + " time: " + str(datetime.now(tz)) + " len: " + str(len(message.text.split("\n"))))
    except Exception as e:
        bot.send_message(chat_id=message.chat.id, text="Ошибка баркода: присутствуют недопустимые символы")

while True:
	try:
		bot.polling(none_stop=True)
	except Exception as e:
		print("Callback timeout error, restarting")
