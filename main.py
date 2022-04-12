import logging
from aiogram import Bot, Dispatcher, executor, types

import Events as events
import markups as nav
from db import Database

TOKEN = "5206592644:AAHbD4XE8JCJygcHW6hz5w0QSIKro9COV4A"
logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)

dp = Dispatcher(bot)

event = events.Events

event_db = events.generate_db("events.db")

db = Database('database.db')
name = ""
date = ""
organizer = ""
count_of_registered = ""


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
        if message.text == '👥 Профиль':
            user_nickname = "Ваш ник: " + db.get_nickname(message.from_user.id) + "\n"
            user_age = "Ваш возраст: " + db.get_age(message.from_user.id)
            res = user_nickname + user_age
            await bot.send_message(message.from_user.id, res, reply_markup=nav.profileMenu)
        elif message.text == '❤ Подписка':
            await bot.send_message(message.from_user.id, "Coming soon... Этот раздел находится в разработке!")
        elif message.text == 'ℹ Помощь':
            await bot.send_message(message.from_user.id, "Скоро здесь появятся команды")
        elif message.text == '⬅ Главное меню':
            await bot.send_message(message.from_user.id, 'Вы вернулись в главное меню', reply_markup=nav.mainMenu)
        elif message.text == '🖊️ Изменить данные':
            await bot.send_message(message.from_user.id, "Укажите Ваше новое имя пользователя")
            db.set_signup(message.from_user.id, "setnewnickname")
        elif message.text == '👥 События':
            await bot.send_message(message.from_user.id, "Что хотите сделать?", reply_markup=nav.eventMenu)
        elif message.text == 'Создать мероприятие':
            await bot.send_message(message.from_user.id, "Укажите название мероприятия")
            event.set_status(message.from_user.id, 'seteventname')
        elif message.text == 'Удалить мероприятие':
            event.delete_event(message.from_user.id)
        elif message.text == 'Изменить мероприятие':
            event.edit_event(message.from_user.id)
        elif message.text == 'Просмотреть мои мероприятия':
            event.get_info(message.from_user.id)
        else:
            global name, date, organizer, count_of_registered
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
            elif db.get_signup(message.from_user.id) == "setnewnickname":
                if len(message.text) > 15:
                    await bot.send_message((message.from_user.id, "Никнейм не должен превышать 15 символов"))
                elif '@' in message.text or '/' in message.text:
                    await bot.send_message(message.from_user.id, "Вы ввели запрещенный символ")
                else:
                    db.set_nickname(message.from_user.id, message.text)
                    db.set_signup(message.from_user.id, "setnewage")
                    await bot.send_message(message.from_user.id, "Теперь укажите Ваш новый возраст")
            elif db.get_signup(message.from_user.id) == "setnewage":
                try:
                    int(message.text)
                except ValueError:
                    await bot.send_message(message.from_user.id, "Некорректное значчение возраста")
                else:
                    if 10 < int(message.text) < 100:
                        db.set_age(message.from_user.id, message.text)
                        db.set_signup(message.from_user.id, "done")
                        await bot.send_message(message.from_user.id, "Успешно")

            # Set new status to name event
            elif event.get_status(message.from_user.id, message.from_user.id) == "seteventname":
                # Checking for forbidden symbols
                if '@' in message.text or '/' in message.text:
                    await bot.send_message(message.from_user.id, "Вы ввели запрещенный символ")
                else:
                    name = message.text
                    event.Events.set_status(message.from_user.id, "seteventdate")
                    await bot.send_message(message.from_user.id, "Укажите дату мероприятия в формате дд.мм.гг")
            elif event.Events.get_status(message.from_user.id) == "seteventdate":
                if '@' in message.text or '/' in message.text:
                    await bot.send_message(message.from_user.id, "Вы ввели запрещенный символ")
                else:
                    date = message.text
                    event.Events.set_status(message.from_user.id, "setorganisationname")
                    await bot.send_message(message.from_user.id, "Укажите организатора мероприятия")
            elif event.Events.get_status(message.from_user.id) == "setorganisationname":
                if '@' in message.text or '/' in message.text:
                    await bot.send_message(message.from_user.id, "Вы ввели запрещенный символ")
                else:
                    organizer = message.text
                    event.Events.set_status(message.from_user.id, "setcountpeopleonevent")
                    await bot.send_message(message.from_user.id, "Укажите количество человек на мероприятии")
            elif event.Events.get_status(message.from_user.id) == "setcountpeopleonevent":
                if '@' in message.text or '/' in message.text:
                    await bot.send_message(message.from_user.id, "Вы ввели запрещенный символ")
                else:
                    count_of_registered = message.text
                    event.Events.set_status(message.from_user.id, "done")
                    await bot.send_message(message.from_user.id, "Укажите количество человек на мероприятии")
            if event.Events.get_status(message.from_user.id) == "done":
                event.Events.add_event(message.from_user.id, name, date, organizer, count_of_registered,
                                       event.Events.get_status(message.from_user.id))
                await bot.send_message(message.from_user.id, "Получилось! Спасибо за регистрацию в нашем сервисе")


            # elif Event_status == 1:
            #     name = message.text
            #     await bot.send_message(message.from_user.id, "")
            #     Event_status = 2
            # elif Event_status == 2:
            #     date = message.text
            #     await bot.send_message(message.from_user.id, "Укажите организатора мероприятия")
            #     Event_status = 3
            # elif Event_status == 3:
            #     organizer = message.text
            #     await bot.send_message(message.from_user.id, "Укажите количество человек на мероприятии")
            #     Event_status = 4
            # elif Event_status == 4:
            #     count_of_registered = message.text
            #     events.Events.add_event(message.from_user.id, name, date, organizer, count_of_registered)

            else:
                await bot.send_message(message.from_user.id, "Я вас пока что не понимаю, но в скором времени "
                                                             "обязательно пойму :)")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
