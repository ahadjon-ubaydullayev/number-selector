from django.shortcuts import render, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from telethon import TelegramClient, sync
from telebot import *
import telebot
import pandas as pd
from .models import UserAction, SimOrder


bot = TeleBot("5264267121:AAFu4trfmIxuTza4y9IgSJ-fCSkmUf7nIrs")


@csrf_exempt
def index(request):
    if request.method == 'GET':
        return HttpResponse("Bot Url My Page")
    elif request.method == 'POST':
        bot.process_new_updates([
            telebot.types.Update.de_json(
                request.body.decode("utf-8")
            )
        ])
        return HttpResponse(status=200)


@bot.message_handler(commands=['start'])
def greeting(message):
    main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton('Raqam tanlash')
    main_markup.add(btn)
    bot.send_message(message.from_user.id,
                  'Salom.\nBotga xush kelibsiz!\nBot sizga yordam beradi.', reply_markup=main_markup)
    


@bot.message_handler(func=lambda message: True)
def main_view(message):

    step = UserAction.objects.first()
    # sim_order = SimOrder.objects.get(user_id=message.from_user.id)
    numbers = read_file()
    selected = []
    main_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    back = types.KeyboardButton("Orqaga")
    cancel = types.KeyboardButton("Bekor qilish")
    main_markup.add(back, cancel)

    sim_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    beeline = types.KeyboardButton("Beeline")
    uzmobile = types.KeyboardButton("Uzmobile")
    sim_markup.add(beeline, uzmobile)

    confirm_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    confirm = types.KeyboardButton("Tasdiqlash")
    cancel = types.KeyboardButton("Bekor qilish")
    confirm_markup.add(confirm, cancel)
    
    list_order = ['Beeline', 'Uzmobile']
    orders = ['Beeline', 'Uzmobile', 'Raqam tanlash', 'Orqaga', 'Bekor qilish']

    if message.text == "Raqam tanlash":
        bot.send_message(message.from_user.id, "Kerakli kompaniyani tanlang:", reply_markup=sim_markup)

    if message.text == "Beeline":
        bot.send_message(message.from_user.id, "Sevimli raqamingizni kiriting.\nMisol: 9999", reply_markup=main_markup) 
        step.user_action = 1
        step.save()

    if message.text == "Uzmobile":
        bot.send_message(message.from_user.id, "Sevimli raqamingizni kiriting.\nMisol: 9999", reply_markup=main_markup)
        step.user_action = 1
        step.save()
        
    if message.text == "Orqaga":
        step.user_action = 0
        step.save()
        bot.send_message(message.from_user.id, "Kerakli kompaniyani tanlang:", reply_markup=sim_markup)

    if message.text == "Yo'q":
        step.user_action = 0
        step.save()
        bot.send_message(message.from_user.id, "Kerakli kompaniyani tanlang:", reply_markup=sim_markup)

    if message.text == "Bekor qilish":
        step.user_action = 0
        step.save()
        bot.send_message(message.from_user.id, "Kerakli kompaniyani tanlang:", reply_markup=sim_markup)

    if message.text == "Tasdiqlash":
        bot.send_message(message.from_user.id, "Buyurtmangiz qabul qilindi", reply_markup=sim_markup)

    if step.user_action == 1:
        if message.text not in list_order:
            for number in numbers:
                number = str(number)
                if message.text in number: 
                    selected.append(number)
                    
        if len(selected) != 0:
            step.user_action = 0
            step.save()
            markup_numbers = types.InlineKeyboardMarkup(row_width=1)
            for number in selected:
                markup_numbers.add(types.InlineKeyboardButton(f"{number}", callback_data=f"{number}"))
            bot.send_message(message.from_user.id, f"Siz qidirgan raqam:", reply_markup=markup_numbers)
        else:
            if message.text not in orders:
                step.user_action = 0
                step.save()
                bot.send_message(message.from_user.id, f"Siz qidirgan raqam bizda hozircha mavjud emas.\nIltimos boshqa raqam terib qaytadan urinib ko'ring.", reply_markup=sim_markup)
   
    orders = SimOrder.objects.filter(user_id=message.from_user.id, active=True).first()

    if orders != None:
        order = SimOrder.objects.filter(user_id=message.from_user.id, active=True).first()           
        
    else:
        order = SimOrder.objects.create(user_id=message.from_user.id, active=True)

    if message.text == "Ha":
        order.order_step = 1
        order.save()
        bot.send_message(message.from_user.id, "Ism familiyangizni kiriting:")  
    
    elif order.order_step == 1:
        order.full_name = message.text
        order.order_step += 1
        order.save()
        bot.send_message(message.from_user.id, "Telefon raqamingizni kiriting:")

    elif order.order_step == 2:
        if str(message.text).isdigit():
            order.tel_number = message.text
            order.order_step += 1
            order.save()
            bot.send_message(message.from_user.id, "To'liq manzilingizni kiriting:")
        else:
            bot.send_message(message.from_user.id,
                             'Iltimos to\'g\'ri ma\'lumot kiriting🙅‍♂️')
        
    
    elif order.order_step == 3:
        order.full_address = message.text
        order.order_cost = "200 ming so'm"
        order.order_step = 0
        order.save()
        bot.send_message(message.from_user.id, "Ma'lumotlar to'g'rimi?")
        bot.send_message(message.from_user.id, f"Ism: {order.full_name}\nTelefon raqam: {order.full_name}\nBuyurtma: {order.order_number}\nManzil: {order.full_address}", reply_markup=confirm_markup)


@bot.callback_query_handler(func=lambda call: True)
def call_data(call):
    order = SimOrder.objects.filter(user_id=call.from_user.id, active=True).first()
    order.order_number = call.data
    order.save()
    request_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    ha = types.KeyboardButton("Ha")
    yoq = types.KeyboardButton("Yo'q")
    request_markup.add(ha, yoq)
    number = str(call.data)
    bot.send_message(call.from_user.id, f"Raqam: {number}\nUnits 22000, Milliy 50, Milliy 70, Milliy 100 va Milliy VIP tarif rejalariga ulash mumkin.\nUshbu raqamga buyurtma berishini xohlaysizmi?", reply_markup=request_markup)

 
def read_file():
    file_name = 'numbers.xlsx'
    sheet = 'number'
    df = pd.read_excel(io=file_name, sheet_name=sheet, usecols='A')
    number_list = df['numbers'].tolist()
    return number_list
