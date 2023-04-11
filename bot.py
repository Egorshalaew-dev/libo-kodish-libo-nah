from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor


from config import TOKEN
import keyboard as kb

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
import logging
import sqlite3

API_TOKEN = TOKEN
ADMIN = 848471421

logging.basicConfig(level=logging.INFO)
storage = MemoryStorage()
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

conn = sqlite3.connect('db.db')
cur = conn.cursor()
cur.execute("""CREATE TABLE IF NOT EXISTS users(user_id INTEGER, block INTEGER);""")
conn.commit()

class dialog(StatesGroup):
  spam = State()
  blacklist = State()
  whitelist = State()



async def check(message: types.Message, text, button):
  cur = conn.cursor()
  cur.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
  result = cur.fetchone()
  if message.from_user.id == ADMIN:
    await message.answer('Welcome back, adm!', reply_markup=kb.markup)
  else:
      print(result)
      if result is None or result[0] is 0:
        cur = conn.cursor()
        cur.execute(f'''SELECT * FROM users WHERE (user_id="{message.from_user.id}")''')
        entry = cur.fetchone()
        print(entry)
        if entry is None or entry[1] is 0:
          #cur.execute(f'''INSERT INTO users VALUES ('{message.from_user.id}', '0')''')
          conn.commit()
          await message.reply(text, reply_markup=button)
      else:
        await message.answer('Ты был заблокирован!')

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
  #await check(message, "Привет!\nЯ чат бот для обучения сотрудников во вкусно и точка. Задавай вопросы",kb.markup1)
  cur = conn.cursor()
  cur.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
  result = cur.fetchone()
  if message.from_user.id == ADMIN:
    await message.answer('Welcome back, adm!', reply_markup=kb.markup)
  else:
      print(result)
      if result is None or result[0] is 0:
        cur = conn.cursor()
        cur.execute(f'''SELECT * FROM users WHERE (user_id="{message.from_user.id}")''')
        entry = cur.fetchone()
        print(entry)
        if entry is None or entry[1] is 0:
          cur.execute(f'''INSERT INTO users VALUES ('{message.from_user.id}', '0')''')
          conn.commit()
          await message.reply(text='Привет!\nЯ чат бот для обучения сотрудников во вкусно и точка. Задавай вопросы', reply_markup=kb.markup1)
      else:
        await message.answer('Ты был заблокирован!')


@dp.message_handler(content_types=['text'], text='Помощь')
async def process_help_command(message: types.Message):
  await check(message, "Данный бот предназначен для онбординга сотрудников\nВ случае возникновения проблем пишите по контактам", None)

@dp.message_handler(content_types=['text'], text='Контакты')
async def process_help_command(message: types.Message):

  await check(message, "В случае проблем, обращаться к \n@i3gorsh \n@motyaabormotya", None)
    ########

@dp.message_handler(content_types=['text'], text='Ознакомление')
async def process_help_command(message: types.Message):
  await check(message, "С кем будем тебя знакомить?", kb.markup2)

@dp.message_handler(content_types=['text'], text='Сотрудники')
async def process_help_command(message: types.Message):
  await check(message, "Главный по булочкам: Пчеленок Матвей \nГлавный по котлетам: Шалаев Егор", None)

@dp.message_handler(content_types=['text'], text='Рабочее место')
async def process_help_command(message: types.Message):

  cur = conn.cursor()
  cur.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
  result = cur.fetchone()
  if message.from_user.id == ADMIN:
    await message.answer('Welcome back, adm!', reply_markup=kb.markup)
  else:
      print(result)
      if result is None or result[0] is 0:
        cur = conn.cursor()
        cur.execute(f'''SELECT * FROM users WHERE (user_id="{message.from_user.id}")''')
        entry = cur.fetchone()
        print(entry)
        if entry is None or entry[1] is 0:
          #cur.execute(f'''INSERT INTO users VALUES ('{message.from_user.id}', '0')''')
          conn.commit()
          with open(r'C:\Users\_ADMIN_\OneDrive\Рабочий стол\libo kodish libo nah\Picture.jpg', 'rb') as photo:
            await bot.send_photo(message.chat.id, photo)
      else:
        await message.answer('Ты был заблокирован!')


@dp.message_handler(content_types=['text'], text='Меню')
async def process_help_command(message: types.Message):
  await check(message, "Меню",kb.markup1)

@dp.message_handler(content_types=['text'], text='Обучение')
async def process_help_command(message: types.Message):
  await check(message, "Выберите вариант обучения",kb.markup3)

