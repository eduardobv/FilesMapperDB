import sqlite3
import os
from datetime import datetime

class Repository:
    def __init__(self, db_path, db_info_path):
        self.db_path = db_path
        self.db_info_path = db_info_path
        # Si existe la base de datos, renombrar
        if os.path.exists(self.db_path):
            fecha = datetime.now().strftime('%Y-%m-%d-%H-%M')
            base, ext = os.path.splitext(self.db_path)
            new_name = f"{base}_{fecha}{ext}"
            os.rename(self.db_path, new_name)
        self.conn = sqlite3.connect(self.db_path)
        self.conn_info = sqlite3.connect(self.db_info_path)
        self.create_table()

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS directorios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                resolution TEXT,
                size TEXT NOT NULL,
                bytes INTEGER NOT NULL,
                files INTEGER NOT NULL,
                path TEXT NOT NULL,
                category TEXT,
                state TEXT,
                priority TEXT
            )
        ''')
        self.conn.commit()

    def insert_record(self, name, size, bytes, files, path, category=None, state=None, priority=None, resolution=None):
        cursor = self.conn.cursor()
        cursor.execute('''
            INSERT INTO directorios (name, resolution, size, bytes, files, path, category, state, priority)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, resolution, size, bytes, files, path, category, state, priority))
        self.conn.commit()

    def get_subscription_info(self, channel_id):
        cursor = self.conn_info.cursor()
        cursor.execute('''
            SELECT category, state, priority, resolution FROM subscriptions WHERE channelId = ?
        ''', (channel_id,))
        return cursor.fetchone()

    def close(self):
        self.conn.close()
        self.conn_info.close()
