import sqlite3


class Database:
    def __init__(self, db_file):
        self.connection = sqlite3.connect(db_file)
        self.cursor = self.connection.cursor()

    def create_user_account(self, data_user_info: dict):
        """
        Добавляет пользователя в базу данных(не для проверки администратором)
        :param data_user_info: Словарик с данными пользователя
        :return: None
        """
        # Доп инфу сохраняем в отдельную таблицу связанную с пользователями по user_id
        with self.connection:
            self.cursor.execute("INSERT INTO `setting_admin_panel` (`key`) VALUES ((?))", (values,))

    def get_message_text(self, msg_id):
        with self.connection:
            result = self.cursor.execute("SELECT `text` FROM `messages` WHERE `id` = (?)",
                                (msg_id,)).fetchone()
        return result[0]

    def delete_message_default(self, message_id):
        with self.connection:
            self.cursor.execute("DELETE FROM `messages` WHERE `id` = (?)", (message_id,))

    def add_global_values(self, values):
        with self.connection:
            self.cursor.execute("INSERT INTO `setting_admin_panel` (`key`) VALUES ((?))", (values,))

    def get_global_values(self):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `setting_admin_panel`").fetchall()

    def get_history_user(self, user_id):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `history` WHERE `user_id` = (?)", (user_id, )).fetchall()

    def get_history_status(self):
        with self.connection:
            text = "history_status"
            status = self.cursor.execute("SELECT `value` FROM `setting_admin_panel` WHERE `key` = (?)", (text,)).fetchone()
        return status[0]