from datetime import datetime
import sqlite3
import os

db = sqlite3.connect("spl-saved-searches.sqlite")
db_cursor = db.cursor()
db_cursor.execute("CREATE TABLE IF NOT EXISTS saved_searches (_id INTEGER PRIMARY KEY, name TEXT NOT NULL, index TEXT, source TEXT, created_by TEXT NOT NULL, created_date TEXT NOT NULL)")

def update_db(name, index, source):
    update_cursor = db.cursor()
    created_by = os.getlogin()
    created_date = datetime.now()

    update_sql_statement = "INSERT INTO saved_searches (name, index, source, created_by, created_date) VALUES (?, ?, ?, ?)"
    update_cursor.execute(update_sql_statement, (name, index, source, created_by, created_date))
