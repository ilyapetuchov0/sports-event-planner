import logging
from aiogram import Bot, Dispatcher, executor, types
import markups as nav
from db import Database

TOKEN = "5001100340:AAG7_nbmWjOEdqpCHYJMyrLLf3B2WDNCNXQ"

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

db = Database('database.db')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    if not db.user_exists(message.from_user.id):
        db.add_user(message.from_user.id)
        await bot.send_message(message.from_user.id, "Укажите Ваше имя пользователя")
    else:
        await bot.send_message(message.from_user.id, "Вы уже зарегистрированы", reply_markup=nav.mainMenu)


@dp.message_handler()
async def bot_message(message: types.Message):
    if message.chat.type == 'private':
        if message.text == '👥 ПРОФИЛЬ':
            user_nickname = "Ваш ник: " + db.get_nickname(message.from_user.id) + "\n"
            user_age = "Ваш возраст: " + db.get_age(message.from_user.id)
            res = user_nickname + user_age
            await bot.send_message(message.from_user.id, res, reply_markup=nav.profileMenu)
        elif message.text == '❤ ПОДПИСКА':
            await bot.send_message(message.from_user.id, "Coming soon... Этот раздел находится в разработке!")
        elif message.text == 'ℹ ПОМОЩЬ':
            await bot.send_message(message.from_user.id, "Скоро здесь появятся команды")
        elif message.text == '⬅ ГЛАВНОЕ МЕНЮ':
            await bot.send_message(message.from_user.id, 'Вы вернулись в главное меню', reply_markup=nav.mainMenu)
        else:
            if db.get_signup(message.from_user.id) == "setnickname":
                if len(message.text) > 15:
                    await bot.send_message((message.from_user.id, "Никнейм не должен превышать 15 символов"))
                elif '@' in message.text or '/' in message.text:
                    await bot.send_message(message.from_user.id, "Вы ввели запрещенный символ")
                else:
                    db.set_nickname(message.from_user.id, message.text)
                    db.set_signup(message.from_user.id, "setage")
                    await bot.send_message(message.from_user.id, "Теперь укажите Ваш возраст")
            elif db.get_signup(message.from_user.id) == "setage":
                try:
                    int(message.text)
                except ValueError:
                    await bot.send_message(message.from_user.id, "Некорректное значчение возраста")
                else:
                    if 10 < int(message.text) < 100:
                        db.set_age(message.from_user.id, message.text)
                        db.set_signup(message.from_user.id, "done")
                        await bot.send_message(message.from_user.id, "Спасибо за регистрицию. Теперь Вы можете "
                                                                     "пользоваться основными функциями бота")
                    else:
                        await bot.send_message(message.from_user.id, "Некорректное значение возраста")

            else:
                await bot.send_message(message.from_user.id, "Я вас пока что не понимаю, но в скором времени "
                                                             "обязательно пойму :)")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
