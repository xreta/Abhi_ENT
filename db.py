import sqlite3

# Connect to the database
conn = sqlite3.connect('verge_articles.db')

# Create a table to store the articles
cur = conn.cursor()
cur.execute('''
    CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY,
        url TEXT NOT NULL,
        headline TEXT NOT NULL,
        author TEXT NOT NULL,
        date TEXT NOT NULL
    )
''')
conn.commit()