@dp.message_handler(content_types=['text'], text='Видеообучение')
async def process_help_command(message: types.Message):
  await check(message, "Видео",kb.markup3)

@dp.message_handler(content_types=['text'], text='Пройти тест')
async def process_help_command(message: types.Message):
  await check(message, "Тест - ",kb.markup3)




























#################################################################################################################################################### АДМИН ПАНЕЛЬ

@dp.message_handler(content_types=['text'], text='Рассылка')
async def spam(message: Message):
  await dialog.spam.set()
  await message.answer('Напиши текст рассылки')

@dp.message_handler(state=dialog.spam)
async def start_spam(message: Message, state: FSMContext):
  if message.text == 'Назад':
    await message.answer('Главное меню', reply_markup=kb.markup)
    await state.finish()
  else:
    cur = conn.cursor()
    cur.execute(f'''SELECT user_id FROM users''')
    spam_base = cur.fetchall()
    print(len(spam_base))
    print(spam_base)
    for z in range(len(spam_base)):
        await bot.send_message(spam_base[z][0], message.text)
        await message.answer('Рассылка завершена', reply_markup=kb.markup)
        await state.finish()

@dp.message_handler(content_types=['text'], text='Добавить в ЧС')
async def hanadler(message: types.Message, state: FSMContext):
  if message.chat.id == ADMIN:
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(types.InlineKeyboardButton(text="Назад"))
    await message.answer('Введите id пользователя, которого нужно заблокировать.\nДля отмены нажмите кнопку ниже', reply_markup=keyboard)
    await dialog.blacklist.set()

@dp.message_handler(state=dialog.blacklist)
async def proce(message: types.Message, state: FSMContext):
  if message.text == 'Назад':
    await message.answer('Отмена! Возвращаю назад.', reply_markup=kb.markup)
    await state.finish()
  else:
    if message.text.isdigit():
      cur = conn.cursor()
      cur.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
      result = cur.fetchall()
      if len(result) == 0:
        await message.answer('Такой пользователь не найден в базе данных.', reply_markup=kb.markup)
        await state.finish()
      else:
        a = result[0]
        id = a[0]
        if id == 0:
          cur.execute(f"UPDATE users SET block = 1 WHERE user_id = {message.text}")
          conn.commit()
          await message.answer('Пользователь успешно добавлен в ЧС.', reply_markup=kb.markup)
          await state.finish()
          await bot.send_message(message.text, 'Ты был забанен Администрацией')
        else:
          await message.answer('Данный пользователь уже получил бан', reply_markup=kb.markup)
          await state.finish()
    else:
      await message.answer('Это не похоже на ID.\n\nВведи ID')

@dp.message_handler(content_types=['text'], text='Убрать из ЧС')
async def hfandler(message: types.Message, state: FSMContext):
  cur = conn.cursor()
  cur.execute(f"SELECT block FROM users WHERE user_id = {message.chat.id}")
  result = cur.fetchone()
  if result is None:
    if message.chat.id == ADMIN:
      keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
      keyboard.add(types.InlineKeyboardButton(text="Назад"))
      await message.answer('Введите id пользователя, которого нужно разблокировать.\nДля отмены нажмите кнопку ниже', reply_markup=keyboard)
      await dialog.whitelist.set()

@dp.message_handler(state=dialog.whitelist)
async def proc(message: types.Message, state: FSMContext):
  if message.text == 'Отмена':
    await message.answer('Отмена! Возвращаю назад.', reply_markup=kb.markup)
    await state.finish()
  else:
    if message.text.isdigit():
      cur = conn.cursor()
      cur.execute(f"SELECT block FROM users WHERE user_id = {message.text}")
      result = cur.fetchall()
      conn.commit()
      if len(result) == 0:
        await message.answer('Такой пользователь не найден в базе данных.', reply_markup=kb.markup)
        await state.finish()
      else:
        a = result[0]
        id = a[0]
        if id == 1:
          cur = conn.cursor()
          cur.execute(f"UPDATE users SET block = 0 WHERE user_id = {message.text}")
          conn.commit()
          await message.answer('Пользователь успешно разбанен.', reply_markup=kb.markup)
          await state.finish()
          await bot.send_message(message.text, 'Вы были разблокированы администрацией.')
        else:
          await message.answer('Данный пользователь не получал бан.', reply_markup=kb.markup)
          await state.finish()
    else:
      await message.answer('Это не похоже на ID.\n\nВведи ID')

#################################################################################################################################################### АДМИН ПАНЕЛЬ







if __name__ == '__main__':
    executor.start_polling(dp)
