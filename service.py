import sqlite3
from datetime import datetime

class Database:
    def __init__(self, db_name='/app/db/items.db'):  # Указываем путь к директории с базой данных
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.create_tables()


    def create_tables(self):
        # Создание таблицы для сообщений
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS processed_items (
                                id INTEGER PRIMARY KEY,
                                status TEXT,
                                added_at TEXT
                              )''')
        # Создание таблицы для подписчиков
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS subscribers (
                                user_id INTEGER PRIMARY KEY
                              )''')
        self.conn.commit()

    # Работа с подписчиками
    def add_subscriber(self, user_id):
        self.cursor.execute('INSERT OR IGNORE INTO subscribers (user_id) VALUES (?)', (user_id,))
        self.conn.commit()

    def remove_subscriber(self, user_id):
        self.cursor.execute('DELETE FROM subscribers WHERE user_id=?', (user_id,))
        self.conn.commit()

    def get_subscribers(self):
        self.cursor.execute('SELECT user_id FROM subscribers')
        return [row[0] for row in self.cursor.fetchall()]

    # Работа с элементами
    def get_item_status(self, item_id):
        self.cursor.execute('SELECT status FROM processed_items WHERE id=?', (item_id,))
        return self.cursor.fetchone()

    def add_item(self, item_id, status):
        added_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('INSERT INTO processed_items (id, status, added_at) VALUES (?, ?, ?)', 
                            (item_id, status, added_at))
        self.conn.commit()

    def update_item_status(self, item_id, new_status):
        added_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.cursor.execute('UPDATE processed_items SET status=?, added_at=? WHERE id=?', 
                            (new_status, added_at, item_id))
        self.conn.commit()
