from telebot import async_telebot, types
from rubpy import Client, methods
from rubpy.crypto import Crypto
from config import token, admin, rubika_session
import os, requests, time, json, sys, asyncio, random

bot = async_telebot.AsyncTeleBot("6406574208:AAFzkKOHtAsFauTmhG8tsJcMK4Y1cd-X3jA")
database = {}
rubika = {}

def sendMessage(chat_id, text, parse_mode, message_id, reply_markup=None):
  send_message = bot.send_message(chat_id=chat_id, text=text, parse_mode=parse_mode, reply_to_message_id=message_id, reply_markup=reply_markup)
  return send_message
  
def editMessage(chat_id, text, parse_mode, message_id, reply_markup=None):
  edit_message_text = bot.edit_message_text(chat_id=chat_id, text=text, parse_mode=parse_mode, message_id=message_id, reply_markup=reply_markup)
  return edit_message_text
  
def sendDocument(chat_id, document):
  send_document = bot.send_document(chat_id=chat_id, document=document)
  return send_document
  
def answerCallbackQuery(callback_query_id, text, show_alert):
  answer_callback_query = bot.answer_callback_query(callback_query_id=callback_query_id, text=text, show_alert=show_alert)
  return answer_callback_query
  
def deleteMessage(chat_id, message_id):
  delete_message = bot.delete_message(chat_id=chat_id, message_id=message_id)
  return delete_message
  
def inlineButton(name, data):
  inline_keyboard_button = types.InlineKeyboardButton(text=name, callback_data=data)
  return inline_keyboard_button
  
def inlineButtonUrl(name, url):
  inline_keyboard_button = types.InlineKeyboardButton(text=name, url=url)
  return inline_keyboard_button
  
def inlineKeyboard(data):
  keyboard = types.InlineKeyboardMarkup()
  if data == "start":
    if database['session'] != None:
      keyboard.row(inlineButton("📤 ارسال پیام", 'send_message')),
      keyboard.row(inlineButton("❎ حذف مخاطبین", 'delete_contacts'), inlineButton("✅ افزودن مخاطبین", 'add_contacts')),
      keyboard.row(inlineButton("♻️ چکر شماره", 'numbers_checker')),
      keyboard.row(inlineButton("🧩 اپشن های سندر", 'options'), inlineButton("💬 متن پیام", 'message_text')),
      keyboard.row(inlineButton("🌀 استخراج شماره", 'lich_numbers')),
      keyboard.row(inlineButton("🛡 انتی لاگین", 'anti_login'), inlineButton("⭕️ خروج از اکانت", 'logout')),
      keyboard.row(inlineButtonUrl("🪼 Developer : Uranus", 't.me/Uranus_iD'))
    else:
      keyboard.row(inlineButton("📲 ورود", 'import')),
      keyboard.row(inlineButton("🌀 استخراج شماره", 'lich_numbers'), inlineButton("💬 متن پیام", 'message_text')),
      keyboard.row(inlineButtonUrl("🪼 Developer : Uranus", 't.me/Uranus_iD'))
  elif data == "send_message":
    keyboard.row(inlineButton("🗯 ارسال به چت و گروه ها", 'send_chats')),
    keyboard.row(inlineButton("💭 ساخت گروه (ویژه)", 'send_group'), inlineButton("☎️ ارسال به مخاطبین", 'send_contacts')),
    keyboard.row(inlineButton("< بازگشت", 'back_home'))
  elif data == "options":
    last_online_time = database['last_online_time']
    if last_online_time == 21600:
      last_online_type = "6 ساعت پیش"
    elif last_online_time == 43200:
      last_online_type = "12 ساعت پیش"
    elif last_online_time == 86400:
      last_online_type = "1 روز پیش"
    elif last_online_time == 172800:
      last_online_type = "2 روز پیش"
    elif last_online_time == 259200:
      last_online_type = "3 روز پیش"
    elif last_online_time == 604800:
      last_online_type = "7 روز پیش"
    keyboard.row(inlineButton(f"👀 اخرین بازدید کاربران : {last_online_type}", 'last_online_type')),
    keyboard.row(inlineButton(f"⏰ زمان ارسال به هر کاربر : {database['send_time']} ثانیه", 'send_time')),
    keyboard.row(inlineButton(f"🖇 نام گروه : {database['group_name']}", 'group_name')),
    keyboard.row(inlineButton("< بازگشت", 'back_home'))
  elif data == "last_online_type":
    keyboard.row(inlineButton("🕰 6 ساعت پیش", 'lastonline_6hago')),
    keyboard.row(inlineButton("🕰 1 روز پیش", 'lastonline_1dago'), inlineButton("🕰 12 ساعت پیش", 'lastonline_12hago')),
    keyboard.row(inlineButton("🕰 2 روز پیش", 'lastonline_2dago')),
    keyboard.row(inlineButton("🕰 7 روز پیش", 'lastonline_7dago'), inlineButton("🕰 3 روز پیش", 'lastonline_3dago')),
    keyboard.row(inlineButton("< بازگشت", 'back_home'))
  elif data == "send_time":
    keyboard.row(inlineButton("⏱ 3 ثانیه", 'sendtime_3s'))
    keyboard.row(inlineButton("⏱ 10 ثانیه", 'sendtime_10s'), inlineButton("⏱ 5 ثانیه", 'sendtime_5s')),
    keyboard.row(inlineButton("< بازگشت", 'back_home'))
  elif data == "anti_login":
    if database['anti_login'] != "روشن✅":
      keyboard.row(inlineButton("✅ روشن کردن", 'anti_login_on')),
      keyboard.row(inlineButton("< بازگشت", 'back_home'))
    else:
      keyboard.row(inlineButton("❎ خاموش کردن", 'anti_login_off')),
      keyboard.row(inlineButton("< بازگشت", 'back_home'))
  elif data == "back_home":
    keyboard.row(inlineButton("< بازگشت", 'back_home'))
  return keyboard
  
