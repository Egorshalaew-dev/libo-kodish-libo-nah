from aiogram.types import ReplyKeyboardRemove,ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton







b1 = KeyboardButton('Рассылка')
b2 = KeyboardButton('Добавить в ЧС')
b3 = KeyboardButton('Убрать из ЧС')

button = KeyboardButton('Меню')

button1 = KeyboardButton('Помощь')
button2 = KeyboardButton('Контакты')
button3 = KeyboardButton('Ознакомление')
button4 = KeyboardButton('Обучение')

markup = ReplyKeyboardMarkup().add(
    b1,b2,b3
)

markup1 = ReplyKeyboardMarkup().row(
    button1, button2, button3
).add(button4)

button5 = KeyboardButton('Сотрудники')
button6 = KeyboardButton('Рабочее место')



markup2 = ReplyKeyboardMarkup().row(
    button5, button6
).add(button)



button7 = KeyboardButton('Видеообучение')
button8 = KeyboardButton('Пройти тест')

markup3 = ReplyKeyboardMarkup().add(button7,button8)
