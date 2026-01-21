from database import create_tables, connect_db
from datetime import datetime

create_tables()

def current_time():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def add_book(title, author):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO books (title, author, available) VALUES (?, ?, 1)",
        (title, author)
    )
    conn.commit()
    conn.close()
    print("Book added successfully")

def register_user(name, email):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO users (name, email) VALUES (?, ?)",
        (name, email)
    )
    conn.commit()
    conn.close()
    print("User registered successfully")

def issue_book(user_id, book_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT available FROM books WHERE book_id = ?", (book_id,))
    book = cursor.fetchone()
    
    if book and book[0] == 1:
        cursor.execute("UPDATE books SET available = 0 WHERE book_id = ?", (book_id,))
        cursor.execute(
            "INSERT INTO transactions (user_id, book_id, issue_date) VALUES (?, ?, ?)",
            (user_id, book_id, current_time())
        )
        conn.commit()
        print("Book issued successfully")
    else:
        print("Book not available")
    
    conn.close()

def return_book(book_id):
    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT available FROM books WHERE book_id = ?", (book_id,))
    book = cursor.fetchone()
    
    if book and book[0] == 0:
        cursor.execute("UPDATE books SET available = 1 WHERE book_id = ?", (book_id,))
        cursor.execute(
            "UPDATE transactions SET return_date = ? WHERE book_id = ? AND return_date IS NULL",
            (current_time(), book_id)
        )
        conn.commit()
        print("Book returned successfully")
    else:
        print("Book was not issued")
    
    conn.close()

def view_books():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM books")
    books = cursor.fetchall()
    print("\n--- Books ---")
    for book in books:
        status = "Available" if book[3] == 1 else "Issued"
        print(f"ID: {book[0]}, Title: {book[1]}, Author: {book[2]}, Status: {status}")
    conn.close()

def view_users():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    print("\n--- Users ---")
    for user in users:
        print(f"ID: {user[0]}, Name: {user[1]}, Email: {user[2]}")
    conn.close()

def view_transactions():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT t.transaction_id, u.name, b.title, t.issue_date, t.return_date
        FROM transactions t
        JOIN users u ON t.user_id = u.user_id
        JOIN books b ON t.book_id = b.book_id
    ''')
    transactions = cursor.fetchall()
    print("\n--- Transactions ---")
    for t in transactions:
        return_date = t[4] if t[4] else "Not returned"
        print(f"ID: {t[0]}, User: {t[1]}, Book: {t[2]}, Issued: {t[3]}, Returned: {return_date}")
    conn.close()

def menu():
    while True:
        print("\n--- Library Management System ---")
        print("1. Add Book")
        print("2. Register User")
        print("3. Issue Book")
        print("4. Return Book")
        print("5. View Books")
        print("6. View Users")
        print("7. View Transactions")
        print("8. Exit")
        
        choice = input("Enter choice: ")
        
        if choice == '1':
            title = input("Enter book title: ")
            author = input("Enter author name: ")
            add_book(title, author)
        elif choice == '2':
            name = input("Enter user name: ")
            email = input("Enter user email: ")
            register_user(name, email)
        elif choice == '3':
            user_id = int(input("Enter user ID: "))
            book_id = int(input("Enter book ID: "))
            issue_book(user_id, book_id)
        elif choice == '4':
            book_id = int(input("Enter book ID to return: "))
            return_book(book_id)
        elif choice == '5':
            view_books()
        elif choice == '6':
            view_users()
        elif choice == '7':
            view_transactions()
        elif choice == '8':
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

if __name__ == "__main__":
    menu()
