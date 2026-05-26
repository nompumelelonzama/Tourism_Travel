import sqlite3

def init_db():
    conn = sqlite3.connect('tourism_system.db')
    c = conn.cursor()
    # Users Table
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (username TEXT PRIMARY KEY, password TEXT, role TEXT, budget REAL)''')
    # Bookings Table
    c.execute('''CREATE TABLE IF NOT EXISTS bookings 
                 (id INTEGER PRIMARY KEY, username TEXT, item_name TEXT, cost REAL, date TEXT)''')
    # Reviews Table
    c.execute('''CREATE TABLE IF NOT EXISTS reviews 
                 (username TEXT, hotel TEXT, review TEXT, sentiment TEXT)''')
    conn.commit()
    conn.close()

def add_booking(username, item, cost):
    conn = sqlite3.connect('tourism_system.db')
    c = conn.cursor()
    c.execute("INSERT INTO bookings (username, item_name, cost, date) VALUES (?, ?, ?, '2023-12-01')", (username, item, cost))
    conn.commit()
    conn.close()

init_db()