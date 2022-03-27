from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

btnMain = KeyboardButton('⬅ Главное меню')

# ------ Main Menu ------
btnProfile = KeyboardButton('👥 Профиль')
btnSub = KeyboardButton('❤ Подписка')
btnHelp = KeyboardButton('ℹ Помощь')
mainMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnProfile, btnSub, btnHelp)

# ------ Profile Menu ------
btnEdit = KeyboardButton('🖊️ Изменить данные')
btnData = KeyboardButton('🗄️ Мои данные')
profileMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnEdit, btnData, btnMain)
