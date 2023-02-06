import sqlite3

cnx = sqlite3.connect('bank_data.db')

with open('schema.sql', 'r') as fp:
    cnx.executescript(fp.read())

cursor = cnx.cursor()

cursor.execute("INSERT INTO Bank_Settings (savings_rate, savings_min,"
                "checkings_rate, checkings_min) VALUES (?, ?, ?, ?)",
                (0.25, 5.0, 0.0, 0.0))

cursor.close()

cnx.commit()
cnx.close()