#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sqlite3


class Events:  # При создании обьекта класса принимается один агрумент - путь к базе данных

    """
        Каждый метод в случае ошибки возвращает кортеж из значения "False" и ошибку которая произошла(error),
        в случае успешного выполнения возвращает "None"
    """

    def __init__(self, path_to_db):  # Подключение
        self.DB_FILE_NAME = path_to_db
        self.connection = sqlite3.connect(path_to_db)
        self.cursor = self.connection.cursor()

    def add_event(self, id, name, date, organizer, count_of_registered, status):  # Добавить мероприятие
        try:
            with self.connection:
                query = "INSERT INTO main (id, name, date, organizer, count_of_registered, status)" \
                        "VALUES(?, ?, ?, ?, ?, ?)"
                self.cursor.execute(query, (id, name, date, organizer, count_of_registered, status))
        except sqlite3.Error as error:
            return False, error

    def delete_event(self, id):  # Удалить мероприятие
        try:
            with self.connection:
                query = f"DELETE from main where id = {id}"
                self.cursor.execute(query)
        except sqlite3.Error as error:
            return False, error

    def edit_event(self, id, name, date, organizer, count_of_registered, status):  # редактировать мероприятие
        try:
            with self.connection:
                query = f"UPDATE main SET name = (?), date = (?), organizer = (?)," \
                        f" count_of_registered = (?), status = (?) where id = (?)"
                self.cursor.execute(query, (name, date, organizer, count_of_registered, status, id))
        except sqlite3.Error as error:
            return False, error

    def get_all_db(self):
        try:
            with self.connection:
                result = self.cursor.execute('''SELECT * FROM main''').fetchall()
                return result
        except sqlite3.Error as error:
            return False, error

    def get_status(self, id):
        try:
            with self.connection:
                result = self.cursor.execute("SELECT `status` FROM `main` WHERE `id` = ?", (id,)).fetchall()
                for row in result:
                    status = str(row[0])
                return status
        except sqlite3.Error as error:
            return False, error

    def set_status(self, id, status):
        try:
            with self.connection:
                return self.cursor.execute("UPDATE `main` SET `status` = ? WHERE `id` = ?", (status, id,))
        except sqlite3.Error as error:
            return False, error

    def get_info(self, column, argument):
        """Принимает на вход назавние столбца, и искомый
         аргумент(Название, дата, id и т.д) по которому возвращает информацию
         column и argument должны быть типа 'str' """
        try:
            with self.connection:
                if column == 'id':
                    result = self.cursor.execute('''SELECT * FROM main WHERE id = (?)''', argument).fetchall()
                if column == 'name':
                    result = self.cursor.execute('''SELECT * FROM main WHERE name = (?)''', [argument]).fetchall()
                if column == 'date':
                    result = self.cursor.execute('''SELECT * FROM main WHERE date = ?''', [argument]).fetchall()
                if column == 'organizer':
                    result = self.cursor.execute('''SELECT * FROM main WHERE organizer = (?)''', [argument]).fetchall()
                if column == 'count_of_registered':
                    result = self.cursor.execute('''SELECT * FROM main WHERE count_of_registered = (?)''',
                                                 [argument]).fetchall()
                if column == 'status':
                    result = self.cursor.execute('''SELECT * FROM main WHERE status = (?)''', [argument]).fetchall()
                return result
        except sqlite3.Error as error:
            return False, error


def generate_db(name_db):  # Используется один раз для создания базы, на вход принимает название создаваемой базы данных
    try:
        with sqlite3.connect(name_db) as db:
            cursor = db.cursor()
            query = "CREATE TABLE IF NOT EXISTS main(id INTEGER, name TEXT, date TEXT, organizer TEXT, " \
                    "count_of_registered INTEGER, status TEXT)"
            # query = "INSERT INTO expenses (id, name, date, quality) VALUES(?, ?, ?, ?)"
            cursor.execute(query)
    except sqlite3.Error as error:
        return False, error
