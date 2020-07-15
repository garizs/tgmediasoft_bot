import sqlite3


class DataBase:
    # Метод инициации подключения к БД
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    # Метод для получения всех подписок на рассылку
    def get_subscriptions(self, status=True):
        with self.connection:
            return self.cursor.execute("SELECT * FROM `subscriptions` WHERE `status` = ?", (status,)).fetchall()

    # Метод получения записи о юзере, существует ли он уже в БД или нет
    def subscriber_exists(self, user_id):
        with self.connection:
            result = self.cursor.execute('SELECT * FROM `subscriptions` WHERE `user_id` = ?', (user_id,)).fetchall()
            return bool(len(result))

    # Метод добавления записи в БД
    def add_subscriber(self, user_id, status=True):
        with self.connection:
            return self.cursor.execute("INSERT INTO `subscriptions` (`user_id`, `status`) VALUES(?,?)",
                                       (user_id, status))

    # Метод обновления статуса подписки пользователя
    def update_subscription(self, user_id, status):
        with self.connection:
            return self.cursor.execute("UPDATE `subscriptions` SET `status` = ? WHERE `user_id` = ?", (status, user_id))

    def close(self):
        self.connection.close()
