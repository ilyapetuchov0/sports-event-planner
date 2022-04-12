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
btnEvent = KeyboardButton('👥 События')
profileMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnEdit, btnData, btnMain, btnEvent)

# ------ Event Menu ------
btnAddEvent = KeyboardButton('Создать мероприятие')
btnDeleteEvent = KeyboardButton('Удалить мероприятие')
btnEditEvent = KeyboardButton('Изменить мероприятие')
btnAllEvent = KeyboardButton('Просмотреть мои мероприятия')

eventMenu = ReplyKeyboardMarkup(resize_keyboard=True).add(btnAddEvent, btnDeleteEvent, btnEditEvent, btnAllEvent)
