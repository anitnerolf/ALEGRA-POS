import sqlite3

conn = sqlite3.connect('alegra_products.db')
c = conn.cursor()

c.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, category TEXT, price REAL NOT NULL)''')


products = [
    ("Coca cola", "Drink", 3.50),
    ("Pizza M", "Food", 9.50),
    ("Pizza S", "Food", 6.50),
    ("Pizza L", "Food", 13.0)
]
c.executemany("INSERT INTO products (name, category, price) VALUES (?, ?, ?)", products)
conn.commit()
conn.close()