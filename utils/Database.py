
import sqlite3


class Database:

    def __init__(self):
        self.create_db()

        # Функции работы с базой данных
    def create_db(self):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        # Создаем таблицу пользователей
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE,
            login TEXT UNIQUE,
            password TEXT
        )
        ''')

        # Создаем таблицу заметок
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            note TEXT,
            priority INTEGER,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
        ''')

        conn.commit()
        conn.close()

    def check_email(self, email):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
        user = cursor.fetchone()  # Возвращаем результат

        conn.close()
        return user is not None  # Если user не найден, значит email свободен

    def check_login(self, login):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM users WHERE login = ?", (login,))
        user = cursor.fetchone()  # Возвращаем результат

        conn.close()
        return user is not None  # Если user не найден, значит логин свободен

    def register_user(self, email, login, password):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO users (email, login, password) VALUES (?, ?, ?)', (email, login, password))
        conn.commit()
        conn.close()

        return True

    def login_user(self, email, password):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM users WHERE email=? AND password=?', (email, password))
        user = cursor.fetchone()
        conn.close()

        if user:
            return user[0]  # Возвращаем ID пользователя
        else:
            return None

    def create_note(self, user_id, note, priority):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        cursor.execute('INSERT INTO notes (user_id, note, priority) VALUES (?, ?, ?)', (user_id, note, priority))
        conn.commit()
        conn.close()

    def get_user_notes(self, user_id):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM notes WHERE user_id=?', (user_id,))
        notes = cursor.fetchall()
        conn.close()

        return notes

    def delete_note(self, note_id):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM notes WHERE id=?', (note_id,))
        conn.commit()
        conn.close()

    def get_user_notes_sorted(self, search_query="", sort_by="priority"):
        conn = sqlite3.connect('app.db')
        cursor = conn.cursor()

        query = "SELECT * FROM notes WHERE note LIKE ? ORDER BY " + (sort_by if sort_by else "priority")
        cursor.execute(query, (f"%{search_query}%",))
        notes = cursor.fetchall()

        conn.close()
        return notes