def checkNumbers(num):
  numbers = num.splitlines()
  for number in numbers:
    list_numbers = list(number)
    if not number.isdigit():
      result = False
      break
    elif not number.startswith('09'):
      result = False
      break
    elif not len(list_numbers) == 11:
      result = False
      break
    elif number.isdigit():
      result = True
  return result
  
def lichNumbers(prefix):
  return "\n".join([prefix + str(random.randint(1000000, 9999999)) for i in range(100)])
  
@bot.message_handler(commands=['start'])
async def startMessage(message):
  chat_id = message.chat.id
  message_id = message.message_id
  global database
  try:
    database['command'] and database['session'] and database['last_online_time'] and database['send_time'] and database['group_name'] and database['message_text'] and database['anti_login']
  except: database = {'command': None, 'session': None, 'last_online_time': 604800, 'send_time': 5, 'group_name': None, 'message_text': None, 'anti_login': "خاموش❎"}
  if message.from_user.id in admin:
    await sendMessage(chat_id, f'سلام <b>{message.from_user.first_name} 😶‍🌫</b>\n\n🪼 به <b>‹‹ روبیکا سندر ››</b> خوش امدید\n\n🦑 گزینه مورد نظر را انتخاب نمایید', 'HTML', message_id, inlineKeyboard('start'))
    database['command'] = None
  else: await sendMessage(chat_id, '❎ شما ادمین ربات نمیباشید ❎\n\n🪼 Developer : @Uranus_iD', 'HTML', message_id)
  
