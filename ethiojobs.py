
from datetime import datetime
import telebot
from telebot import types
from bs4 import BeautifulSoup
from datetime import datetime
from telebot.types import InlineKeyboardMarkup,InlineKeyboardButton
from constants import API_KEY
from telegram import ParseMode
from telegram.ext import *
import requests
import json
bot = telebot.TeleBot(API_KEY,parse_mode=None)
headers ={'User-Agent':'Mozilla/5.0 (X11; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'}

def markup_inline():
    markup = InlineKeyboardMarkup()
    markup.width =3
    tabs=requests.get('https://www.ethiojobs.net/',headers=headers).text
    souplist =BeautifulSoup(tabs,'lxml')
    jobitems =souplist.find_all(class_='list-group-item')
    
   
        
    for i in range(0,len(jobitems)-1,2):
        jobitem1 =jobitems[i]
        jobitem2 =jobitems[i+1]
        li1=str(jobitem1['href'])
        te1=''.join(jobitem1.text.split()[:-1])
        
        li1=li1.replace('https://www.ethiojobs.net/browse-by-category','b')
        li1=li1.replace('https://www.ethiojobs.net/find-jobs-in-ethiopia','a')


        li2=str(jobitem2['href'])
        te2=''.join(jobitem2.text.split()[:-1])
        
        li2=li2.replace('https://www.ethiojobs.net/browse-by-category','b')
        li2=li2.replace('https://www.ethiojobs.net/find-jobs-in-ethiopia','a')
        
        
        markup.add(
                InlineKeyboardButton(te1,callback_data=li1),
                InlineKeyboardButton(te2,callback_data=li2),
                )
       

    return markup

def generate_info(lin,user_id,k,d):
    lin+='?listings_per_page=5&view=list&page='+k
    if lin[0]=='a':
        lin='https://www.ethiojobs.net/find-jobs-in-ethiopia'+lin[1:]
    else:
        lin='https://www.ethiojobs.net/browse-by-category'+lin[1:]
    html_text = requests.get(lin,headers=headers).text
    soup =BeautifulSoup(html_text,'lxml')
    jobs=soup.find_all(class_ ="listing-section")

    markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    btn1 = types.KeyboardButton("/jobcategory")
    btn3 = types.KeyboardButton("/help")
    markup.add(btn1,btn3)
    
    for job in jobs :
        title = job.find('h2').text.strip()
        company_name =job.find(class_ ="company-name").text.strip()
        work_place = job.find(class_ = "work-palce captions-field").text.strip()
        Deadline_date =job.find(class_ ='text-danger captions-field').text.strip()
        Deadline_date=' '.join(Deadline_date.replace(',','').split(' '))
        mydate=datetime.strptime(Deadline_date,'%b %d %Y')
        x= mydate - datetime.now()
        Deadline_date=str(x).split(',')[0]+" left"
            
        level=job.find_all(class_='captions-field')[-2].text.strip()
        viewDetails=job.find(class_='viewDetails').a['href']
        tet="  "+title+ "\ncompany :-> " + company_name +'\nwork_place :-> ' + work_place + '\nlevel  :-> ' + level +'\nDeadline_date :->  ' +Deadline_date +'\nview details ->' + viewDetails
        bot.send_message(chat_id=user_id,text=tet,reply_markup=markup)
        
    a=d
    try:
          print("it is working")
          bot.delete_message(chat_id=user_id, message_id=a-1)
          bot.delete_message(chat_id=user_id, message_id=a-2)
          bot.delete_message(chat_id=user_id, message_id=a-3)
          bot.delete_message(chat_id=user_id, message_id=a-4)
          bot.delete_message(chat_id=user_id, message_id=a-5)
          bot.delete_message(chat_id=user_id, message_id=a-6)
    except:
        print(a)
        pass



@bot.message_handler(commands=['start','jobcategory'])
def send_welcome(msg):
    markup = types.ReplyKeyboardMarkup(row_width=2,resize_keyboard=True)
    btn1 = types.KeyboardButton("/jobcategory")
    btn3 = types.KeyboardButton("/help")
    markup.add(btn1,btn3)
    bot.reply_to(msg,"loading ..",reply_markup =markup)
    try:
        bot.reply_to(msg,"it is good to see you well come",reply_markup =markup_inline())
    except:
         bot.send_message(chat_id=msg.chat.id,text='sorry the website not workiing now',reply_markup =markup)
         return 0

    bot.send_message(chat_id=msg.chat.id,text='select 🤞',reply_markup =markup)

@bot.callback_query_handler(func=lambda message : True)
def callback_query(call):
    da=call.data[:]
    
    if  da[-1] not in '0123456789':
        da +='=1'
    x=da.split('=')
    y=x[:]
    generate_info(da,call.from_user.id,x[-1],call.message.id)
   
    a=str(int(x[-1])+1)
    pre=str(int(x[-1])-1)
   
    if int(x[-1]) <= 1:
        pre='1'
    x.pop()
    y.pop()
    x.append(a)
    y.append(pre)
    da="=".join(x)
    ad="=".join(y)
     
    markup = InlineKeyboardMarkup()
    markup.width =1
    markup.add(
                InlineKeyboardButton('######### Next ###############',callback_data=da),
                InlineKeyboardButton('######### previous ###############',callback_data=ad),
                )
    bot.send_message(chat_id=call.from_user.id,text=da.split("=")[-1],reply_markup=markup)
    
    


@bot.message_handler(commands=['help'])
def helpmessage(msg):
    bot.send_message(chat_id=msg.chat.id,text='please enter jobcategory command one you inter press the button what you want\n\n\n thanx')

bot.polling()
