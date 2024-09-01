#@AsiacellI2
#@MKOOSH
#HMDTOOLS
#اذكر المصدر
import telebot
from autopep8 import fix_code
import os
from time import sleep

API_TOKEN = ("7195742178:AAFRC-gWPCJ11kmHSbiaXJkamDaYBkzz0nA") 
bot = telebot.TeleBot(API_TOKEN)

users_data = {}

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    users_data[user_id] = {'file_path': '', 'corrected_file_path': ''}
    welcome_message = "مرحبًا! اختر نوع الملف الذي ترغب في تصحيح أخطاءه:\n\nPython 🐍 أو PHP 🐘المطور @AsiacellI2 "

    # Create buttons to choose file type
    markup = telebot.types.InlineKeyboardMarkup()
    python_button = telebot.types.InlineKeyboardButton("Python 🐍", callback_data='python')
    php_button = telebot.types.InlineKeyboardButton("PHP 🐘", callback_data='php')
    markup.row(python_button, php_button)

    # Add developer button
    developer_button = telebot.types.InlineKeyboardButton("Dav", url="https://t.me/AsiacellI2")
    markup.add(developer_button)

    bot.send_message(message.chat.id, welcome_message, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    user_id = call.from_user.id
    if call.data == 'python':
        bot.send_message(call.message.chat.id, "حسنًا، أرسل الآن ملف Python (.py) لأقوم بتصحيحه.")
    elif call.data == 'php':
        bot.send_message(call.message.chat.id, "حسنًا، أرسل الآن ملف PHP (.php) لأقوم بتصحيحه.")

@bot.message_handler(content_types=['document'])
def handle_document(message):
    user_id = message.from_user.id
    file_path = f"temp/{user_id}_{message.document.file_name}"
    corrected_file_path = f"temp/{user_id}_{message.document.file_name.replace('.py', '_corrected.py').replace('.php', '_corrected.php')}"

    try:
        if message.document.file_name.endswith('.py') or message.document.file_name.endswith('.php'):
            # Download the file
            file_info = bot.get_file(message.document.file_id)
            downloaded_file = bot.download_file(file_info.file_path)

            # Save the file
            with open(file_path, 'wb') as new_file:
                new_file.write(downloaded_file)

            # Process and correct the file
            reply_message = bot.reply_to(message, f"جاري المعالجة، يرجى الانتظار (30)")
            for i in range(29, 0, -1):
                sleep(1)
                bot.edit_message_text(f"جاري المعالجة، يرجى الانتظار ({i})⌛️", message.chat.id, reply_message.message_id)

            with open(file_path, 'r') as code_file:
                code_content = code_file.read()

            corrected_code = fix_code(code_content)

            if code_content == corrected_code:
                final_message = "✅ الملف جيد وليس به مشاكل."
            else:
                with open(corrected_file_path, 'w') as corrected_file:
                    corrected_file.write(corrected_code)
                corrected_file = open(corrected_file_path, 'rb')
                bot.send_document(message.chat.id, corrected_file, caption=f"🆙 تم العثور على أخطاء وتم تصحيحها. الملف المصحح مرفق: {message.document.file_name.replace('.py', '_corrected.py').replace('.php', '_corrected.php')}")
                final_message = "ارجو منك تقييم البوت وخبرني عن سبب تقييمك فضلا وليس امرا المطور @AsiacellI2"
            bot.send_message(message.chat.id, final_message)
        else:
            choose_file_type_message = "يرجى اختيار نوع الملف الذي ترغب في تصحيح أخطاءه:\n\nPython 🐍 أو PHP 🐘"
            markup = telebot.types.InlineKeyboardMarkup()
            python_button = telebot.types.InlineKeyboardButton("Python 🐍", callback_data='python')
            php_button = telebot.types.InlineKeyboardButton("PHP 🐘", callback_data='php')
            markup.row(python_button, php_button)

            # Add developer button
            developer_button = telebot.types.InlineKeyboardButton("المطور", url="https://t.me/AsiacellI2")
            markup.add(developer_button)

            bot.send_message(message.chat.id, choose_file_type_message, reply_markup=markup)
    except Exception as e:
        error_message = f"❌ حدث خطأ: {e}"
        bot.reply_to(message, error_message)
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if os.path.exists(corrected_file_path):
            os.remove(corrected_file_path)

if __name__ == '__main__':
    if not os.path.exists("temp"):
        os.makedirs("temp")

    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"An error occurred: {e}")
            sleep(5)
#@AsiacellI2
#@MKOOSH
#HMDTOOLS
#اذكر المصدر