@bot.callback_query_handler(func=lambda call: True)
async def callbackData(call: object) -> None:
  data = call.data
  chat_id = call.message.chat.id
  message_id = call.message.message_id
  global database
  message_text = database['message_text']
  last_online_time = database['last_online_time']
  if last_online_time == 21600:
    last_online_type = "6 ساعت پیش"
  elif last_online_time == 43200:
    last_online_type = "12 ساعت پیش"
  elif last_online_time == 86400:
    last_online_type = "1 روز پیش"
  elif last_online_time == 172800:
    last_online_type = "2 روز پیش"
  elif last_online_time == 259200:
    last_online_type = "3 روز پیش"
  elif last_online_time == 604800:
    last_online_type = "7 روز پیش"
  group_name = database['group_name']
  
  
  if data == "import":
    await editMessage(chat_id, f'🦑 شماره مورد نظر را ارسال نمایید\n\n<b>✅ مثال =></b> ( +98 )', 'HTML', message_id, inlineKeyboard('back_home'))
    database['command'] = "getPhone"
    
    
    
  elif data == "send_message":
    await editMessage(chat_id, '🦑 نوع ارسال پیام مورد نظر را انتخاب نمایید', 'HTML', message_id, inlineKeyboard('send_message'))
    
    
    
  elif data == "send_chats":
    try:
      chats = await rubika['client'].get_chats()
      if chats.chats:
        await answerCallbackQuery(call.id, f'🦑 اندکی صبر کنید، در حال ارسال پیام به چت و گروه ها ...', True)
        total = len(chats.chats)
        successful = 0
        unsuccessful = 0
        error = 0
        for index, chat in enumerate(chats.chats, start=1):
          if methods.groups.SendMessages in chat.access:
            try:
              sending_message = await rubika['client'].send_message(chat.object_guid, str(message_text))
              successful += 1
            except Exception:
              error += 1
            if successful >= 50:
              time.sleep(database['send_time'])
        unsuccessful = total-successful
        if successful != 0:
          await editMessage(chat_id, f'🦑 اتصال به سرور روبیکا با موفقیت انجام شد\n\n<b>🗯 تعداد چت و گروه ها :</b> {total}\n<b>✅ ارسال موفق :</b> {successful}\n<b>❎ ارسال ناموفق :</b> {unsuccessful}\n\n<b>💬 متن پیام :</b> {message_text}', 'HTML', message_id, inlineKeyboard('back_home'))
        else: await editMessage(chat_id, f'🦑 اکانت شما محدود شد!', 'HTML', message_id, inlineKeyboard('back_home'))
      else: await answerCallbackQuery(call.id, f'🦑 چت یا گروهی وجود ندارد!', True)
    except: await answerCallbackQuery(call.id, f'🦑 اتصال برقرار نشد!', True)
    
    
  if data == "send_contacts":
    try:
      contacts = await rubika['client'].get_contacts()
      if contacts.users:
        await answerCallbackQuery(call.id, f'🦑 اندکی صبر کنید، در حال ارسال پیام به مخاطبین ...', True)
        total = len(contacts.users)
        successful = 0
        unsuccessful = 0
        error = 0
        for index, contact in enumerate(contacts.users, start=1):
          try:
            if round(int(time.time()) - int(contact.last_online)) <= last_online_time:
              sending_message = await rubika['client'].send_message(str(contact.user_guid), str(message_text))
              successful += 1
          except Exception:
            error += 1
          if successful >= 75:
            time.sleep(database['send_time'])
        unsuccessful = total-successful
        if successful != 0:
          await editMessage(chat_id, f'🦑 اتصال به سرور روبیکا با موفقیت انجام شد\n\n<b>☎️ تعداد مخاطبین :</b> {total}\n<b>✅ ارسال موفق :</b> {successful}\n<b>❎ ارسال ناموفق :</b> {unsuccessful}\n<b>👀 اخرین بازدید کاربران :</b> {last_online_type}\n\n<b>💬 متن پیام :</b> {message_text}', 'HTML', message_id, inlineKeyboard('back_home'))
        else: await editMessage(chat_id, f'🦑 اکانت شما محدود شد!', 'HTML', message_id, inlineKeyboard('back_home'))
      else: await answerCallbackQuery(call.id, f'🦑 مخاطبی وجود ندارد!', True)
    except: await answerCallbackQuery(call.id, f'🦑 اتصال برقرار نشد!', True)
    
    
    
    
  elif data == "add_contacts":
    await editMessage(chat_id, '🦑 شماره و رنج های خود را ارسال نمایید\n\n<b>✅ مثال =></b>\n\n➖➖➖➖➖\n<code>09112069926\n09113174400\n09157204547</code>\n➖➖➖➖➖', 'HTML', message_id, inlineKeyboard('back_home'))
    database['command'] = "addContacts"
    
    
  elif data == "delete_contacts":
    try:
      contacts = await rubika['client'].get_contacts()
      if contacts.users:
        await answerCallbackQuery(call.id, f'🦑 اندکی صبر کنید، در حال حذف مخاطبین ...', True)
        total = len(contacts.users)
        successful = 0
        unsuccessful = 0
        for index, contact in enumerate(contacts.users, start=1):
          await rubika['client'].delete_contact(str(contact.user_guid))
          successful += 1
        unsuccessful = total-successful
        await editMessage(chat_id, f'🦑 اتصال به سرور روبیکا با موفقیت انجام شد\n\n<b>✅ حذف موفق :</b> {successful}\n<b>❎ حذف ناموفق :</b> {unsuccessful}', 'HTML', message_id, inlineKeyboard('back_home'))
      else: await answerCallbackQuery(call.id, f'🦑 مخاطبی وجود ندارد!', True)
    except: await answerCallbackQuery(call.id, f'🦑 اتصال برقرار نشد!', True)
    
    
  elif data == "numbers_checker":
    await editMessage(chat_id, '🦑 شماره و رنج های خود را ارسال نمایید\n\n<b>✅ مثال =></b>\n\n➖➖➖➖➖\n<code>09112069926\n09113174400\n09157204547</code>\n➖➖➖➖➖', 'HTML', message_id, inlineKeyboard('back_home'))
    database['command'] = "numbersChecker"
   
   
    
    
  elif data == "options":
    await editMessage(chat_id, '🦑 اپشن مورد نظر را انتخاب نمایید', 'HTML', message_id, inlineKeyboard('options'))
  elif data == "last_online_type":
    await editMessage(chat_id, '🦑 اخرین بازدید کاربرانی که میخواهید به انها پیام ارسال شود را انتخاب نمایید', 'HTML', message_id, inlineKeyboard('last_online_type'))
    
    
  elif data == "lastonline_6hago":
    if database['last_online_time'] != 21600:
      database['last_online_time'] = 21600
      await answerCallbackQuery(call.id, f'🦑 اخرین بازدید کاربرانی که میخواهید به انها پیام ارسال شود به [ 6 ساعت پیش ] تغییر کرد', True)
    else: await answerCallbackQuery(call.id, f'🦑 اخرین بازدید کابران از قبل [ 6 ساعت پیش ] بوده است!', True)
    
  elif data == "lastonline_12hago":
    if database['last_online_time'] != 43200:
      database['last_online_time'] = 43200
      await answerCallbackQuery(call.id, f'🦑 اخرین بازدید کاربرانی که میخواهید به انها پیام ارسال شود به [ 12 ساعت پیش ] تغییر کرد', True)
    else: await answerCallbackQuery(call.id, f'🦑 اخرین بازدید کابران از قبل [ 12 ساعت پیش ] بوده است!', True)
    
  elif data == "lastonline_1dago":
    if database['last_online_time'] != 86400:
      database['last_online_time'] = 86400
      await answerCallbackQuery(call.id, f'🦑 اخرین بازدید کاربرانی که میخواهید به انها پیام ارسال شود به [ 1 روز پیش ] تغییر کرد', True)
    else: await answerCallbackQuery(call.id, f'🦑 اخرین بازدید کابران از قبل [ 1 روز پیش ] بوده است!', True)
    
  elif data == "lastonline_2dago":
    if database['last_online_time'] != 172800:
      database['last_online_time'] = 172800
      await answerCallbackQuery(call.id, f'🦑 اخرین بازدید کاربرانی که میخواهید به انها پیام ارسال شود به [ 2 روز پیش ] تغییر کرد', True)
    else: await answerCallbackQuery(call.id, f'🦑 اخرین بازدید کابران از قبل [ 2 روز پیش ] بوده است!', True)
    
  elif data == "lastonline_3dago":
    if database['last_online_time'] != 259200:
      database['last_online_time'] = 259200
      await answerCallbackQuery(call.id, f'🦑 اخرین بازدید کاربرانی که میخواهید به انها پیام ارسال شود به [ 3 روز پیش ] تغییر کرد', True)
    else: await answerCallbackQuery(call.id, f'🦑 اخرین بازدید کابران از قبل [ 3 روز پیش ] بوده است!', True)
    
  elif data == "lastonline_7dago":
    if database['last_online_time'] != 604800:
      database['last_online_time'] = 604800
      await answerCallbackQuery(call.id, f'🦑 اخرین بازدید کاربرانی که میخواهید به انها پیام ارسال شود به [ 7 روز پیش ] تغییر کرد', True)
    else: await answerCallbackQuery(call.id, f'🦑 اخرین بازدید کابران از قبل [ 7 روز پیش ] بوده است!', True)
    
    
  elif data == "send_time":
    await editMessage(chat_id, '🦑 زمان ارسال پیام به هر کاربر را انتخاب نمایید', 'HTML', message_id, inlineKeyboard('send_time'))
    
    
  elif data == "sendtime_3s":
    if database['send_time'] != 3:
      database['send_time'] = 3
      await answerCallbackQuery(call.id, f'🦑 زمان ارسال پیام به هر کاربر به [ 3 ثانیه ] تغییر کرد', True)
    else: await answerCallbackQuery(call.id, f'🦑 زمان ارسال پیام به هر کاربر از قبل [ 3 ثانیه ] بوده است!', True)
    
  elif data == "sendtime_5s":
    if database['send_time'] != 5:
      database['send_time'] = 5
      await answerCallbackQuery(call.id, f'🦑 زمان ارسال پیام به هر کاربر به [ 5 ثانیه ] تغییر کرد', True)
    else: await answerCallbackQuery(call.id, f'🦑 زمان ارسال پیام به هر کاربر از قبل [ 5 ثانیه ] بوده است!', True)
    
  elif data == "sendtime_10s":
    if database['send_time'] != 10:
      database['send_time'] = 10
      await answerCallbackQuery(call.id, f'🦑 زمان ارسال پیام به هر کاربر به [ 10 ثانیه ] تغییر کرد', True)
    else: await answerCallbackQuery(call.id, f'🦑 زمان ارسال پیام به هر کاربر از قبل [ 10 ثانیه ] بوده است!', True)
    
    
  elif data == "group_name":
    if group_name != None:
      await editMessage(chat_id, f'<b>🖇 نام گروه فعلی :</b> {group_name}\n\n🦑 نام گروه جدید خود را ارسال نمایید', 'HTML', message_id, inlineKeyboard('back_home'))
    else:
      await editMessage(chat_id, f'<b>🖇 نام گروه فعلی :</b> تنظیم نشده!\n\n🦑 نام گروه خود را ارسال نمایید', 'HTML', message_id, inlineKeyboard('back_home'))
    database['command'] = "setGroupName"
    
    
    
    
  elif data == "message_text":
    if message_text != None:
      await editMessage(chat_id, f'<b>💬 متن پیام فعلی :</b> {message_text}\n\n🦑 متن پیام جدید خود را ارسال نمایید', 'HTML', message_id, inlineKeyboard('back_home'))
    else:
      await editMessage(chat_id, f'<b>💬 متن پیام فعلی :</b> تنظیم نشده!\n\n🦑 متن پیام خود را ارسال نمایید', 'HTML', message_id, inlineKeyboard('back_home'))
    database['command'] = "setMessageText"
    
    
    
    
  elif data == "lich_numbers":
    await editMessage(chat_id, '🦑 پیش شماره خود را ارسال نمایید\n\n<b>✅ مثال =></b> ( 0911 )', 'HTML', message_id, inlineKeyboard('back_home'))
    database['command'] = "lichNumbers"
    
    
    
    
    
  elif data == "anti_login":
    await editMessage(chat_id, f'<b>🛡 وضعیت انتی لاگین</b> : {database["anti_login"]}\n\n🦑 وضعیت انتی لاگین را انتخاب نمایید', 'HTML', message_id, inlineKeyboard('anti_login'))
    
    
    
  elif data == "anti_login_on":
    if database['anti_login'] != "روشن✅":
      database['anti_login'] = "روشن✅"
      await editMessage(chat_id, '🦑 وضعیت انتی لاگین با موفقیت به <b>[ روشن✅ ]</b> تغییر کرد', 'HTML', message_id, inlineKeyboard('back_home'))
      while True:
        if database['anti_login'] == "روشن✅":
          print('AntiLogin ON')
          try:
            sessions = await rubika['client'].get_my_sessions()
            for index, session in enumerate(sessions.other_sessions, start=1):
              if session.terminatable == True:
                await ['client'].terminate_session(str(session.key))
          except Exception as e:
            print('Not Checking')
        else: break
    else:
      editMessage(chat_id, 'Activation problem', 'HTML', message_id, inlineKeyboard('back_home'))
      
      
  elif data == "anti_login_off":
    database['anti_login'] = "خاموش❎"
    await editMessage(chat_id, '🦑 وضعیت انتی لاگین با موفقیت به <b>[ خاموش❎ ]</b> تغییر کرد', 'HTML', message_id, inlineKeyboard('back_home'))
    
  elif data == "logout":
    database['session'] = None
    os.remove(f'{rubika_session}.rbs')
    await rubika['client'].disconnect()
    await editMessage(chat_id, '🦑 سشن پاک شد کصکش', 'HTML', message_id, inlineKeyboard('start'))
    
    
    
  elif data == "back_home":
    await editMessage(chat_id, f'سلام <b>{call.message.from_user.first_name} 😶‍🌫</b>\n\n🪼 به <b>‹‹ روبیکا سندر ››</b> خوش امدید\n\n🦑 گزینه مورد نظر را انتخاب نمایید', 'HTML', message_id, inlineKeyboard('start'))
    database['command'] = None
    
    
  
    
