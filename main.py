import telebot
from telebot import types

bot = telebot.TeleBot('6921760139:AAGSiBqm_2hhCZfcE2J8DTvdwGo3BCcw0g0')

name = ''
surname = ''
age = 0
speciality = ''
experience = 0
phonenumber = ''


@bot.message_handler(content_types=['text'])
def start(message):
    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Ваше имя?")
        bot.register_next_step_handler(message, get_name)
    else:
        bot.send_message(message.from_user.id, 'Привет! Это наша автоматизированная система подачи заявок '
                                               'на собеседование! Для продолжения напишите /reg')


def get_name(message):  # получаем фамилию
    global name
    name = message.text
    bot.send_message(message.from_user.id, 'Ваша фамилия?')
    bot.register_next_step_handler(message, get_surname)


def get_surname(message):
    global surname
    surname = message.text
    bot.send_message(message.from_user.id, 'Сколько вам лет? Введите числом!')
    bot.register_next_step_handler(message, get_age)


def get_age(message):
    global age
    age = int(message.text)
    bot.send_message(message.from_user.id, 'Ваша специальность?')
    bot.register_next_step_handler(message, get_speciality)


def get_speciality(message):
    global speciality
    speciality = message.text
    bot.send_message(message.from_user.id, 'Какой у вас опыт работы? Введите числом!')
    bot.register_next_step_handler(message, get_experience)


def get_experience(message):
    global experience
    experience = int(message.text)
    bot.send_message(message.from_user.id, 'Введите ваш номер телефона для связи с вами!')
    bot.register_next_step_handler(message, get_phone)


def get_phone(message):
    global phonenumber
    phonenumber = message.text

    keyboard = types.InlineKeyboardMarkup()
    key_yes = types.InlineKeyboardButton(text='Да', callback_data='yes')
    keyboard.add(key_yes)
    key_no = types.InlineKeyboardButton(text='Нет', callback_data='no')
    keyboard.add(key_no)
    question = (f'Вот ваша анкета: \n'
                f'Имя: {name} \n'
                f'Фамилия: {surname} \n'
                f'Возраст: {age} год \n'
                f'Специальность: {speciality} \n'
                f'Опыт Работы: {experience} год(-а)/лет \n'
                f'Телефон для связи: {phonenumber} \n'
                f'Все данные верны?')
    bot.send_message(message.from_user.id, text=question, reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "yes":
        bot.send_message(call.message.chat.id, 'Спасибо за оставленную заяку! Наш HR свяжется с вами в '
                                               'ближайшее время!')
    elif call.data == "no":
        bot.send_message(call.message.chat.id, 'Нажмите /reg и пройдите оформление заявки заново!')


bot.polling(none_stop=True, interval=0)
