import sqlite3


class Database:
    def __init__(self, db_file):
        # подключение дб
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    # добавление пользователя
    def add_user(self, user_id):
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    # существует ли пользователь
    def user_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return bool(len(result))

    def set_nickname(self, user_id, nickname):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `nickname` = ? WHERE `user_id` = ?", (nickname, user_id,))

    def set_age(self, user_id, age):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `age` = ? WHERE `user_id` = ?", (age, user_id,))

    def get_signup(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `signup` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                signup = str(row[0])
            return signup

    def set_signup(self, user_id, signup):
        with self.connection:
            return self.cursor.execute("UPDATE `users` SET `signup` = ? WHERE `user_id` = ?", (signup, user_id,))

    def get_nickname(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `nickname` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                nickname = str(row[0])
            return nickname

    def get_age(self, user_id):
        with self.connection:
            result = self.cursor.execute("SELECT `age` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            for row in result:
                age = str(row[0])
            return age
