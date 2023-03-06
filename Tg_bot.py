from telegram.ext import Updater,CommandHandler,CallbackContext,MessageHandler,Filters,CallbackQueryHandler
from telegram import Update,ReplyKeyboardMarkup,KeyboardButton,InlineKeyboardMarkup,InlineKeyboardButton,ChatAdministratorRights
from db import DB
from trsl import lotin_krill
import pytz
from datetime import datetime,timedelta


TOKEN='5655855014:AAFujPMR4kBm5qS4QHVp_eMfy-SoN5kjDdk'

def start(update: Update, context: CallbackContext):
    bot=context.bot 
    chat_id=update.message.chat.id
    print(context.bot)
    db=DB('db.json')
    db.starting(chat_id)
    db.save()
    name=update.message.chat.first_name
    text=f'Aссалому алайкум {name}'
    uz=InlineKeyboardButton('🇺🇿Узбекча',callback_data='til uz')
    ru=InlineKeyboardButton('🇷🇺Руский',callback_data='til ru')
    button=InlineKeyboardMarkup([[uz,ru]])
    bot.sendMessage(chat_id,text,reply_markup=button)

def tekshir(chat_id,bot):
    data=DB('db.json')
    kan1=data.kanal()
    chan1=bot.getChatMember(f'@{kan1[13:]}',str(chat_id))['status']

    if chan1=='left':
        return False
    return True

