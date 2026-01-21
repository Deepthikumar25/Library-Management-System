import sqlite3

def connect_db():
    return sqlite3.connect("library.db")

def create_tables():
    conn = connect_db()
    cursor = conn.cursor()
    
    # Books table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS books (
            book_id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            available INTEGER DEFAULT 1
        )
    ''')
    
    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE
        )
    ''')

    # Transactions table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            transaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            book_id INTEGER,
            issue_date TEXT,
            return_date TEXT,
            FOREIGN KEY(user_id) REFERENCES users(user_id),
            FOREIGN KEY(book_id) REFERENCES books(book_id)
        )
    ''')
    
    conn.commit()
    conn.close()