@bot.message_handler(func=lambda message: True, content_types=['text'])
async def returnMessage(message):
  text = message.text
  chat_id = message.chat.id
  message_id = message.message_id
  global database
  command = database['command']
  message_text = database['message_text']
  last_online_time = database['last_online_time']
  if last_online_time == 21600:
    last_online_type = "6 ساعت پیش"
  elif last_online_time == 43200:
    last_online_type = "12 ساعت پیش"
  elif last_online_time == 86400:
    last_online_type = "1 روز پیش"
  elif last_online_time == 172800:
    last_online_type = "2 روز پیش"
  elif last_online_time == 259200:
    last_online_type = "3 روز پیش"
  elif last_online_time == 604800:
    last_online_type = "7 روز پیش"
  if message.from_user.id in admin:
    
    
    
    
    
    
    if command == "getPhone":
      if text.startswith('+98') and len(text) == 13:
        try:
          rubika['client'] = Client(session=rubika_session)
          await rubika['client'].connect()
          rubika['phone_number'] = text.replace('+98', '')
          rubika['response'] = await rubika['client'](methods.authorisations.SendCode(phone_number=text.replace('+98', '')))
          await sendMessage(chat_id, f'🦑 کد ارسال شده به شماره [ {text} ] را ارسال نمایید\n\n<b>✅ مثال =></b> ( 021210 )', 'HTML', message_id)
          database['command'] = "getCode"
        except Exception as e: await sendMessage(chat_id, f'🦑 اتصال برقرار نشد!', 'HTML', message_id)
      else: await sendMessage(chat_id, f'❎ شماره ارسالی اشتباه میباشد\n\n🦑 شماره صحیح ارسال نمایید ', 'HTML', message_id)
      
      
      
      
      
      
    elif command == "getCode":
      if len(text) == 6 or len(text) == 5:
        await sendMessage(chat_id, f'🦑 اندکی صبر کنید، در حال اتصال به روبیکا ...', 'HTML', message_id)
        try:
          public_key, rubika['client']._private_key = Crypto.create_keys()
          sign_in = await rubika['client'](methods.authorisations.SignIn(phone_code=text, phone_number=rubika['phone_number'], phone_code_hash=rubika['response'].phone_code_hash, public_key=public_key))
          if sign_in.status == "OK":
            database['session'] = True
            chats = await rubika['client'].get_chats()
            total_chats = len(chats.chats)
            contacts = await rubika['client'].get_contacts()
            total_contacts = len(contacts.users)
            await editMessage(chat_id, f'Hi <b>{message.from_user.first_name} 😶‍🌫</b>\n\n🪼 با موفقیت به سرور روبیکا متصل شدید\n\n<b>🗯 چت و گروه ها :</b> {int(total_chats)}\n<b>☎️ مخاطبین :</b> {int(total_contacts)}', 'HTML', message_id+1, inlineKeyboard('start'))
            database['command'] = None
          else: await editMessage(chat_id, f'❎ کد ارسالی اشتباه میباشد\n\n🦑 کد صحیح ارسال نمایید', 'HTML', message_id+1)
        except Exception as e: await editMessage(chat_id, f'🦑 اتصال برقرار نشد!', 'HTML', message_id+1)
      else: await sendMessage(chat_id, f'❎ کد ارسالی اشتباه میباشد\n\n🦑 کد صحیح ارسال نمایید', 'HTML', message_id)
    
    
    
    
    
    
    
    
    
    
    if command == "addContacts":
      if checkNumbers(text):
        numbers = text.splitlines()
        numbers = list(map(lambda x: x[1:], numbers))
        await sendMessage(chat_id, '🦑 اندکی صبر کنید، در حال افزودن مخاطبین ...', 'HTML', message_id)
        with open('contacts_successful.txt', 'a') as f:
          total = 0
          successful = 0
          unsuccessful = 0
          for contact in numbers:
            add_contacts = await rubika['client'].add_address_book(str(contact), str('My'), str('Contacts'))
            check = json.loads(str(add_contacts))
            if check['user_exist'] == True:
              last_online = str(check['user']['last_online'])
              total += 1
              if round(int(time.time()) - int(last_online)) <= last_online_time:
                f.write(f"0{str(contact)}\n")
                successful += 1
              else:
                unsuccessful += 1
          f.close()
          with open('contacts_successful.txt', 'rb') as f_id:
            await sendDocument(chat_id, f_id)
            f = open("contacts_successful.txt", "r").readlines()
            await editMessage(chat_id, f'🦑 اتصال به سرور روبیکا با موفقیت انجام شد\n\n<b>☎️ مخاطبین ادد شده :</b> {total}\n<b>✅ مخاطبین انلاین :</b> {successful}\n<b>❎ مخاطبین افلاین :</b> {unsuccessful}\n<b>👀 اخرین بازدید کاربران :</b> {last_online_type}', 'HTML', message_id+1, inlineKeyboard('back_home'))
            os.remove('contacts_successful.txt')
            database['command'] = None
      else: await sendMessage(chat_id, f'❎ شماره و رنج های ارسالی اشتباه میباشد\n\n🦑 شماره و رنج های صحیح ارسال نمایید', 'HTML', message_id)
      
      
      
      
      
      
      
    if command == "numbersChecker":
      try:
        if checkNumbers(text):
          numbers = text.splitlines()
          numbers = list(map(lambda x: x[1:], numbers))
          await sendMessage(chat_id, '🦑 اندکی صبر کنید، در حال چک کردن شماره ها ...', 'HTML', message_id)
          with open('numbers_successful.txt', 'a') as f:
            total = 0
            successful = 0
            unsuccessful = 0
            for contact in numbers:
              add_contacts = await rubika['client'].add_address_book(str(contact), str('My'), str('Contacts'))
              check = json.loads(str(add_contacts))
              if check['user_exist'] == True:
                last_online = str(check['user']['last_online'])
                total += 1
                if round(int(time.time()) - int(last_online)) <= last_online_time:
                  f.write(f"0{str(contact)}\n")
                  successful += 1
                else:
                  unsuccessful += 1
            f.close()
            with open('numbers_successful.txt', 'rb') as f_id:
              await sendDocument(chat_id, f_id)
              f = open("numbers_successful.txt", "r").readlines()
              await editMessage(chat_id, f'🦑 اتصال به سرور روبیکا با موفقیت انجام شد\n\n<b>♻️ شماره های چک شده :</b> {total}\n<b>✅ شماره های انلاین :</b> {successful}\n<b>❎ شماره های افلاین :</b> {unsuccessful}\n<b>👀 اخرین بازدید کاربران :</b> {last_online_type}', 'HTML', message_id+1, inlineKeyboard('back_home'))
              os.remove('numbers_successful.txt')
              database['command'] = None
        else: await sendMessage(chat_id, f'❎ شماره و رنج های ارسالی اشتباه میباشد\n\n🦑 شماره و رنج های صحیح ارسال نمایید', 'HTML', message_id)
      except: await sendMessage(chat_id, f'Error Connection', 'HTML', message_id)
      
      
      
      
      
      
    elif command == "lichNumbers":
      if text.startswith('09') and len(text) == 4:
        await sendMessage(chat_id, f'🦑 شماره ها با موفقیت استخراج شدند\n\n➖➖➖➖➖\n<code>{lichNumbers(text)}</code>\n➖➖➖➖➖', 'HTML', message_id, inlineKeyboard('back_home'))
        database['command'] = None
      else:
        await sendMessage(chat_id, f'❎ پیش شماره ارسالی اشتباه میباشد\n\n🦑 پیش شماره صحیح ارسال نمایید', 'HTML', message_id, inlineKeyboard('back_home'))
        
        
        
    elif command == "setMessageText":
      database['message_text'] = text
      await sendMessage(chat_id, f'🦑 متن پیام با موفقیت تغییر کرد\n\n<b>💬 متن پیام جدید :</b> {text}', 'HTML', message_id, inlineKeyboard('back_home'))
      database['command'] = None
      
    elif command == "setGroupName":
      database['group_name'] = text
      await sendMessage(chat_id, f'🦑 نام گروه با موفقیت تغییر کرد\n\n<b>🖇 نام گروه جدید :</b> {text}', 'HTML', message_id, inlineKeyboard('back_home'))
      database['command'] = None
  



asyncio.run(bot.infinity_polling())