def til(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_iid=query.message.message_id
    lang = query.data[4:]
    bot = context.bot
    db=DB('db.json')
    db.get_til(str(chat_id),lang)
    kan1=db.kanal()
    if lang=='uz':
        text='Ботдан тўлиқ фойдаланиш учун каналга обуна бўлинг ва текшириш тугмасини босинг.'
        obuna = InlineKeyboardButton('1-Канал',callback_data='obuna 1', url=kan1)
        tek=InlineKeyboardButton('Текшириш',callback_data='obuna tek')
        button=InlineKeyboardMarkup([[obuna],[tek]])
        bot.edit_message_text(text,chat_id,message_id=message_iid,reply_markup=button)
    else:
        text='Чтобы полноценно использовать бота, подпишитесь на канал и нажмите кнопку подтверждения.'
        obuna = InlineKeyboardButton('Канал 1',callback_data='obuna 1', url=kan1)
        tek=InlineKeyboardButton('Проверять',callback_data='obuna tek')
        button=InlineKeyboardMarkup([[obuna],[tek]])
        bot.edit_message_text(text,chat_id=chat_id,message_id=message_iid,reply_markup=button)
    db.save()

def main(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_iid=query.message.message_id
    data = query.data.split()
    user_name = query.from_user.username
    bot = context.bot
    db=DB('db.json')
    check=tekshir(chat_id,bot)
    kan1=db.kanal()
    admins=db.get_admins()
    if check:
        if db.til(chat_id)=='uz':
            text='Бўлимлардан бирини танланг'
            ramazon=InlineKeyboardButton('☪️ Рўза вақтини билиш',callback_data='menu ramazan')
            namoz=InlineKeyboardButton('🕋 Намоз вақтини билиш',callback_data='menu namoz')
            eslatma=InlineKeyboardButton('Тил 🇺🇿/🇷🇺', callback_data='menu til')
            rasm=InlineKeyboardButton('🖼Расмли табрик', callback_data='menu rasm')
            buttons=[[ramazon,namoz],[rasm,eslatma]]
            print(user_name)
            if user_name in admins:
                admin_panel=InlineKeyboardButton('Admin Panel', callback_data='panel b')
                buttons.append([admin_panel])
            btn=InlineKeyboardMarkup(buttons)
            bot.edit_message_text(text,chat_id,message_id=message_iid,reply_markup=btn)
        else:
            text='Выберите один из разделов'
            ramazon=InlineKeyboardButton('☪️ Узнать время поста', callback_data='menu ramazan')
            namoz=InlineKeyboardButton('🕋 Узнать время намаза',callback_data='menu namoz')
            eslatma=InlineKeyboardButton('Язык 🇺🇿/🇷🇺', callback_data='menu til')
            button=[[ramazon,namoz],[eslatma]]
            if user_name in admins:
                admin_panel=InlineKeyboardButton('Admin Panel ru', callback_data='panel b')
                button.append([admin_panel])
            button=InlineKeyboardMarkup(button)
            bot.edit_message_text(text,chat_id,message_id=message_iid,reply_markup=button)
    else:
        if db.til(chat_id):
            text='Обунада хатолик‼️'
            text2='Ботдан тўлиқ фойдаланиш учун каналга обуна бўлинг ва текшириш тугмасини босинг.'
            obuna = InlineKeyboardButton('1-Канал',callback_data='obuna 1', url=kan1)
            tek=InlineKeyboardButton('Текшириш',callback_data='obuna tek')
            button=InlineKeyboardMarkup([[obuna],[tek]])
            bot.sendMessage(chat_id,text)
            bot.sendMessage(chat_id,text2,reply_markup=button)
        else:
            text='Ошибка подписки‼️'
            text2='Чтобы полноценно использовать бота, подпишитесь на канал и нажмите кнопку подтверждения.'
            obuna = InlineKeyboardButton('Канал 1',callback_data='obuna 1', url=kan1)
            tek=InlineKeyboardButton('Проверять',callback_data='obuna tek')
            button=InlineKeyboardMarkup([[obuna],[tek]])
            bot.sendMessage(chat_id,text)
            bot.edit_message_text(text2,chat_id=chat_id,message_id=message_iid,reply_markup=button)
    db.save()


def main_menu(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    bot=context.bot
    message_iid=query.message.message_id
    quer,data=query.data.split()
    db=DB('db.json')
    lang=db.til(chat_id)
    if data=='namoz':
        db.add_amal(chat_id,'namoz')
        if lang=='uz':
            text='Танланг'
            shahar=InlineKeyboardButton('Шаҳарлар',callback_data='data shahar')
            lokatsiya=InlineKeyboardButton('Жойлашув',callback_data='joy lokatsiya')
            main=InlineKeyboardButton('Бош мену',callback_data='obuna main')
            buttons=InlineKeyboardMarkup([[shahar,lokatsiya],[main]])
            bot.edit_message_text(text,chat_id=chat_id,message_id=message_iid,reply_markup=buttons)
        else:
            text='Выбирать'
            shahar=InlineKeyboardButton('Города',callback_data='data shahar')
            lokatsiya=InlineKeyboardButton('Расположение',callback_data='joy lokatsiya')
            main=InlineKeyboardButton('Главное меню',callback_data='obuna main')
            buttons=InlineKeyboardMarkup([[shahar,lokatsiya],[main]])
            bot.edit_message_text(text,chat_id=chat_id,message_id=message_iid,reply_markup=buttons)
    elif data=='til':
        if lang=='uz':
            text='Тилни танланг'
            uz=InlineKeyboardButton('🇺🇿Узбекча',callback_data='yazik uz')
            ru=InlineKeyboardButton('🇷🇺Руский',callback_data='yazik ru')
            btn=InlineKeyboardMarkup([[uz,ru]])
            bot.edit_message_text(text,chat_id=chat_id,message_id=message_iid,reply_markup=btn)
        else:
            text='Выберите язык'
            uz=InlineKeyboardButton('🇺🇿Узбекча',callback_data='yazik uz')
            ru=InlineKeyboardButton('🇷🇺Руский',callback_data='yazik ru')
            btn=InlineKeyboardMarkup([[uz,ru]])
            bot.edit_message_text(text,chat_id=chat_id,message_id=message_iid,reply_markup=btn)
    elif data=='ramazan':
        db.add_amal(chat_id,'ramazon')
        if lang=='uz':
            text='Танланг'
            shahar=InlineKeyboardButton('Шаҳарлар',callback_data='data shahar')
            lokatsiya=InlineKeyboardButton('Жойлашув',callback_data='joy lokatsiya')
            main=InlineKeyboardButton('Бош мену',callback_data='obuna main')
            buttons=InlineKeyboardMarkup([[shahar,lokatsiya],[main]])
            bot.edit_message_text(text,chat_id=chat_id,message_id=message_iid,reply_markup=buttons)
        else:
            text='Выбирать'
            shahar=InlineKeyboardButton('Города',callback_data='data shahar')
            lokatsiya=InlineKeyboardButton('Расположение',callback_data='joy lokatsiya')
            main=InlineKeyboardButton('Главное меню',callback_data='obuna main')
            buttons=InlineKeyboardMarkup([[shahar,lokatsiya],[main]])
            bot.edit_message_text(text,chat_id=chat_id,message_id=message_iid,reply_markup=buttons)
    else:
        if lang=='uz':
            text='Танланг'
            shahar=InlineKeyboardButton('s',callback_data='rasm shahar')
            lokatsiya=InlineKeyboardButton('Жойлашув',callback_data='rasm lokatsiya')
            main=InlineKeyboardButton('Бош мену',callback_data='obuna main')
            buttons=InlineKeyboardMarkup([[shahar,lokatsiya],[main]])
            bot.edit_message_text(text,chat_id=chat_id,message_id=message_iid,reply_markup=buttons)
        else:
            text='Выбирать'
            shahar=InlineKeyboardButton('Города',callback_data='ram shahar')
            lokatsiya=InlineKeyboardButton('Расположение',callback_data='ram lokatsiya')
            main=InlineKeyboardButton('Главное меню',callback_data='obuna main')
            buttons=InlineKeyboardMarkup([[shahar,lokatsiya],[main]])
            bot.edit_message_text(text,chat_id=chat_id,message_id=message_iid,reply_markup=buttons)        
    db.save()

def yazik(update:Update,context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    bot=context.bot
    message_iid=query.message.message_id
    quer,data=query.data.split()
    db=DB('db.json')
    db.get_til(chat_id,data)
    user_name=query.from_user.first_name
    admins=db.get_admins()
    if data=='uz':
        text='Бўлимлардан бирини танланг'
        ramazon=InlineKeyboardButton('☪️ Рўза вақтини билиш',callback_data='menu ramazan')
        namoz=InlineKeyboardButton('🕋 Намоз вақтини билиш',callback_data='menu namoz')
        eslatma=InlineKeyboardButton('Тил 🇺🇿/🇷🇺', callback_data='menu til')
        rasm=InlineKeyboardButton('🖼Расмли табрик', callback_data='menu rasm')
        button=[[ramazon,namoz],[rasm,eslatma]]
        if user_name in admins:
            admin_panel=InlineKeyboardButton('Admin Panel', callback_data='panel b')
            button.append([admin_panel])
        button=InlineKeyboardMarkup(button)
        bot.edit_message_text(text,chat_id,message_id=message_iid,reply_markup=button)
    else:
        text='Выберите один из разделов'
        ramazon=InlineKeyboardButton('☪️ Узнать время поста', callback_data='menu ramazan')
        namoz=InlineKeyboardButton('🕋 Узнать время намаза',callback_data='menu namoz')
        eslatma=InlineKeyboardButton('Язык 🇺🇿/🇷🇺', callback_data='menu til')
        button=[[ramazon,namoz],[eslatma]]
        if user_name in admins:
            admin_panel=InlineKeyboardButton('Admin Panel ru', callback_data='panel b')
            button.append([admin_panel])
        button=InlineKeyboardMarkup(button)
        bot.edit_message_text(text,chat_id,message_id=message_iid,reply_markup=button)
  
def lokatsiya(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    bot=context.bot
    message_iid=query.message.message_id
    quer,data=query.data.split()
    db=DB('db.json')
    lang=db.til(chat_id)
    buttons=[[]]
    city=db.get_city()
    n=db.get_page(chat_id)
    for c in range(6):
        buttons[-1].append(InlineKeyboardButton(text=f"{lotin_krill(city[n+c]['city'])}", callback_data=f"lok {city[c]['lat']}/{city[c]['lng']}"))
        buttons[-1].append(InlineKeyboardButton(text=f"{lotin_krill(city[n-c]['city'])}", callback_data=f"lok {city[c+2]['lat']}/{city[c+2]['lng']}"))
        buttons.append([])
    buttons[-1].append(InlineKeyboardButton(text='Keyingi', callback_data='tan next'))
    buttons.append([InlineKeyboardButton(text='Bosh menu', callback_data='obuna main')])
    text='Shaharni tanlang'
    buttons=InlineKeyboardMarkup(buttons)
    db.add_page(chat_id,n+6)
    db.save()
    bot.edit_message_text(text,chat_id,message_id=message_iid,reply_markup=buttons)

def tan_call(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id=query.message.message_id
    bot = context.bot
    query,data = query.data.split(' ')
    if data=='back':
        db=DB('db.json')
        buttons=[[]]
        city=db.get_city()
        n=db.get_page(chat_id)
        for c in range(6):
            buttons[-1].append(InlineKeyboardButton(text=f"{lotin_krill(city[c+n]['city'])}", callback_data=f"lok {city[c]['lat']}/{city[c]['lng']}"))
            buttons[-1].append(InlineKeyboardButton(text=f"{lotin_krill(city[n-c]['city'])}", callback_data=f"lok {city[c+2]['lat']}/{city[c+2]['lng']}"))
            buttons.append([])
            i+=1
        buttons[-1].append(InlineKeyboardButton(text='Oraga', callback_data='tan back'))
        buttons[-1].append(InlineKeyboardButton(text='Keyingi', callback_data='tan next'))
        buttons.append([InlineKeyboardButton(text='Bosh menu', callback_data='obuna main')])
        buttons=InlineKeyboardMarkup(buttons)
        bot.edit_message_reply_markup(chat_id,message_id,reply_markup=buttons)
        db.add_page(chat_id,n-6)
        db.save()
    else:
        db=DB('db.json')
        buttons=[[]]
        city=db.get_city()
        n=db.get_page(chat_id)
        for c in range(6):
            buttons[-1].append(InlineKeyboardButton(text=f"{lotin_krill(city[n+c]['city'])}", callback_data=f"lok {city[c]['lat']}/{city[c]['lng']}"))
            buttons[-1].append(InlineKeyboardButton(text=f"{lotin_krill(city[n-c]['city'])}", callback_data=f"lok {city[c+2]['lat']}/{city[c+2]['lng']}"))
            buttons.append([])
        buttons[-1].append(InlineKeyboardButton(text='Oraga', callback_data='tan back'))
        buttons[-1].append(InlineKeyboardButton(text='Keyingi', callback_data='tan next'))
        buttons.append([InlineKeyboardButton(text='Bosh menu', callback_data='obuna main')])
        buttons=InlineKeyboardMarkup(buttons)
        bot.edit_message_reply_markup(chat_id,message_id,reply_markup=buttons)
        db.add_page(chat_id,n+6)
        db.save()
    
def joylashuv(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id=query.message.message_id
    date=query.message.date
    date=str(date.strftime('%d-%m-%Y'))
    bot = context.bot
    query,data = query.data.split(' ')
    db=DB('db.json')
    til=db.til(chat_id)
    ans=db.get_d(chat_id,date)
    print(ans)
    db.save()
    if til=='uz':
        bot.edit_message_text(lotin_krill('Joylashuvinggizni yuboring'),chat_id=chat_id,message_id=message_id)
    else:
        bot.edit_message_text('Отправьте свое местоположение',chat_id=chat_id,message_id=message_id)        

def malumot(update: Update, context: CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    message_id=query.message.message_id
    dat=query.message.date
    bot = context.bot
    date=str(dat.strftime('%d-%m-%Y'))
    query,data = query.data.split(' ')
    lat,lng=data.split('/')
    db=DB('db.json')
    amal=db.get_amal(chat_id)
    lang=db.til(chat_id)
    if amal=='namoz':
        taqvim,tz=db.get_d(chat_id,date,lng,lat)
        dat=((dat.replace(tzinfo=pytz.timezone(tz))).strftime('%d-%m-%Y'))
        date=str(dat)
        taqvim,tz=db.get_d(chat_id,date,lng,lat)
        if lang=='uz':
            oy=['Январ','Феврал','Март','Апрел','Май','Июн','Июл','Август','Сентабр','Октабр','Ноябр','Декабр']
            text=f"Сана: {dat[6:]}-йил {dat[:2]}-{oy[int(dat[3:5])-1]}\n Ҳижрий: {taqvim['hijriy']}\nВақт минтақаси: ({tz})\n\n"
            text+=f"Субҳ: (эҳтиётини инобатга олиб белгиланган) {str(timedelta(hours=float(taqvim['Imsak'][:2]), minutes=float(taqvim['Imsak'][3:5]),)-timedelta(minutes=2.0))[:-3]}"
            text+=f"\nБомдод: {taqvim['Fajr']}\nҚуёш: {taqvim['Sunrise'][:5]}\n\nПешин: {taqvim['Dhuhr'][:5]}\n\nАср: {str(timedelta(hours=float(taqvim['Asr'][:2]),minutes=float(taqvim['Asr'][3:5]))-timedelta(minutes=48.0))[:-3]}\n\n"
            text+=f"Шом: {str(timedelta(hours=float(taqvim['Maghrib'][:2]), minutes=float(taqvim['Maghrib'][3:5]),)-timedelta(minutes=4.0))[:-3]}\nАввобийн: Шом намозидан кейин*"
            text+=f"\n\nХуфтон: {taqvim['Isha'][:5]}\n\n\n"
            text+=f'______\nНамоз ва Рўза вақтларига уланиш'
            bugun=InlineKeyboardButton('Бугун',callback_data='bug current')
            ertaga=InlineKeyboardButton('Эртага',callback_data='bug tomorrow')
            btn=InlineKeyboardMarkup([[bugun,ertaga]])
            bot.sendMessage(chat_id,text,reply_markup=btn)
        else:
            oy=['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
            text=f"Дата: {dat[6:]}-год {dat[3:5]}-{oy[int(dat[3:5])-1]}\n По хиджре: {taqvim['hijriy']}\nЧасовой пояс: ({tz})\n\n"
            text+=f"Фаджр: (время фаджра указано с учетом упреждения пропуска его наступления) {str(timedelta(hours=float(taqvim['Imsak'][:2]), minutes=float(taqvim['Imsak'][3:5]),)-timedelta(minutes=2.0))[:-3]}"
            text+=f"\nУтренний (предрассветный) намаз: {taqvim['Fajr']}\nВосход: {taqvim['Sunrise'][:5]}\n\nЗухр: {taqvim['Dhuhr'][:5]}\n\nАср: {str(timedelta(hours=float(taqvim['Asr'][:2]),minutes=float(taqvim['Asr'][3:5]))-timedelta(minutes=48.0))[:-3]}\n\n"
            text+=f"Магриб: {str(timedelta(hours=float(taqvim['Maghrib'][:2]), minutes=float(taqvim['Maghrib'][3:5]),)-timedelta(minutes=4.0))[:-3]}\nАввабин: После вечерней молитвы магриб*"
            text+=f"\n\nИша: {taqvim['Isha'][:5]}\n\n\n"
            text+=f'_______\nУзнать время Намаза и Поста'
            bugun=InlineKeyboardButton('Сегодня',callback_data='bug current')
            ertaga=InlineKeyboardButton('завтра',callback_data='bug tomorrow')
            btn=InlineKeyboardMarkup([[bugun,ertaga]])
            bot.sendMessage(chat_id,text,reply_markup=btn)          
    else:
        taqvim,tz=db.get_d(chat_id,date,lng,lat)
        dat=((dat.replace(tzinfo=pytz.timezone(tz))).strftime('%d-%m-%Y'))
        date=str(dat)
        taqvim,tz=db.get_d(chat_id,date,lng,lat)
        if lang=='uz':
            oy=['Январ','Феврал','Март','Апрел','Май','Июн','Июл','Август','Сентабр','Октабр','Ноябр','Декабр']
            text=f"Сана: {dat[6:]}-йил {dat[0:2]}-{oy[int(dat[3:5])-1]}\n Ҳижрий: {taqvim['hijriy']}\nВақт минтақаси: ({tz})\n\n"
            text+=f"Саҳарлик (оғиз ёпиш) вақти: {str(timedelta(hours=float(taqvim['Imsak'][:2]), minutes=float(taqvim['Imsak'][3:5]),)-timedelta(minutes=2.0))[:-3]}"
            text+=f"\nВремя ифтара: {str(timedelta(hours=float(taqvim['Maghrib'][:2]), minutes=float(taqvim['Maghrib'][3:5]),)-timedelta(minutes=4.0))[:-3]}\n"
            text+=f"___\n*Саҳарлик вақти эҳтиётини инобатга олиб белгиланган."
            text+=f'______\nНамоз ва Рўза вақтларига уланиш'
            bugun=InlineKeyboardButton('Бугун',callback_data='ift current')
            ertaga=InlineKeyboardButton('Эртага',callback_data='ift tomorrow')
            btn=InlineKeyboardMarkup([[bugun,ertaga]])
            bot.sendMessage(chat_id,text,reply_markup=btn)
        else:
            oy=['Январь','Февраль','Март','Апрель','Май','Июнь','Июль','Август','Сентябрь','Октябрь','Ноябрь','Декабрь']
            text=f"Дата: {dat[6:]}-год {dat[0:2]}-{oy[int(dat[3:5])-1]}\n По хиджре: {taqvim['hijriy']}\nЧасовой пояс: ({tz})\n\n"
            text+=f"Сахар (закрытие рта) время: {str(timedelta(hours=float(taqvim['Imsak'][:2]), minutes=float(taqvim['Imsak'][3:5]),)-timedelta(minutes=2.0))[:-3]}"
            text+=f"\nВремя ифтара: {str(timedelta(hours=float(taqvim['Maghrib'][:2]), minutes=float(taqvim['Maghrib'][3:5]),)-timedelta(minutes=4.0))[:-3]}\n"
            text+=f"___\n*Утреннее время определено с учетом осторожности."
            text+=f'_______\nУзнать время Намаза и Поста'
            bugun=InlineKeyboardButton('Сегодня',callback_data='ift current')
            ertaga=InlineKeyboardButton('завтра',callback_data='ift tomorrow')
            btn=InlineKeyboardMarkup([[bugun,ertaga]])
            bot.sendMessage(chat_id,text,reply_markup=btn)    
def admin(update:Update,context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    bot=context.bot
    message_id=query.message.message_id
    dat=query.message.date
    db=DB('db.json')
    lang=db.til(chat_id)
    if lang=='uz':
        text='Tanlang'
        send_msg=InlineKeyboardButton('Xabar yuborish',callback_data='admin send')
        statistic=InlineKeyboardButton('Bot statistikasi',callback_data='admin stc')
        add_admin=InlineKeyboardButton('Admin qo\'shish',callback_data='admin add')
        add_channel=InlineKeyboardButton('Kanal qo\'shish',callback_data='admin channel')
        btn=InlineKeyboardMarkup([[send_msg,statistic],[add_admin,add_channel]])
        bot.sendMessage(chat_id,text,reply_markup=btn)
    else:
        text='Tanlang'
        send_msg=InlineKeyboardButton('Отправить сообщение',callback_data='admin send')
        statistic=InlineKeyboardButton('Статистика бота',callback_data='admin stc')
        add_admin=InlineKeyboardButton('Добавить администратора',callback_data='admin add')
        add_channel=InlineKeyboardButton('Добавить канал',callback_data='admin channel')
        btn=InlineKeyboardMarkup([[send_msg,statistic],[add_admin,add_channel]])
        bot.sendMessage(chat_id,text,reply_markup=btn)
    db.save()

def admin_command(update:Update,context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    bot=context.bot
    user_name = query.from_user.username
    message_id=query.message.message_id
    dat=query.message.date
    query,data=query.data.split()
    db=DB('db.json')
    lang=db.til(chat_id)
    admins=db.get_admins()
    if lang=='uz':
        if data=='stc':
            text=f'Bot foydalanuvchilari soni: {db.get_members()}'
            bot.sendMessage(chat_id,text)
            text='Бўлимлардан бирини танланг'
            ramazon=InlineKeyboardButton('☪️ Рўза вақтини билиш',callback_data='menu ramazan')
            namoz=InlineKeyboardButton('🕋 Намоз вақтини билиш',callback_data='menu namoz')
            eslatma=InlineKeyboardButton('Тил 🇺🇿/🇷🇺', callback_data='menu til')
            rasm=InlineKeyboardButton('🖼Расмли табрик', callback_data='menu rasm')
            button=[[ramazon,namoz],[rasm,eslatma]]
            if user_name in admins:
                admin_panel=InlineKeyboardButton('Admin Panel', callback_data='panel b')
                button.append([admin_panel])
            button=InlineKeyboardMarkup(button)
            bot.sendMessage(text,chat_id,reply_markup=button)
        elif data=='add':
            text='Aдмин қо`шиш учун админ усернамени <Admin:@username> ко`ринишида киритинг'
            bot.sendMessage(chat_id,text)
        elif data=='channel':
            text='Канални қо`шиш учун аввал каналга админ қилинг ва со`нг канал линкини <Kanal:@username> ко`ринишида юборинг'
            bot.sendMessage(chat_id,text)
        else:
            text='Бот фойдаланувчиларига хабар жўнатиш'
            textily=InlineKeyboardButton('Матнли хабар',callback_data='send text')
            imgliy=InlineKeyboardButton('Расмли ҳабар',callback_data='send img')
            videoliy=InlineKeyboardButton('Видеоли ҳабар',callback_data='send video')
            button=InlineKeyboardMarkup([[textily,imgliy],[videoliy]])
            bot.sendMessage(chat_id,text,reply_makup=button)
    else:
        if data=='stc':
            text=f'Количество пользователей бота: {db.get_members()}'
            bot.sendMessage(chat_id, text)
            text='Выберите один из разделов'
            ramazon=InlineKeyboardButton('☪️ Узнать время поста', callback_data='menu ramazan')
            namoz=InlineKeyboardButton('🕋 Узнать время намаза',callback_data='menu namoz')
            eslatma=InlineKeyboardButton('Язык 🇺🇿/🇷🇺', callback_data='menu til')
            button=[[ramazon,namoz],[eslatma]]
            if user_name in admins:
                admin_panel=InlineKeyboardButton('Admin Panel ru', callback_data='panel b')
                button.append([admin_panel])
            button=InlineKeyboardMarkup(button)
            bot.sendMessage(chat_id,text,reply_markup=button)
        elif data=='add':
            text='Чтобы добавить администратора, введите имя пользователя администратора в форме <Admin:@username>'
            bot.sendMessage(chat_id,text)
        elif data=='channel':
            text='Чтобы добавить канал, сначала выполните администрирование канала, а затем отправьте ссылку на канал как <Kanal:@username>.'
            bot.sendMessage(chat_id,text)
        else:
            text='Отправка сообщений пользователям бота'
            textily=InlineKeyboardButton('Текстовое сообщение',callback_data='send text')
            imgliy=InlineKeyboardButton('Графическое сообщение',callback_data='send img')
            videoliy=InlineKeyboardButton('Видео сообщение',callback_data='send video')
            button=InlineKeyboardMarkup([[textily,imgliy],[videoliy]])
            bot.sendMessage(chat_id,text,reply_markup=button)

def add_command(update:Update,context:CallbackContext):
    bot=context.bot 
    chat_id=update.message.chat.id
    message_id=update.message.message_id
    user_name=update.message.from_user.username
    text=update.message.text
    db=DB('db.json')
    lang=db.til(chat_id)
    admins=db.get_admins()
    if user_name in admins:
        if lang=='ru':
            if text[:5]=='Admin':
                admin_name=text[7:]
                db.add_admin(admin_name)
                text='Администратор успешно добавлен'
                bot.sendMessage(chat_id,text)
                text='Выберите один из разделов'
                ramazon=InlineKeyboardButton('☪️ Узнать время поста', callback_data='menu ramazan')
                namoz=InlineKeyboardButton('🕋 Узнать время намаза',callback_data='menu namoz')
                eslatma=InlineKeyboardButton('Язык 🇺🇿/🇷🇺', callback_data='menu til')
                button=[[ramazon,namoz],[eslatma]]
                if user_name in admins:
                    admin_panel=InlineKeyboardButton('Admin Panel ru', callback_data='panel b')
                    button.append([admin_panel])
                button=InlineKeyboardMarkup(button)
                bot.sendMessage(chat_id,text,reply_markup=button)
            if text[:5] == 'Kanal':
                channel_name=text[7:]
                try:
                    chan1=bot.getChatMember(f'@{channel_name}',str(chat_id))['status']
                except:
                    bot.sendMessage(chat_id,'Kanal qo\'shishda xatolik tekshirib qayta urinib ko\'ring')
                if chan1=='administrator':
                    db.add_kanal(channel_name)
                    bot.send_message(chat_id,'Kanal muvafaqiyatli qo\'shildi')
                    text='Выберите один из разделов'
                    ramazon=InlineKeyboardButton('☪️ Узнать время поста', callback_data='menu ramazan')
                    namoz=InlineKeyboardButton('🕋 Узнать время намаза',callback_data='menu namoz')
                    eslatma=InlineKeyboardButton('Язык 🇺🇿/🇷🇺', callback_data='menu til')
                    button=[[ramazon,namoz],[eslatma]]
                    if user_name in admins:
                        admin_panel=InlineKeyboardButton('Admin Panel ru', callback_data='panel b')
                        button.append([admin_panel])
                    button=InlineKeyboardMarkup(button)
                    bot.sendMessage(text,chat_id,reply_markup=button)
        else:
            if text[:5]=='Admin':
                admin_name=text[7:]
                db.add_admin(admin_name)
                text='Admin muvafaqqiyatli qo\'shildi'
                bot.sendMessage(chat_id,text)
                text='Выберите один из разделов'
                ramazon=InlineKeyboardButton('☪️ Узнать время поста', callback_data='menu ramazan')
                namoz=InlineKeyboardButton('🕋 Узнать время намаза',callback_data='menu namoz')
                eslatma=InlineKeyboardButton('Язык 🇺🇿/🇷🇺', callback_data='menu til')
                button=[[ramazon,namoz],[eslatma]]
                if user_name in admins:
                    admin_panel=InlineKeyboardButton('Admin Panel ru', callback_data='panel b')
                    button.append([admin_panel])
                button=InlineKeyboardMarkup(button)
                bot.sendMessage(text,chat_id,reply_markup=button)
            if text[:5] == 'Kanal':
                channel_name=text[7:]
                try:
                    chan1=bot.getChatMember(f'@{channel_name}',str(chat_id))['status']
                except:
                    bot.sendMessage(chat_id,'Kanal qo\'shishda xatolik tekshirib qayta urinib ko\'ring')
                if chan1=='administrator':
                    db.add_kanal(channel_name)
                    bot.send_message(chat_id,'Kanal muvafaqiyatli qo\'shildi')
                    text='Выберите один из разделов'
                    ramazon=InlineKeyboardButton('☪️ Узнать время поста', callback_data='menu ramazan')
                    namoz=InlineKeyboardButton('🕋 Узнать время намаза',callback_data='menu namoz')
                    eslatma=InlineKeyboardButton('Язык 🇺🇿/🇷🇺', callback_data='menu til')
                    button=[[ramazon,namoz],[eslatma]]
                    if user_name in admins:
                        admin_panel=InlineKeyboardButton('Admin Panel ru', callback_data='panel b')
                        button.append([admin_panel])
                    button=InlineKeyboardMarkup(button)
                    bot.sendMessage(text,chat_id,reply_markup=button)
    db.save()

def query_send(update:Update,context:CallbackContext):
    query = update.callback_query
    chat_id = query.message.chat_id
    bot=context.bot
    message_id=query.message.message_id
    db=DB('db.json')
    qury,msg=query.data.split()
    lang=db.til(chat_id)
    if lang=='uz':
        if msg=='text':
            text='Матнли хабар жўнатиш учун <Text:Жўнатмоқчи бўлган хабар матнинггиз> кўринишида юборасиз'
            bot.send_message(chat_id,text)
        elif msg=='img':
            text='Расмли хабарни юбориш учун биринчи расмни юборасиз сўнг <Img Text:Расм пастидаги матн> кўринишида юборинг'
            bot.send_message(chat_id,text)
        else:
            text='Видео хабарни юбориш учун биринчи видеони юборасиз сўнг <Video Text:Видео пастидаги матн> кўринишида юборинг'
            bot.sendMessage(chat_id,text)
    else:
        if msg=='text':
            text='Чтобы отправить текстовое сообщение, введите <Text:Текст сообщения, которое вы хотите отправить>'
            bot.send_message(chat_id,text)
        elif msg=='img':
            text='Чтобы отправить графическое сообщение, вы сначала отправляете изображение, а затем отправляете его как <Img Text: Текст под изображением>'
            bot.send_message(chat_id,text)
        else:
            text='Чтобы отправить видеосообщение, вы сначала отправляете видео, а затем отправляете его как <Video Text: Текст под видео>'
            bot.sendMessage(chat_id,text)


# def admin_send(update:Update,context:CallbackContext):
    
    

            


   
    







updater=Updater(TOKEN)

updater.dispatcher.add_handler(CommandHandler('start',start))
updater.dispatcher.add_handler(CallbackQueryHandler(til,pattern='til'))
updater.dispatcher.add_handler(CallbackQueryHandler(main,pattern='obuna'))
updater.dispatcher.add_handler(CallbackQueryHandler(main_menu,pattern='menu'))
updater.dispatcher.add_handler(CallbackQueryHandler(lokatsiya,pattern='data'))
updater.dispatcher.add_handler(CallbackQueryHandler(tan_call,pattern='tan'))
updater.dispatcher.add_handler(CallbackQueryHandler(joylashuv,pattern='joy'))
updater.dispatcher.add_handler(CallbackQueryHandler(malumot,pattern='lok'))
updater.dispatcher.add_handler(CallbackQueryHandler(yazik,pattern='yazik'))
updater.dispatcher.add_handler(CallbackQueryHandler(admin,pattern='panel'))
updater.dispatcher.add_handler(CallbackQueryHandler(admin_command,pattern='admin'))
updater.dispatcher.add_handler(MessageHandler(Filters.text,add_command))





updater.start_polling()
updater.idle()